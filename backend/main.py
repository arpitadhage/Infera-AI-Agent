from fastapi import FastAPI

app = FastAPI(
    title="Infera AI Agent",
    version="1.0.0"
)


@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "Infera AI Agent Backend"
    }