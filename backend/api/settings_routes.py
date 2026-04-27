from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Setting
from ..schemas import SettingOut, UpdateSettingsIn

router = APIRouter(prefix="/api/settings", tags=["settings"])

SETTING_KEYS = ["company_name", "openai_api_key", "openai_model", "response_style"]


@router.get("", response_model=list[SettingOut])
def get_settings(db: Session = Depends(get_db)):
    settings = db.query(Setting).filter(Setting.key.in_(SETTING_KEYS)).all()
    existing_keys = {s.key for s in settings}
    defaults = {"company_name": "Mon Entreprise", "openai_model": "gpt-4o",
                "response_style": "professionnel", "openai_api_key": ""}
    for key in SETTING_KEYS:
        if key not in existing_keys:
            settings.append(Setting(key=key, value=defaults.get(key, "")))
    # Mask API key
    result = []
    for s in settings:
        if s.key == "openai_api_key" and s.value:
            result.append(SettingOut(key=s.key, value="sk-...•••" + s.value[-4:]))
        else:
            result.append(SettingOut(key=s.key, value=s.value))
    return result


@router.put("", response_model=list[SettingOut])
def update_settings(body: UpdateSettingsIn, db: Session = Depends(get_db)):
    updates = body.model_dump(exclude_none=True)
    for key, value in updates.items():
        if key not in SETTING_KEYS:
            continue
        existing = db.query(Setting).filter(Setting.key == key).first()
        if existing:
            existing.value = value
            existing.updated_at = datetime.utcnow()
        else:
            db.add(Setting(key=key, value=value))

    # Sync openai settings to runtime config
    from ..config import settings as app_settings
    if "openai_api_key" in updates:
        app_settings.openai_api_key = updates["openai_api_key"]
    if "openai_model" in updates:
        app_settings.openai_model = updates["openai_model"]
    if "response_style" in updates:
        app_settings.response_style = updates["response_style"]

    db.commit()
    return get_settings(db)
