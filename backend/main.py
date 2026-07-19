from fastapi import FastAPI

app = FastAPI(
    title="Nexus API",
    description="AI-powered knowledge engine backend",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Nexus!"
    }

@app.get("/version")
def version():
    return {
        "version": "1.0.0"
    }

@app.get("/status")
def status():
    return {
        "status": "online"
    }