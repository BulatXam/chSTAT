from sqlalchemy import create_engine

TOKEN = "2120001268:AAEl-aoSg7TiZjHvYZ6XrtS-sl5FxFN_Z2Y"
DB_ENGINE = create_engine('sqlite:///db.sqlite3', echo=False)
