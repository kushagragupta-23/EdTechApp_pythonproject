import os
import sys
import shutil

# Add backend directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

# Vercel's filesystem is read-only. We copy the seeded DB to /tmp to allow ephemeral reads/writes.
if os.environ.get("VERCEL"):
    db_source = "backend/edtech.db"
    db_dest = "/tmp/edtech.db"
    if not os.path.exists(db_dest) and os.path.exists(db_source):
        shutil.copy(db_source, db_dest)
    os.environ["DATABASE_URL"] = f"sqlite:///{db_dest}"

from app.main import app
