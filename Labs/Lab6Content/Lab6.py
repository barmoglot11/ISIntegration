import yaml
from datetime import datetime
from rich.console import Console
from rich.table import Table
import random
import os

# Настройка консоли для красивого вывода
console = Console()

def generate_rich_data():
    """Генерация насыщенных данных пользователей"""
    names = ['Алексей', 'Мария', 'Иван', 'Ольга', 'Дмитрий', 'Анна']
    lastNames = ['Иванов', 'Петрова', 'Сидоров', 'Смирнова', 'Кузнецов']
    cities = ['Москва', 'Санкт-Петербург', 'Екатеринбург', 'Новосибирск', 'Казань', 'Сочи']
    professions = ['Разработчик', 'Дизайнер', 'Менеджер', 'Аналитик', 'Маркетолог']
    interests = ['спорт', 'музыка', 'кино', 'путешествия', 'программирование', 'книги']

    users = []
    for i in range(1, 11):  # Генерируем 10 пользователей
        user = {
            'id': i,
            'name': random.choice(names),
            'last_name': random.choice(lastNames),
            'age': random.randint(20, 45),
            'city': random.choice(cities),
            'profession': random.choice(professions),
            'salary': random.randint(50000, 200000),
            'registration_date': datetime.now().strftime('%Y-%m-%d'),
            'premium': random.choice([True, False]),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'interests': random.sample(interests, k=random.randint(1, 3))
        }
        users.append(user)

    return {
        'metadata': {
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_users': len(users),
            'file_version': '1.0'
        },
        'users': users
    }


def save_to_yaml(data, filename):
    """Сохранение данных в YAML файл"""
    with open(filename, 'w', encoding='utf-8') as yamlfile:
        yaml.dump(data, yamlfile, allow_unicode=True, sort_keys=False)
    console.print(f"[green]✓ Данные успешно сохранены в файл {filename}[/green]")


def display_users(data):
    """Красивый вывод данных пользователей"""
    table = Table(title="Данные пользователей", show_header=True, header_style="bold magenta")

    # Добавляем колонки
    table.add_column("ID", style="dim")
    table.add_column("Имя")
    table.add_column("Фамилия")
    table.add_column("Возраст")
    table.add_column("Город")
    table.add_column("Профессия")
    table.add_column("Зарплата")
    table.add_column("Рейтинг")
    table.add_column("Премиум")

    # Добавляем строки с данными
    for user in data['users']:
        # Форматируем значения для красивого вывода
        age = f"[red]{user['age']}[/red]" if user['age'] > 35 else f"[green]{user['age']}[/green]"
        salary = f"[yellow]{user['salary']:,} руб.[/yellow]"
        rating = f"[bold green]{user['rating']}[/bold green]" if user['rating'] >= 4.5 else str(user['rating'])
        premium = "✅" if user['premium'] else "❌"

        table.add_row(
            str(user['id']),
            user['name'],
            user['last_name'],
            age,
            user['city'],
            user['profession'],
            salary,
            rating,
            premium
        )

    console.print(table)

    # Выводим статистику
    console.print(f"\n[b]Метаданные:[/b]")
    console.print(f"Всего пользователей: [bold]{data['metadata']['total_users']}[/bold]")
    console.print(f"Дата генерации: [bold]{data['metadata']['generated_at']}[/bold]")

    premium_count = sum(1 for user in data['users'] if user['premium'])
    console.print(f"Премиум пользователей: [bold]{premium_count}[/bold]")


def main():
    # Генерация данных
    users_data = generate_rich_data()

    # Сохранение в файл
    save_to_yaml(users_data, "users_data.yaml")

    # Вывод информации о файле
    file_size = os.path.getsize("users_data.yaml") / 1024
    console.rule("[bold blue]Анализ данных пользователей[/bold blue]")
    console.print(f"Размер файла: [i]{file_size:.2f} KB[/i]\n")

    # Чтение и вывод данных
    with open('users_data.yaml', 'r', encoding='utf-8') as yamlfile:
        loaded_data = yaml.safe_load(yamlfile)

    display_users(loaded_data)


if __name__ == "__main__":
    main()