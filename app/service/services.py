import logging
from datetime import datetime
from openai import OpenAI

from app.service.agenda import AgendaManager
from app.service.rag import RAGMatcher
from app.service.email import EmailGenerator

logger = logging.getLogger("app")


class InvitationService:
    
    def __init__(self, agenda_file_path: str, openai_api_key: str, openai_base_url: str | None = None):
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY is required. Set it as a runtime environment variable when running in Docker.")

        client_kwargs = {"api_key": openai_api_key}
        if openai_base_url:
            client_kwargs["base_url"] = openai_base_url

        self.client = OpenAI(**client_kwargs)
        self.agenda = AgendaManager(agenda_file_path)
        self.rag_matcher = RAGMatcher(self.client, self.agenda.get_all_sessions())
        self.email_generator = EmailGenerator(self.client)
    
    def get_sessions(self):
        return self.agenda.get_all_sessions()
    
    async def generate_invitation(
        self,
        name: str,
        email: str,
        focus: str
    ):
        try:
            logger.info(f"Processing invitation for {email}")      
            session = await self.rag_matcher.match_session(focus)
            print(session)
            
            if not session:
                logger.warning(f"No session match found for {email}")
                return {"success": False, "error": "No matching session found"}
            
            email_body = await self.email_generator.generate_invitation_email(
                name,
                session,
                focus
            )
            
            # await self.email_generator.send_email(
            #     to_email=email,
            #     subject=f"Invitation to {session['name']} Session",
            #     body=email_body,
            #     is_html=False
            # )
            
            timestamp = datetime.utcnow().isoformat() + "Z"
            
            logger.info(f"Generated invitation for {email}")
            
            return {
                "success": True,
                "matched_session": session["name"],
                "email_body": email_body,
                "timestamp": timestamp
            }
        
        except Exception as e:
            logger.error(f"Error in generate_invitation: {e}")
            return {"success": False, "error": str(e)}
