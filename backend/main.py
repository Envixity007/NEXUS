from fastapi import FastAPI
from routers import auth, users, admin



app = FastAPI(
    title="Nexus API",
    description="AI-powered knowledge engine backend",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)



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



