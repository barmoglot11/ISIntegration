import csv
from datetime import datetime
from rich.console import Console
from rich.table import Table
import random
import os

# Настройки консоли
console = Console()


def generate_rich_data():
    """Генерация насыщенных данных о пользователях"""
    names = ['Алексей', 'Мария', 'Иван', 'Ольга', 'Дмитрий', 'Анна']
    lastNames = ['Иванов', 'Петрова', 'Сидоров', 'Смирнова', 'Кузнецов']
    cities = ['Москва', 'Санкт-Петербург', 'Екатеринбург', 'Новосибирск', 'Казань', 'Сочи']
    professions = ['Разработчик', 'Дизайнер', 'Менеджер', 'Аналитик', 'Маркетолог']
    interests = ['спорт', 'музыка', 'кино', 'путешествия', 'программирование', 'книги']

    data = []
    # Заголовки таблицы
    data.append([
        'ID', 'Имя', 'Фамилия', 'Возраст', 'Город',
        'Профессия', 'Зарплата', 'Дата регистрации',
        'Премиум статус', 'Рейтинг'
    ])

    # Генерация данных пользователей
    for i in range(1, 21):
        first_name = random.choice(names)
        last_name = random.choice(lastNames)
        age = random.randint(20, 45)
        city = random.choice(cities)
        profession = random.choice(professions)
        salary = random.randint(50000, 200000)
        reg_date = datetime.now().strftime('%Y-%m-%d')
        premium = random.choice([True, False])
        rating = round(random.uniform(3.5, 5.0), 1)

        data.append([
            i, first_name, last_name, age, city,
            profession, f"{salary:,}", reg_date,
            "Да" if premium else "Нет", rating
        ])

    return data


def save_to_csv(data, filename):
    """Сохранение данных в CSV файл"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    console.print(f"[green]✓ Данные успешно сохранены в файл {filename}[/green]")


def display_data(data):
    """Красивый вывод данных с использованием Rich"""
    table = Table(title="Данные пользователей", show_header=True, header_style="bold magenta")

    # Добавляем колонки
    for header in data[0]:
        table.add_column(header, style="dim")

    # Добавляем строки (пропускаем заголовки)
    for row in data[1:11]:  # Выводим только первые 10 записей
        # Форматируем цветами
        styled_row = []
        for i, item in enumerate(row):
            # Преобразуем все элементы в строки
            item_str = str(item)
            if i == 3:  # Возраст
                if int(item) > 35:
                    styled_row.append(f"[red]{item_str}[/red]")
                else:
                    styled_row.append(f"[green]{item_str}[/green]")
            elif i == 6:  # Зарплата
                styled_row.append(f"[yellow]{item_str}[/yellow]")
            elif i == 9:  # Рейтинг
                if float(item) >= 4.5:
                    styled_row.append(f"[bold green]{item_str}[/bold green]")
                else:
                    styled_row.append(item_str)
            else:
                styled_row.append(item_str)

        table.add_row(*styled_row)

    console.print(table)

    # Статистика
    total_users = len(data) - 1  # Минус заголовок
    premium_count = sum(1 for row in data[1:] if row[8] == "Да")
    avg_salary = sum(int(row[6].replace(',', '')) for row in data[1:]) / total_users

    console.print(f"\n[b]Статистика:[/b]")
    console.print(f"Всего пользователей: [bold]{total_users}[/bold]")
    console.print(f"Премиум пользователей: [bold]{premium_count}[/bold]")
    console.print(f"Средняя зарплата: [bold]{avg_salary:,.2f} руб.[/bold]")

def main():
    # Генерация данных
    users_data = generate_rich_data()

    # Сохранение в файл
    save_to_csv(users_data, "users_data.csv")

    # Вывод данных
    console.rule("[bold blue]Анализ данных пользователей[/bold blue]")
    display_data(users_data)

    # Информация о файле
    file_size = os.path.getsize("users_data.csv") / 1024
    console.print(f"\n[i]Размер файла: {file_size:.2f} KB[/i]")


if __name__ == "__main__":
    main()