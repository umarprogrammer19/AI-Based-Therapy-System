from fastapi import FastAPI
from . import chat_router, upload_router, admin_router

app = FastAPI(title="Ketamine AI & Learning System", version="1.0.0")

# Include routers
app.include_router(chat_router.router, prefix="/api", tags=["chat"])
app.include_router(upload_router.router, prefix="/api", tags=["upload"])
app.include_router(admin_router.router, prefix="/api", tags=["admin"])

@app.get("/")
def read_root():
    return {"message": "Ketamine AI & Learning System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)