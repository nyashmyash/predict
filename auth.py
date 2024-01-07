from passlib.context import CryptContext
from dbmodels import *

# Хэширование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Auth:
    # Функция для проверки пароля
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def add_user(db, username, plain_password):
        hashed_password = pwd_context.hash(plain_password)
        new_user = User(username=username, password=hashed_password)
        db.add(new_user)
        db.commit()

    @staticmethod
    def get_user(db, username: str):
        return db.query(User).filter(User.username == username).first()

    # Функция для аутентификации пользователя
    @staticmethod
    def authenticate_user(db, username: str, password: str):
        user = Auth.get_user(db, username)
        if not user:
            return False
        if not Auth.verify_password(password, user.password):
            return False
        return user
