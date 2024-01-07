import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models import *
from dbprocess import *
from auth import *

app = FastAPI()

# Генерация токена для аутентификации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Роутинг для создания клиента
@app.post("/clients/")
def create_client(client: ClientCreate, current_user: str = Depends(oauth2_scheme)):
    return DBProcess.create_client(SessionLocal(), client.name)


# Роутинг для создания продукта
@app.post("/products/")
def create_product(product: ProductCreate, current_user: str = Depends(oauth2_scheme)):
    return DBProcess.create_product(SessionLocal(), product.name)


# Роутинг для получения топ 3 продуктов по моделям рекомендаций
# талица с client->product
@app.get("/predict/{client_id}")
def get_top_products(client_id: str, current_user: str = Depends(oauth2_scheme)):
    if DBProcess.get_client(SessionLocal(), client_id=client_id) is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return str(DBProcess.predict(SessionLocal(), int(client_id)))


# Роут для получения токена аутентификации
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = Auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
