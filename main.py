import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

# Create FastAPI app
app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request model
class QuestionRequest(BaseModel):
    question: str


# Home API
@app.get("/")
def home():
    return {
        "message": "Welcome to EduGenie - Google Gemini Powered Learning Assistant"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "running",
        "application": "EduGenie"
    }


# Ask Gemini
@app.post("/ask")
def ask_gemini(request: QuestionRequest):

    if not request.question.strip():
        return {
            "success": False,
            "message": "Please enter a question."
        }

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
You are EduGenie, an intelligent learning assistant.

Help the student understand the topic clearly.

Question:
{request.question}

Give:
1. Simple explanation
2. Important points
3. Example if needed
4. Short summary
"""
        )

        return {
            "success": True,
            "question": request.question,
            "answer": response.text
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Unable to generate response.",
            "error": str(e)
        }


# Run with:
# uvicorn main:app --reload