from pydantic import BaseModel, EmailStr, Field


class VisitorInput(BaseModel):    
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    professional_focus: str = Field(..., min_length=10, max_length=500)


class InvitationResponse(BaseModel):    
    visitor_name: str
    visitor_email: str
    matched_session: str
    email_body: str
    timestamp: str
    status: str
