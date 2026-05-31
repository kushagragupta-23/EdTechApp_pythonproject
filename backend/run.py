import uvicorn
import argparse
from app.config import settings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run EduVerse Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host IP")
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    args = parser.parse_args()

    # In development, default to reload
    reload = args.reload or settings.DEBUG

    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=reload)
