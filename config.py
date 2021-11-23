from sqlalchemy import create_engine

from pathlib import Path

TOKEN = "2120001268:AAEl-aoSg7TiZjHvYZ6XrtS-sl5FxFN_Z2Y"
# DB_ENGINE = create_engine('sqlite:///db.sqlite3', echo=False)

BASE_DIR = Path(__file__).parent

MEDIA_DIR = Path(BASE_DIR / "media")
