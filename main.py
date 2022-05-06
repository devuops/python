import logging
import secrets
from random import choice
from typing import List, Optional

import sqlmodel
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlmodel import SQLModel, Session, select
from starlette import status

import db

app = FastAPI()
log = logging.getLogger("fastapi")
security = HTTPBasic()


class Question(SQLModel, table=True):
    index: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    question: str = Field("", title="question à poser", min_length=1, example="Que signifie le sigle No-SQL")
    subject: str = Field("", title="la categorie", min_length=1, example="BDD")
    correct: str = Field("", title="la réponse juste", min_length=1, example="A")
    use: str = Field("", title="le type de test", min_length=1, example="Test de positionnement")
    responseA: str = Field("", title="ReponseA", min_length=1, example="Pas seulement SQL")
    responseB: str = Field("", title="ReponseB", min_length=1, example="Pas de SQL")
    responseC: str = Field("", title="ReponseC", min_length=1, example="Pas tout SQL")
    responseD: Optional[str] = Field(None, title="ReponseD", min_length=1, example="BDD")
    remark: Optional[str] = Field(None, title="ReponseD", min_length=1, example="BDD")


class QuestionaireRequest(BaseModel):
    subjects: List[str] = Field("", title="la categorie", min_items=1, example=['BDD', 'Python'])
    use: str = Field("", title="le type de test", min_length=1, example="Test de positionnement")


def check_user(credentials: HTTPBasicCredentials, it):
    log.info(it['user'])
    log.info(credentials.username)
    return (secrets.compare_digest(credentials.username, it['user']) and secrets.compare_digest(
        credentials.password, it['password']))


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    users_password = [{"user": "alice", "password": "wonderland"}, {"user": "bob", "password": "builder"},
                      {"user": "clementine", "password": "mandarine"}, {"user": "admin", "password": "4dm1N"}]
    users = list(filter(lambda it: check_user(credentials=credentials, it=it), users_password))
    if len(users) != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="utilisateur inconnu",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def get_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "4dm1N")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="vous devez etre admin pour créer une question",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def get_session():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.on_event("startup")
def on_startup():
    db.init_db()


@app.post("/question")
async def create_question(request: Question, username: str = Depends(get_admin)):
    with Session(db.engine) as session:
        if username == "admin":
            session.add(request)
            session.commit()
            session.refresh(request)
            return request
    return ""


@app.post("/questionnaire", response_model=List[Question])
async def generate_questionnaire(request: QuestionaireRequest,
                                 username: str = Depends(get_current_username)):
    log.info(f"{username} a demandé un nouveau questionnaire")
    limit = choice([5, 10, 20])
    with Session(db.engine) as session:
        result = session.query(Question).where(
            Question.use == request.use).where(Question.subject.in_(request.subjects)).order_by(
            text('Random()')).limit(limit).all()
        return result


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
