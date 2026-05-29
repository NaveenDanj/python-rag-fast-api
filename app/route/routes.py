import logging
from fastapi import APIRouter, HTTPException, status, Depends

from app.schema.schemas import VisitorInput, InvitationResponse
from app.service.services import InvitationService
from app.utils.utils import log_email_sent
from app.config.settings import get_invitation_service

logger = logging.getLogger("app")

router = APIRouter()


def send_draft_via_mcp(email_address: str, email_body: str, timestamp: str) :
    log_email_sent(logger, email_address, email_body, timestamp)


@router.get("/")
async def root():
    return {
        "message": "Event Invitation System API",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0"
    }


@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@router.get("/api/v1/agenda")
async def get_agenda(service: InvitationService = Depends(get_invitation_service)):
    sessions = service.get_sessions()
    
    return {
        "total_sessions": len(sessions),
        "sessions": sessions
    }


@router.post("/api/v1/generate-invitation", response_model=InvitationResponse)
async def generate_invitation(
    visitor_input: VisitorInput,
    service: InvitationService = Depends(get_invitation_service)
) -> InvitationResponse:
    try:
        logger.info(f"Processing invitation for {visitor_input.email}")
        
        result = await service.generate_invitation(
            name=visitor_input.name,
            email=visitor_input.email,
            focus=visitor_input.professional_focus
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to generate invitation")
            )
        
        timestamp = result["timestamp"]
        email_body = result["email_body"]
        send_draft_via_mcp(visitor_input.email, email_body, timestamp)
        
        logger.info(f"Invitation sent to {visitor_input.email}")
        
        return InvitationResponse(
            visitor_name=visitor_input.name,
            visitor_email=visitor_input.email,
            matched_session=result["matched_session"],
            email_body=email_body,
            timestamp=timestamp,
            status="success"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
