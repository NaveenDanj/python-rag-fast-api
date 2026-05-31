import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI
from app.config.config import get_settings
from app.utils.utils import generate_invitation_email_prompt
logger = logging.getLogger("app")

settings = get_settings()

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

    async def send_email(self, to_email: str, subject: str, body: str, is_html: bool = False):
        try:
            sender_email = settings.gmail_username
            sender_password = settings.gmail_app_password.replace(" ", "")
            
            if not sender_email or not sender_password:
                raise ValueError("Gmail credentials not found in environment variables. Set GMAIL_USERNAME and GMAIL_APP_PASSWORD.")
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = to_email
            
            mime_type = "html" if is_html else "plain"
            message.attach(MIMEText(body, mime_type))
            
            # Send email via Gmail SMTP
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
            
            logger.info(f"Email sent successfully to {to_email}")
            return {
                "success": True,
                "message": f"Email sent successfully to {to_email}"
            }
        
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error while sending email: {e}")
            raise
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {e}")
            raise