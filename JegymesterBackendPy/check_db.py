from app import create_app
from app.extensions import db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    print("Tables found in database:")
    for table_name in inspector.get_table_names():
        print(f" - {table_name}")