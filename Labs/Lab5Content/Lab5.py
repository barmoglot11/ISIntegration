import json
from datetime import datetime
from tabulate import tabulate


def generate_rich_data():
    users = []
    for i in range(1, 11):
        user = {
            "id": i,
            "name": f"User_{i}",
            "email": f"user{i}@example.com",
            "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "activity": {
                "logins": i * 3,
                "last_login": datetime.now().strftime("%Y-%m-%d"),
                "premium": i % 3 == 0
            },
            "stats": {
                "posts": i * 2,
                "likes": i * 15,
                "comments": i * 5
            }
        }
        users.append(user)
    return users


def save_to_json(data, filename):
    """Сохранение данных в JSON файл с красивым форматированием"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def display_table(data):
    """Вывод данных в виде красивой таблицы"""
    table_data = []
    for user in data:
        table_data.append([
            user['id'],
            user['name'],
            user['email'],
            user['activity']['logins'],
            user['stats']['posts'],
            user['stats']['likes'],
            "✅" if user['activity']['premium'] else "❌"
        ])

    headers = ["ID", "Name", "Email", "Logins", "Posts", "Likes", "Premium"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


# Основной код
if __name__ == "__main__":
    # Генерация данных
    users_data = generate_rich_data()

    # Сохранение в файл
    save_to_json(users_data, "users_data.json")
    print("Данные успешно сохранены в файл 'users_data.json'")

    # Вывод в консоль
    print("\nТаблица пользователей:")
    display_table(users_data)