from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    mobile = Column(String, unique=True, index=True)
    password = Column(String) # For secure login
    is_admin = Column(Boolean, default=False) # Tumhe admin banane ke liye
    progress = Column(Integer, default=0) # 0 to 100% study progress