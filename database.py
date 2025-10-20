from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql://postgres:1234567890@localhost:5432/testserver"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)