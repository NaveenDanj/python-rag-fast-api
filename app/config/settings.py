from app.service.services import InvitationService
from app.config.config import get_settings

settings = get_settings()

_invitation_service = InvitationService(
    settings.agenda_file_path,
    settings.openai_api_key
)

def get_invitation_service():
    return _invitation_service