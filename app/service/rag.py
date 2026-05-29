import logging
from openai import OpenAI
from app.utils.utils import cosine_similarity

logger = logging.getLogger("app")


class RAGMatcher:
    
    def __init__(self, client: OpenAI, sessions: list[dict]):
        self.client = client
        self.sessions = sessions
        self.session_embeddings = {}
    
    async def get_embedding(self, text: str):
        try:
            response = self.client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            print("Embedding response:", response)
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error getting embedding: {e}")
            raise
    
    async def match_session(self, visitor_focus: str):
        if not self.sessions:
            return None
        
        try:
            focus_embedding = await self.get_embedding(visitor_focus)
            
            best_match = None
            best_similarity = -1
            
            for session in self.sessions:
                session_text = f"{session['name']}. {session['keywords']}. {session['description']}"
                
                if session["name"] not in self.session_embeddings:
                    self.session_embeddings[session["name"]] = await self.get_embedding(session_text)
                
                session_embedding = self.session_embeddings[session["name"]]
                similarity = cosine_similarity(focus_embedding, session_embedding)
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = session
            
            if best_match:
                logger.info(
                    f"Best match: {best_match['name']} (similarity: {best_similarity:.3f})"
                )
            
            return best_match
        
        except Exception as e:
            logger.error(f"Error matching session: {e}")
            return self.sessions[0] if self.sessions else None
