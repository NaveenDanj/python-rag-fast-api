import logging
from openai import OpenAI
from app.utils.utils import generate_invitation_email_prompt
logger = logging.getLogger("app")

class EmailGenerator:
    
    def __init__(self, client: OpenAI):
        self.client = client
    
    async def generate_invitation_email(self, name: str, session: dict, focus: str):
        try:
            prompt = generate_invitation_email_prompt(name, session, focus)
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional event coordinator. Generate invitations using ONLY provided data. Never hallucinate information."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=512
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"Error generating email: {e}")
            raise
