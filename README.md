# Arkanoid
Игра, где нужно ломать препятствия на нескольких уровнях
## Алгоритмы
- Функция создания пароля
  ```python
  def create_password():
    password_data = string.ascii_letters + string.digits
    return ''.join(random.sample(password_data, k=8))
  ```
  Здесь происходит то-то то-то
- Функция создания логина
  ```python
  def create_login(full_name):
    surname, name, smth = full_name.split()
    login = surname + '_' + name[0] + smth[0]
    return login
  ```
  Возвращает логин
- Используемые библиотеки
  ```python
  import csv
  import random
  import string
  ```
  Для того, для, того, для того
