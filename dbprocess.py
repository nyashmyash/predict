from sqlalchemy.sql import func
from dbmodels import *

import pickle


class DBProcess:
    # Функция для получения пользователя из базы данных по имени

    @staticmethod
    def save_clients(db, clients_file: str):
        with open(clients_file, 'wb') as f:
            clients = []
            for client in db.query(Client).all():
                clients.append({"name": client.name})
            pickle.dump(clients, f)

    @staticmethod
    def save_products(db, products_file: str):
        with open(products_file, 'wb') as f:
            products = []
            for product in db.query(Product).all():
                products.append({"name": product.name})
            pickle.dump(products, f)

    @staticmethod
    def save_purchase(db, purchase_file: str):
        with open(purchase_file, 'wb') as f:
            purchases = []
            for purchase in db.query(Purchase).all():
                prod = DBProcess.get_product(db, prod_id=purchase.product_id)
                client = DBProcess.get_client(db, client_id=purchase.client_id)
                purchases.append({"product": prod.name, "client": client.name})
            pickle.dump(purchases, f)

    @staticmethod
    def load_clients(db, clients_file):
        with open(clients_file, 'rb') as f:
            data_clients = pickle.load(f)
            for client in data_clients:
                new_client = Client(name=client['name'])
                db.add(new_client)
            db.commit()

    @staticmethod
    def load_products(db, products_file):
        with open(products_file, 'rb') as f:
            data_products = pickle.load(f)
            for product in data_products:
                new_product = Product(name=product['name'])
                db.add(new_product)
            db.commit()

    @staticmethod
    def load_purchase(db, purchase_file):
        with open(purchase_file, 'rb') as f:
            data_purchase = pickle.load(f)
            for purchase in data_purchase:
                client = DBProcess.get_client(db, name=purchase['client'])
                product = DBProcess.get_product(db, name=purchase['product'])
                if client and product:
                    new_purchase = Purchase(client_id=client.id, product_id=product.id)
                    db.add(new_purchase)
            db.commit()

    @staticmethod
    def create_client(db, name: str) -> Client:
        new_client = Client(name=name)
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client

    @staticmethod
    def create_product(db, name: str) -> Product:
        new_product = Product(name=name)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    @staticmethod
    def get_client(db, client_id: str = "", name: str = "") -> Client:
        if name:
            return db.query(Client).filter(Client.name == name).first()
        client = db.query(Client).filter(Client.id == int(client_id)).first()
        return client

    @staticmethod
    def get_product(db, prod_id: str = "", name: str = "") -> Product:
        if name:
            return db.query(Product).filter(Product.name == name).first()
        product = db.query(Product).filter(Product.id == int(prod_id)).first()
        return product

    @staticmethod
    def predict(db, client_id: int):
        # Здесь можно добавить логику для получения топ 3 продуктов по моделям рекомендаций
        top_products_for_client = db.query(Product.name, func.count(Purchase.product_id).label('total_purchases')). \
            join(Purchase). \
            filter(Purchase.client_id == client_id). \
            group_by(Product.name). \
            order_by(func.count(Purchase.product_id).desc()). \
            limit(3).all()

        return top_products_for_client
