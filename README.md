# Django_stripe_service

#### Веб-сервис, позволяющий оплачивать выбранные товары через платежную систему Stripe.
___
## Site page examples

#### Главная страница:
![img.png](djstrippr/static/img.png)

#### Выбор товара для оплаты:

![img_1.png](djstrippr/static/img_1.png) 

#### Корзина с выбранными товарами, учитывающая налогообложение и скидочные купоны:

![img_2.png](djstrippr/static/img_2.png)

#### Пример отображения формы оплаты единичного товара и списка выбранных товаров:

![img_3.png](djstrippr/static/img_3.png)
![img_4.png](djstrippr/static/img_4.png)

#### Панель администратора:

![img_5.png](djstrippr/static/img_5.png)

___

## Installation

#### Заполните файл .env в соотвествии с образцом по адресу:

```bash
djstrippr/djstrippr/.env
```

#### Выполните следующую команду:

```bash
docker-compose up 
```

#### Войдите в контейнер приложения:

```bash
docker-compose exec web sh
```

#### Создайте и выполните миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Создайте суперпользователя:
```bash
python manage.py createsuperuser
```
___

#### Заполните данные через панель администратора и приступайте к использованию!

___
## Published version
[Django-stripe-service](http://pashokpl.beget.tech/)
