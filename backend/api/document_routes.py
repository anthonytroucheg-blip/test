import io
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import MemoryItem

router = APIRouter(prefix="/api/memory", tags=["documents"])

ALLOWED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/markdown",
}

MAX_SIZE_MB = 10


def _extract_text(file: UploadFile, data: bytes) -> str:
    ct = file.content_type or ""

    if ct == "application/pdf" or file.filename.lower().endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(data))
        pages = [p.extract_text() or "" for p in reader.pages]
        return "\n\n".join(p.strip() for p in pages if p.strip())

    if (
        ct == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        or file.filename.lower().endswith(".docx")
    ):
        from docx import Document
        doc = Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    # TXT / Markdown / fallback
    return data.decode("utf-8", errors="replace")


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form(default="notes"),
    title: str = Form(default=""),
    db: Session = Depends(get_db),
):
    data = await file.read()

    if len(data) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(413, f"Fichier trop volumineux (max {MAX_SIZE_MB} Mo)")

    try:
        text = _extract_text(file, data)
    except Exception as e:
        raise HTTPException(422, f"Impossible de lire le fichier : {e}")

    if not text.strip():
        raise HTTPException(422, "Le document semble vide ou illisible")

    item_title = title.strip() or file.filename or "Document importé"

    item = MemoryItem(
        category=category,
        title=item_title,
        content=text.strip(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "id": item.id,
        "category": item.category,
        "title": item.title,
        "content": item.content,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
        "chars": len(text),
    }
