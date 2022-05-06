import pandas as pandas
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, SQLModel, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    df = pandas.read_csv("https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv")
    df.to_sql("Question", engine,if_exists="append")
