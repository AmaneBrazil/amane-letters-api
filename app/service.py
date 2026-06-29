from fastapi import HTTPException
from models import Letter
from db import SessionLocal
from utils.security import hash_password, verify_password
from exceptions.BusinessException import BusinessException

def create_letter(db, data):
    try:
        letter = Letter(
            title=data.title,
            content=data.content,
            style_theme=data.style_theme,
            image_url=data.image_url,
            password_hash=hash_password(data.password) if data.password else None
        )

        db.add(letter)
        db.commit()
        db.refresh(letter)

        letter.is_public = letter.password_hash is None

        return letter    
    except Exception as e:
        raise BusinessException(str(e), 500)

def get_letter(db, letter_id: int, password: str|None):
    letter = db.query(Letter).filter(Letter.id == letter_id).first()

    if not letter:
        raise HTTPException(
            status_code=404,
            detail="Letter não encontrada"
        )

    letter.is_public = letter.password_hash is None

    if not letter.is_public and password is None:
        raise BusinessException("É necessário enviar a senha dessa carta para a sua visualização.", 401)
    
    elif not letter.is_public and not verify_password(password, letter.password_hash):
        raise BusinessException("Senha de acesso incorreta.", 401)

    return letter

def get_public_letters(db):
    return db.query(Letter).filter(Letter.password_hash.is_(None)).all()