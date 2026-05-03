from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql://admin:password@localhost:5432/mydb"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, bind=engine)