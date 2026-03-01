from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Titanic Chat Agent API")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    query: str

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str
    chart: Optional[str] = None
    type: str

@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "Titanic Chat Agent API is running"}

@app.get("/dataset-info")
def dataset_info():
    """Get basic information about the Titanic dataset"""
    return agent.get_dataset_info()

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main chat endpoint that processes user queries about the Titanic dataset.
    Returns text answers and optional chart data.
    """
    try:
        if not request.query or request.query.strip() == "":
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Process the query using the agent
        result = agent.process_query(request.query)
        
        return ChatResponse(
            answer=result["answer"],
            chart=result.get("chart"),
            type=result["type"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
