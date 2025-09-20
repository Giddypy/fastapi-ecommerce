import uvicorn
from app.app import app

if __name__ == "__main__":
    uvicorn.run("main:app", port="0.0.0.0", host=8007, reload=True, log_level="debug")