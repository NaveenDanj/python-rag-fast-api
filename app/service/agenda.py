import logging
from pathlib import Path

logger = logging.getLogger("app")


class AgendaManager:
    
    def __init__(self, agenda_file_path: str):
        self.sessions = self._load_sessions(agenda_file_path)
    
    def _load_sessions(self, file_path: str):
        sessions = []
        
        try:
            path = Path(file_path)
            if not path.exists():
                logger.warning(f"Agenda file not found: {file_path}")
                return sessions
            
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            session_blocks = content.split("[SESSION_")
            
            for block in session_blocks[1:]:
                lines = block.strip().split("\n")
                session_data = {}
                
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if key == "time":
                            session_data["time"] = value
                        elif key == "title":
                            session_data["name"] = value
                        elif key == "speaker":
                            session_data["speaker"] = value
                        elif key == "focus keywords":
                            session_data["keywords"] = value
                        elif key == "description":
                            session_data["description"] = value
                
                if "name" in session_data and "time" in session_data:
                    sessions.append({
                        "name": session_data.get("name", ""),
                        "time": session_data.get("time", ""),
                        "speaker": session_data.get("speaker", ""),
                        "description": session_data.get("description", ""),
                        "keywords": session_data.get("keywords", ""),
                    })
            
            logger.info(f"Loaded {len(sessions)} sessions")
        
        except Exception as e:
            logger.error(f"Error loading agenda: {e}")
        
        return sessions
    
    def get_all_sessions(self):
        return self.sessions
