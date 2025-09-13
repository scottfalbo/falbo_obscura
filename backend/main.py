from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app instance
app = FastAPI(
    title="Falbo Obscura API",
    description="Portfolio website backend API",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic health check endpoint
@app.get("/")
async def root():
    return {"message": "Falbo Obscura API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Run the app (for development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True  # Auto-reload on code changes
    )
