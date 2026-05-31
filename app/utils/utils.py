import logging
import json

logger = logging.getLogger("app")

def log_email_sent(logger_instance: logging.Logger,recipient_email: str,email_body: str,timestamp: str):
    log_data = {
        "action": "email_sent",
        "recipient": recipient_email,
        "timestamp": timestamp,
        "body_chars": len(email_body)
    }
    
    logger_instance.info(f"EMAIL_SENT: {json.dumps(log_data)}")
    
    print(f"\n{'='*70}")
    print("EMAIL SENT - MCP ACTION LOG")
    print(f"{'='*70}")
    print(f"Recipient:  {recipient_email}")
    print(f"Timestamp:  {timestamp}")
    print(f"Subject:    Event Invitation - Your Personalized Session")
    print(f"{'='*70}")
    print(f"Body:\n{email_body}")
    print(f"{'='*70}\n")


def cosine_similarity(vec1: list[float], vec2: list[float]):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = sum(a * a for a in vec1) ** 0.5
    mag2 = sum(b * b for b in vec2) ** 0.5
    return dot_product / (mag1 * mag2) if mag1 and mag2 else 0.0



def generate_invitation_email_prompt(name: str, session: dict, focus: str):
    return f"""Generate a professional, personalized B2B invitation email.

IMPORTANT: Use ONLY the provided session information. Do NOT invent or hallucinate any details.

Recipient: {name}
Professional Focus: {focus}

Session Details:
- Name: {session['name']}
- Time: {session['time']}
- Speaker: {session['speaker']}
- Description: {session['description']}

include the company name as Cogent Solutions Event Marketing Pvt Ltd no need to add other placeholders
Do not include any information that is not provided in the session details. The email should be concise, engaging, and clearly communicate the value of attending the session. Write a 3-sentence professional invitation email:"""
