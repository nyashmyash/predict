from pydantic import BaseModel


# Модель для создания клиента
class ClientCreate(BaseModel):
    name: str


# Модель для получения топ3 продуктов
class ClientPredict(BaseModel):
    name: str


# Модель рекомендаций
class Predict(BaseModel):
    prod_name: str
    client_id: int


# Модель для создания продукта
class ProductCreate(BaseModel):
    name: str
    client_id: int
