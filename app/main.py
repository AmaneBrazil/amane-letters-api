from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from uuid import UUID
from exceptions.BusinessException import BusinessException
from typing import Optional

from db import SessionLocal, engine, Base, get_db
import schemas
import service

from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, e: BusinessException):
    return JSONResponse(
        status_code=e.code,
        content={"error": e.message}
    )

@app.post("/letters", response_model=schemas.LetterResponse)
def create_letter(letter: schemas.LetterCreate, db: Session = Depends(get_db)):
    return service.create_letter(db, letter)

@app.get("/letters", response_model=List[schemas.LetterResponse])
def get_public_letters(db: Session = Depends(get_db)):
    return service.get_public_letters(db)

@app.post("/letters/{letter_id}/get", response_model=schemas.LetterResponse)
def get_letter(letter_id: UUID, access: Optional[schemas.LetterAccess] = None, db: Session = Depends(get_db)):
    return service.get_letter(db, letter_id, None if access is None else access.password)

@app.get("/")
def root():
    return {"message": "A API está online"}