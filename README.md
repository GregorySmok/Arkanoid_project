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
