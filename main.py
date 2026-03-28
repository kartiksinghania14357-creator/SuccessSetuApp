from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
import google.generativeai as genai

# Database tables create karna
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Advanced CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini API Configuration
genai.configure(api_key="AIzaSyACRdbpVSKpAWHOPCoDncU5Hhvcd6_0oXY")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Success Setu Backend is Running!"}

# Priya AI Chat API (Naam remove kar diya gaya hai)
@app.post("/ask_priya/")
async def ask_priya(query: str):
    try:
        # gemini-1.5-flash zyada stable hai
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # System Instruction: Ab ye kisi ka naam nahi legi
        prompt = (
            f"Tumhara naam Priya AI hai. Tum 'Success Setu' app ki expert mentor ho. "
            f"Tum sabhi students ki help karti ho. "
            f"Hamesha friendly English aur Hinglish mein baat karo. "
            f"Kisi ka personal naam mat lo. "
            f"Student ka doubt: {query}"
        )
        
        response = model.generate_content(prompt)
        
        if not response.text:
            return {"reply": "Main abhi iska jawab nahi dhoond pa rahi hoon. Kya aap dobara puch sakte hain?"}
            
        return {"reply": response.text}
    except Exception as e:
        # Terminal mein error check karne ke liye
        print(f"ERROR: {e}") 
        return {"reply": "Maaf karna ji, thoda technical issue hai. Kya tum phir se puch sakte ho?"}

@app.post("/register/")
def register_user(name: str, mobile: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.mobile == mobile).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Mobile already registered!")
    
    new_user = models.User(full_name=name, mobile=mobile)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "status": "Success", 
        "user_id": new_user.id, 
        "welcome_msg": f"Welcome to Success Setu! Main Priya AI tumhari madad ke liye taiyar hoon."
    }