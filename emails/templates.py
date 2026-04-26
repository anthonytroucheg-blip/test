"""
Templates d'emails automatiques pour chaque étape du parcours client.
Supporte le français, anglais, néerlandais, allemand et espagnol.
"""

from core.csv_loader import Reservation
from config.camping import CAMPING, HEBERGEMENTS, EQUIPEMENTS, LOCALISATION

# ---------------------------------------------------------------------------
# Helpers HTML
# ---------------------------------------------------------------------------

_STYLE_BASE = """
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333;">
  <div style="background-color: #2e7d32; padding: 20px; text-align: center;">
    <h1 style="color: white; margin: 0; font-size: 22px;">{nom_camping}</h1>
    <p style="color: #c8e6c9; margin: 4px 0 0; font-size: 14px;">{sous_titre}</p>
  </div>
  <div style="padding: 30px 24px;">
    {corps}
  </div>
  <div style="background-color: #f5f5f5; padding: 16px 24px; font-size: 12px; color: #777; text-align: center;">
    {nom_camping} · {adresse} · {telephone}<br>
    <a href="{site_web}" style="color: #2e7d32;">{site_web}</a>
  </div>
</div>
"""


def _enveloppe(sous_titre: str, corps: str) -> str:
    return _STYLE_BASE.format(
        nom_camping=CAMPING["nom"],
        sous_titre=sous_titre,
        corps=corps,
        adresse=CAMPING["adresse"],
        telephone=CAMPING["telephone"],
        site_web=CAMPING["site_web"],
    )


# ---------------------------------------------------------------------------
# Templates par langue et étape
# ---------------------------------------------------------------------------

def email_j_moins_7(resa: Reservation) -> tuple[str, str]:
    """Retourne (sujet, corps_html) pour J-7."""
    lang = resa.code_langue
    arrivee = resa.date_arrivee.strftime("%d/%m/%Y")
    depart = resa.date_depart.strftime("%d/%m/%Y")
    check_in = HEBERGEMENTS["locations"]["check_in"] if resa.est_location else HEBERGEMENTS["emplacements"]["check_in"]
    check_out = HEBERGEMENTS["locations"]["check_out"] if resa.est_location else HEBERGEMENTS["emplacements"]["check_out"]

    if lang == "en":
        sujet = f"Your stay at {CAMPING['nom']} is in 7 days!"
        corps = f"""
        <p>Dear {resa.salutation},</p>
        <p>Your stay is approaching! We look forward to welcoming you on <strong>{arrivee}</strong>.</p>
        <h3>Your stay details</h3>
        <ul>
          <li><strong>Arrival:</strong> {arrivee} from {check_in}</li>
          <li><strong>Departure:</strong> {depart} before {check_out}</li>
          <li><strong>Pitch/Accommodation:</strong> {resa.emplacement or 'to be assigned at arrival'}</li>
        </ul>
        <h3>How to get here</h3>
        <p>We are located at {CAMPING['adresse']}.</p>
        <h3>Activities nearby</h3>
        <p>{', '.join(LOCALISATION['attractions_proches'])}</p>
        <p>Any question? Simply reply to this email, we'll be happy to help!</p>
        <p>See you soon,<br>The team at {CAMPING['nom']}</p>
        """
    elif lang == "nl":
        sujet = f"Uw verblijf bij {CAMPING['nom']} over 7 dagen!"
        corps = f"""
        <p>Beste {resa.salutation},</p>
        <p>Uw verblijf nadert! We kijken ernaar uit u te verwelkomen op <strong>{arrivee}</strong>.</p>
        <h3>Uw verblijfdetails</h3>
        <ul>
          <li><strong>Aankomst:</strong> {arrivee} vanaf {check_in}</li>
          <li><strong>Vertrek:</strong> {depart} voor {check_out}</li>
          <li><strong>Standplaats/Accommodatie:</strong> {resa.emplacement or 'wordt toegewezen bij aankomst'}</li>
        </ul>
        <h3>Hoe ons te bereiken</h3>
        <p>Wij zijn gevestigd op {CAMPING['adresse']}.</p>
        <p>Heeft u vragen? Antwoord gewoon op deze e-mail!</p>
        <p>Tot ziens,<br>Het team van {CAMPING['nom']}</p>
        """
    elif lang == "de":
        sujet = f"Ihr Aufenthalt bei {CAMPING['nom']} in 7 Tagen!"
        corps = f"""
        <p>Sehr geehrte/r {resa.salutation},</p>
        <p>Ihr Aufenthalt rückt näher! Wir freuen uns darauf, Sie am <strong>{arrivee}</strong> willkommen zu heißen.</p>
        <h3>Ihre Aufenthaltsdaten</h3>
        <ul>
          <li><strong>Anreise:</strong> {arrivee} ab {check_in}</li>
          <li><strong>Abreise:</strong> {depart} bis {check_out}</li>
          <li><strong>Stellplatz/Unterkunft:</strong> {resa.emplacement or 'wird bei Ankunft zugewiesen'}</li>
        </ul>
        <h3>Anfahrt</h3>
        <p>Wir befinden uns in {CAMPING['adresse']}.</p>
        <p>Bei Fragen antworten Sie einfach auf diese E-Mail!</p>
        <p>Bis bald,<br>Das Team von {CAMPING['nom']}</p>
        """
    elif lang == "es":
        sujet = f"¡Su estancia en {CAMPING['nom']} es en 7 días!"
        corps = f"""
        <p>Estimado/a {resa.salutation},</p>
        <p>¡Su estancia se acerca! Esperamos darle la bienvenida el <strong>{arrivee}</strong>.</p>
        <h3>Detalles de su estancia</h3>
        <ul>
          <li><strong>Llegada:</strong> {arrivee} a partir de las {check_in}</li>
          <li><strong>Salida:</strong> {depart} antes de las {check_out}</li>
          <li><strong>Parcela/Alojamiento:</strong> {resa.emplacement or 'se asignará a la llegada'}</li>
        </ul>
        <h3>Cómo llegar</h3>
        <p>Estamos en {CAMPING['adresse']}.</p>
        <p>¿Alguna pregunta? ¡Responda a este correo!</p>
        <p>¡Hasta pronto!<br>El equipo de {CAMPING['nom']}</p>
        """
    else:  # fr par défaut
        sujet = f"Votre séjour au {CAMPING['nom']} dans 7 jours !"
        corps = f"""
        <p>Bonjour {resa.salutation},</p>
        <p>Votre séjour approche ! Nous avons hâte de vous accueillir le <strong>{arrivee}</strong>.</p>
        <h3>Récapitulatif de votre séjour</h3>
        <ul>
          <li><strong>Arrivée :</strong> {arrivee} à partir de {check_in}</li>
          <li><strong>Départ :</strong> {depart} avant {check_out}</li>
          <li><strong>Emplacement :</strong> {resa.emplacement or "attribué à l'arrivée"}</li>
        </ul>
        <h3>Comment nous rejoindre</h3>
        <p>Nous sommes situés au {CAMPING['adresse']}.</p>
        <h3>À découvrir autour du camping</h3>
        <p>{', '.join(LOCALISATION['attractions_proches'])}</p>
        <p>Une question ? Répondez simplement à cet email, nous sommes là pour vous aider !</p>
        <p>À très bientôt,<br>L'équipe du {CAMPING['nom']}</p>
        """

    sous_titre = {"en": "Your holiday countdown", "nl": "Aftellen naar uw vakantie",
                  "de": "Ihr Urlaubs-Countdown", "es": "La cuenta atrás de sus vacaciones"}.get(lang, "Le compte à rebours de vos vacances")
    return sujet, _enveloppe(sous_titre, corps)


def email_j_moins_1(resa: Reservation) -> tuple[str, str]:
    """Retourne (sujet, corps_html) pour J-1."""
    lang = resa.code_langue
    arrivee = resa.date_arrivee.strftime("%d/%m/%Y")
    check_in = HEBERGEMENTS["locations"]["check_in"] if resa.est_location else HEBERGEMENTS["emplacements"]["check_in"]

    if lang == "en":
        sujet = f"See you tomorrow at {CAMPING['nom']}!"
        corps = f"""
        <p>Dear {resa.salutation},</p>
        <p>Tomorrow is the big day! We're ready to welcome you from <strong>{check_in}</strong>.</p>
        <h3>Practical information</h3>
        <ul>
          <li>Reception is open from <strong>8:00 AM to 8:00 PM</strong></li>
          <li>Check-in from <strong>{check_in}</strong></li>
          <li>Address: {CAMPING['adresse']}</li>
          <li>Phone: {CAMPING['telephone']}</li>
        </ul>
        <p>Don't forget: animals are welcome with an up-to-date vaccination record, kept on a leash on the campsite.</p>
        <p>See you tomorrow!<br>The team at {CAMPING['nom']}</p>
        """
    elif lang == "nl":
        sujet = f"Tot morgen bij {CAMPING['nom']}!"
        corps = f"""
        <p>Beste {resa.salutation},</p>
        <p>Morgen is het zover! We staan klaar om u te verwelkomen vanaf <strong>{check_in}</strong>.</p>
        <h3>Praktische informatie</h3>
        <ul>
          <li>Receptie open van <strong>8:00 tot 20:00</strong></li>
          <li>Inchecken vanaf <strong>{check_in}</strong></li>
          <li>Adres: {CAMPING['adresse']}</li>
          <li>Telefoon: {CAMPING['telephone']}</li>
        </ul>
        <p>Tot morgen!<br>Het team van {CAMPING['nom']}</p>
        """
    elif lang == "de":
        sujet = f"Bis morgen bei {CAMPING['nom']}!"
        corps = f"""
        <p>Sehr geehrte/r {resa.salutation},</p>
        <p>Morgen ist es soweit! Wir empfangen Sie ab <strong>{check_in}</strong>.</p>
        <h3>Praktische Informationen</h3>
        <ul>
          <li>Rezeption geöffnet von <strong>8:00 bis 20:00 Uhr</strong></li>
          <li>Check-in ab <strong>{check_in}</strong></li>
          <li>Adresse: {CAMPING['adresse']}</li>
          <li>Telefon: {CAMPING['telephone']}</li>
        </ul>
        <p>Bis morgen!<br>Das Team von {CAMPING['nom']}</p>
        """
    elif lang == "es":
        sujet = f"¡Hasta mañana en {CAMPING['nom']}!"
        corps = f"""
        <p>Estimado/a {resa.salutation},</p>
        <p>¡Mañana es el gran día! Estaremos listos para recibirle a partir de las <strong>{check_in}</strong>.</p>
        <h3>Información práctica</h3>
        <ul>
          <li>Recepción abierta de <strong>8:00 a 20:00</strong></li>
          <li>Llegada a partir de las <strong>{check_in}</strong></li>
          <li>Dirección: {CAMPING['adresse']}</li>
          <li>Teléfono: {CAMPING['telephone']}</li>
        </ul>
        <p>¡Hasta mañana!<br>El equipo de {CAMPING['nom']}</p>
        """
    else:
        sujet = f"À demain au {CAMPING['nom']} !"
        corps = f"""
        <p>Bonjour {resa.salutation},</p>
        <p>C'est demain ! Nous serons prêts à vous accueillir dès <strong>{check_in}</strong>.</p>
        <h3>Informations pratiques</h3>
        <ul>
          <li>L'accueil est ouvert de <strong>8h00 à 20h00</strong></li>
          <li>Arrivée à partir de <strong>{check_in}</strong></li>
          <li>Adresse : {CAMPING['adresse']}</li>
          <li>Téléphone : {CAMPING['telephone']}</li>
        </ul>
        <p>N'oubliez pas : les animaux sont acceptés avec le carnet de vaccination à jour, tenus en laisse.</p>
        <p>À demain !<br>L'équipe du {CAMPING['nom']}</p>
        """

    sous_titre = {"en": "Ready to welcome you tomorrow", "nl": "Klaar om u morgen te verwelkomen",
                  "de": "Bereit, Sie morgen zu begrüßen", "es": "Listos para recibirle mañana"}.get(lang, "Prêts à vous accueillir demain")
    return sujet, _enveloppe(sous_titre, corps)


def email_jour_arrivee(resa: Reservation) -> tuple[str, str]:
    """Retourne (sujet, corps_html) pour le jour d'arrivée."""
    lang = resa.code_langue
    check_in = HEBERGEMENTS["locations"]["check_in"] if resa.est_location else HEBERGEMENTS["emplacements"]["check_in"]
    activites = ", ".join(EQUIPEMENTS["activites"][:5])

    if lang == "en":
        sujet = f"Welcome to {CAMPING['nom']}!"
        corps = f"""
        <p>Dear {resa.salutation},</p>
        <p>Welcome! We hope your journey went well.</p>
        <h3>Check-in</h3>
        <p>Reception is open until 8:00 PM. Check-in from <strong>{check_in}</strong>.<br>
        Your pitch/accommodation: <strong>{resa.emplacement or 'will be assigned at check-in'}</strong>.</p>
        <h3>Activities available</h3>
        <p>{activites} and more!</p>
        <h3>WiFi</h3>
        <p>Free WiFi available throughout the campsite.</p>
        <p>If you have any question, feel free to reply to this email. Enjoy your stay!</p>
        <p>The team at {CAMPING['nom']}</p>
        """
    elif lang == "nl":
        sujet = f"Welkom bij {CAMPING['nom']}!"
        corps = f"""
        <p>Beste {resa.salutation},</p>
        <p>Welkom! We hopen dat uw reis goed was.</p>
        <h3>Inchecken</h3>
        <p>Receptie open tot 20:00. Inchecken vanaf <strong>{check_in}</strong>.<br>
        Uw standplaats: <strong>{resa.emplacement or 'wordt bij aankomst toegewezen'}</strong>.</p>
        <h3>Activiteiten</h3>
        <p>{activites} en meer!</p>
        <p>Fijne vakantie!<br>Het team van {CAMPING['nom']}</p>
        """
    elif lang == "de":
        sujet = f"Willkommen bei {CAMPING['nom']}!"
        corps = f"""
        <p>Sehr geehrte/r {resa.salutation},</p>
        <p>Willkommen! Wir hoffen, Ihre Anreise war angenehm.</p>
        <h3>Check-in</h3>
        <p>Rezeption bis 20:00 Uhr geöffnet. Check-in ab <strong>{check_in}</strong>.<br>
        Ihr Stellplatz: <strong>{resa.emplacement or 'wird bei Ankunft zugewiesen'}</strong>.</p>
        <h3>Aktivitäten</h3>
        <p>{activites} und mehr!</p>
        <p>Schönen Urlaub!<br>Das Team von {CAMPING['nom']}</p>
        """
    elif lang == "es":
        sujet = f"¡Bienvenido/a a {CAMPING['nom']}!"
        corps = f"""
        <p>Estimado/a {resa.salutation},</p>
        <p>¡Bienvenido/a! Esperamos que su viaje haya sido agradable.</p>
        <h3>Check-in</h3>
        <p>Recepción abierta hasta las 20:00. Llegada a partir de las <strong>{check_in}</strong>.<br>
        Su parcela: <strong>{resa.emplacement or 'se asignará a la llegada'}</strong>.</p>
        <h3>Actividades</h3>
        <p>{activites} ¡y más!</p>
        <p>¡Que disfrute su estancia!<br>El equipo de {CAMPING['nom']}</p>
        """
    else:
        sujet = f"Bienvenue au {CAMPING['nom']} !"
        corps = f"""
        <p>Bonjour {resa.salutation},</p>
        <p>Bienvenue ! Nous espérons que votre trajet s'est bien passé.</p>
        <h3>Votre arrivée</h3>
        <p>L'accueil est ouvert jusqu'à 20h00. Arrivée à partir de <strong>{check_in}</strong>.<br>
        Votre emplacement : <strong>{resa.emplacement or "vous sera attribué à l'accueil"}</strong>.</p>
        <h3>Ce qui vous attend</h3>
        <p>Piscine chauffée, plage privée sur la Dourbie, {activites}...</p>
        <h3>WiFi</h3>
        <p>WiFi gratuit disponible sur tout le camping.</p>
        <p>Une question pendant votre séjour ? Répondez à cet email, nous sommes là !</p>
        <p>L'équipe du {CAMPING['nom']}</p>
        """

    sous_titre = {"en": "Your holiday starts today!", "nl": "Uw vakantie begint vandaag!",
                  "de": "Ihr Urlaub beginnt heute!", "es": "¡Sus vacaciones comienzan hoy!"}.get(lang, "Vos vacances commencent aujourd'hui !")
    return sujet, _enveloppe(sous_titre, corps)


def email_j_plus_2(resa: Reservation) -> tuple[str, str]:
    """Retourne (sujet, corps_html) pour J+2 (demande d'avis)."""
    lang = resa.code_langue
    lien_tripadvisor = CAMPING["lien_avis_tripadvisor"]
    lien_google = CAMPING.get("lien_avis_google", "")

    if lang == "en":
        sujet = f"How was your stay at {CAMPING['nom']}?"
        corps = f"""
        <p>Dear {resa.salutation},</p>
        <p>We hope you had a wonderful time with us and that you arrived home safely.</p>
        <p>Your opinion matters a lot to us and helps other travellers discover our campsite.</p>
        <p>Could you take 2 minutes to share your experience?</p>
        <p style="text-align:center; margin: 24px 0;">
          <a href="{lien_tripadvisor}" style="background:#2e7d32; color:white; padding:12px 24px; text-decoration:none; border-radius:4px;">
            Leave a review on TripAdvisor
          </a>
        </p>
        {f'<p style="text-align:center;"><a href="{lien_google}" style="color:#2e7d32;">Leave a review on Google</a></p>' if lien_google else ''}
        <p>Thank you, and we hope to see you again soon!</p>
        <p>The team at {CAMPING['nom']}</p>
        """
    elif lang == "nl":
        sujet = f"Hoe was uw verblijf bij {CAMPING['nom']}?"
        corps = f"""
        <p>Beste {resa.salutation},</p>
        <p>We hopen dat u een geweldige tijd bij ons heeft gehad en veilig thuis bent aangekomen.</p>
        <p>Uw mening helpt andere reizigers onze camping te ontdekken.</p>
        <p style="text-align:center; margin: 24px 0;">
          <a href="{lien_tripadvisor}" style="background:#2e7d32; color:white; padding:12px 24px; text-decoration:none; border-radius:4px;">
            Schrijf een beoordeling op TripAdvisor
          </a>
        </p>
        <p>Bedankt en tot de volgende keer!<br>Het team van {CAMPING['nom']}</p>
        """
    elif lang == "de":
        sujet = f"Wie war Ihr Aufenthalt bei {CAMPING['nom']}?"
        corps = f"""
        <p>Sehr geehrte/r {resa.salutation},</p>
        <p>Wir hoffen, Sie hatten eine wunderbare Zeit bei uns und sind gut nach Hause gekommen.</p>
        <p>Ihre Meinung hilft anderen Reisenden, unseren Campingplatz zu entdecken.</p>
        <p style="text-align:center; margin: 24px 0;">
          <a href="{lien_tripadvisor}" style="background:#2e7d32; color:white; padding:12px 24px; text-decoration:none; border-radius:4px;">
            Bewertung auf TripAdvisor schreiben
          </a>
        </p>
        <p>Danke und bis zum nächsten Mal!<br>Das Team von {CAMPING['nom']}</p>
        """
    elif lang == "es":
        sujet = f"¿Cómo fue su estancia en {CAMPING['nom']}?"
        corps = f"""
        <p>Estimado/a {resa.salutation},</p>
        <p>Esperamos que haya tenido una estancia maravillosa y que haya llegado bien a casa.</p>
        <p>Su opinión ayuda a otros viajeros a descubrir nuestro camping.</p>
        <p style="text-align:center; margin: 24px 0;">
          <a href="{lien_tripadvisor}" style="background:#2e7d32; color:white; padding:12px 24px; text-decoration:none; border-radius:4px;">
            Dejar una reseña en TripAdvisor
          </a>
        </p>
        <p>¡Gracias y hasta la próxima!<br>El equipo de {CAMPING['nom']}</p>
        """
    else:
        sujet = f"Comment s'est passé votre séjour au {CAMPING['nom']} ?"
        corps = f"""
        <p>Bonjour {resa.salutation},</p>
        <p>Nous espérons que vous avez passé un excellent séjour parmi nous et que vous êtes bien rentré(e).</p>
        <p>Votre avis compte beaucoup pour nous et aide d'autres voyageurs à découvrir notre camping.</p>
        <p>Pourriez-vous prendre 2 minutes pour partager votre expérience ?</p>
        <p style="text-align:center; margin: 24px 0;">
          <a href="{lien_tripadvisor}" style="background:#2e7d32; color:white; padding:12px 24px; text-decoration:none; border-radius:4px;">
            Laisser un avis sur TripAdvisor
          </a>
        </p>
        {f'<p style="text-align:center;"><a href="{lien_google}" style="color:#2e7d32;">Laisser un avis sur Google</a></p>' if lien_google else ''}
        <p>Merci et à bientôt !<br>L'équipe du {CAMPING['nom']}</p>
        """

    sous_titre = {"en": "Thank you for choosing us", "nl": "Bedankt voor uw keuze",
                  "de": "Danke für Ihre Wahl", "es": "Gracias por elegirnos"}.get(lang, "Merci de nous avoir choisis")
    return sujet, _enveloppe(sous_titre, corps)


def email_annulation(resa: Reservation) -> tuple[str, str]:
    """Retourne (sujet, corps_html) pour une annulation."""
    lang = resa.code_langue

    if lang == "en":
        sujet = f"Your cancellation – {CAMPING['nom']}"
        corps = f"""
        <p>Dear {resa.salutation},</p>
        <p>We have noted the cancellation of your reservation.</p>
        <p>We're sorry you won't be joining us this time. If you have any questions about your cancellation,
        please contact our reception directly at {CAMPING['telephone']} or {CAMPING['email_contact']}.</p>
        <p>We hope to welcome you another time!</p>
        <p>The team at {CAMPING['nom']}</p>
        """
    elif lang == "nl":
        sujet = f"Uw annulering – {CAMPING['nom']}"
        corps = f"""
        <p>Beste {resa.salutation},</p>
        <p>Wij bevestigen de annulering van uw reservering.</p>
        <p>Het spijt ons dat u er dit keer niet bij kunt zijn. Voor vragen kunt u contact opnemen via
        {CAMPING['telephone']} of {CAMPING['email_contact']}.</p>
        <p>Tot de volgende keer!<br>Het team van {CAMPING['nom']}</p>
        """
    elif lang == "de":
        sujet = f"Ihre Stornierung – {CAMPING['nom']}"
        corps = f"""
        <p>Sehr geehrte/r {resa.salutation},</p>
        <p>Wir bestätigen die Stornierung Ihrer Reservierung.</p>
        <p>Es tut uns leid, dass Sie dieses Mal nicht dabei sein können. Bei Fragen erreichen Sie uns unter
        {CAMPING['telephone']} oder {CAMPING['email_contact']}.</p>
        <p>Bis zum nächsten Mal!<br>Das Team von {CAMPING['nom']}</p>
        """
    elif lang == "es":
        sujet = f"Su cancelación – {CAMPING['nom']}"
        corps = f"""
        <p>Estimado/a {resa.salutation},</p>
        <p>Confirmamos la cancelación de su reserva.</p>
        <p>Sentimos que no pueda unirse a nosotros esta vez. Para cualquier pregunta, contáctenos en
        {CAMPING['telephone']} o {CAMPING['email_contact']}.</p>
        <p>¡Esperamos verle otro día!<br>El equipo de {CAMPING['nom']}</p>
        """
    else:
        sujet = f"Votre annulation – {CAMPING['nom']}"
        corps = f"""
        <p>Bonjour {resa.salutation},</p>
        <p>Nous avons bien pris note de l'annulation de votre réservation.</p>
        <p>Nous sommes désolés de ne pas pouvoir vous accueillir cette fois-ci. Pour toute question
        concernant votre annulation, n'hésitez pas à contacter directement notre accueil au
        {CAMPING['telephone']} ou par email à {CAMPING['email_contact']}.</p>
        <p>Nous espérons vous accueillir une prochaine fois !</p>
        <p>L'équipe du {CAMPING['nom']}</p>
        """

    sous_titre = {"en": "Cancellation confirmed", "nl": "Annulering bevestigd",
                  "de": "Stornierung bestätigt", "es": "Cancelación confirmada"}.get(lang, "Annulation confirmée")
    return sujet, _enveloppe(sous_titre, corps)


ETAPE_VERS_TEMPLATE = {
    "j_moins_7": email_j_moins_7,
    "j_moins_1": email_j_moins_1,
    "jour_arrivee": email_jour_arrivee,
    "j_plus_2": email_j_plus_2,
    "annulation": email_annulation,
}


def generer_email_pour_etape(resa: Reservation, etape: str) -> tuple[str, str] | None:
    """Génère (sujet, html) si l'étape a un template automatique, sinon None."""
    fn = ETAPE_VERS_TEMPLATE.get(etape)
    if fn:
        return fn(resa)
    return None
