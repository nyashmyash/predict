from db.dbprocess import *
import pytest

# Создаем подключение к базе данных
engine = create_engine('sqlite:///:memory:', echo=True)
# Создаем таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Вставляем тестовые данные
client1 = Client(name='John')
client2 = Client(name='Alice')
product1 = Product(name='Apple')
product2 = Product(name='Banana')
product3 = Product(name='Orange')
session.add_all([client1, client2, product1, product2, product3])
session.commit()

purchase1 = Purchase(client_id=1, product_id=1)
purchase2 = Purchase(client_id=1, product_id=2)
purchase3 = Purchase(client_id=1, product_id=2)
purchase4 = Purchase(client_id=1, product_id=3)
purchase5 = Purchase(client_id=1, product_id=3)
purchase6 = Purchase(client_id=1, product_id=3)
purchase7 = Purchase(client_id=2, product_id=1)
session.add_all([purchase1, purchase2, purchase3, purchase4, purchase5, purchase6, purchase7])
session.commit()


# Тест для проверки правильности получения топ 3 продуктов для клиента
def test_top_products_for_client():
    # Вызываем функцию для получения топ 3 продуктов для клиента с ID=1
    top_products = DBProcess.predict(session, 1)
    # Проверяем ожидаемый результат
    assert len(top_products) == 3
    assert top_products[0][0] == 'Orange'  # Ожидаемый самый популярный продукт для клиента ID=1
    assert top_products[1][0] == 'Banana'  # Ожидаемый второй по популярности продукт для клиента ID=1
    assert top_products[2][0] == 'Apple'  # Ожидаемый третий по популярности продукт для клиента ID=1

    # Проверяем общее количество покупок каждого продукта
    assert top_products[0][1] == 3  # Ожидаемое общее количество покупок самого популярного продукта для клиента ID=1
    assert top_products[1][
               1] == 2  # Ожидаемое общее количество покупок второго по популярности продукта для клиента ID=1
    assert top_products[2][
               1] == 1  # Ожидаемое общее количество покупок третьего по популярности продукта для клиента ID=1


# Запускаем тесты
pytest.main([__file__])
