from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
import uvicorn

app = FastAPI(
    title="Smart Train Traffic Controller API",
    description="Railway Automation System for Delay Prediction and Rerouting",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Smart Train Traffic Controller API",
        "status": "active",
        "endpoints": ["/predict_delay", "/reroute", "/health"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "backend"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
