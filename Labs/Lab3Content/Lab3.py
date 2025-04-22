import configparser
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import socket


def create_config():
    """Создание и сохранение конфигурационного файла с расширенными настройками"""
    config = configparser.ConfigParser(allow_no_value=True)

    # Добавляем комментарии в виде ключей без значений
    config['DEFAULT'] = {
        '; Main server settings': None,
        'Server': 'localhost',
        'Port': '8080',
        'Timeout': '30',
        'Max_Connections': '100',
        'SSL_Enabled': 'True',
        '; Cache settings': None,
        'Cache_Size': '256',
        'Cache_TTL': '3600'
    }

    config['DATABASE'] = {
        '; Database connection settings': None,
        'User': 'admin',
        'Password': 'password123',
        'Host': '127.0.0.1',
        'Port': '5432',
        'Database': 'mydatabase',
        'Pool_Size': '10',
        'Connection_Timeout': '5'
    }

    config['LOGGING'] = {
        '; Logging settings': None,
        'Level': 'INFO',
        'File': '/var/log/app.log',
        'Max_Size': '10',
        'Backup_Count': '5'
    }
    # Запись конфигурации в файл
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    return config


def display_config(config):
    """Отображение конфигурации с использованием Rich"""
    console = Console()

    # Заголовок и информация о файле
    console.rule("[bold blue]Конфигурация приложения[/bold blue]")
    console.print(f"Файл конфигурации: [bold]config.ini[/bold]")
    console.print(f"Количество секций: [bold]{len(config.sections())}[/bold]\n")

    # Таблица с основными настройками
    table = Table(title="Основные настройки (DEFAULT)", show_header=True, header_style="bold magenta")
    table.add_column("Параметр", style="dim")
    table.add_column("Значение")

    for key, value in config['DEFAULT'].items():
        if not key.startswith(';'):  # Пропускаем комментарии
            table.add_row(key, value)

    console.print(table)

    # Таблица с настройками БД
    db_table = Table(title="Настройки базы данных", show_header=True, header_style="bold green")
    db_table.add_column("Параметр", style="dim")
    db_table.add_column("Значение")

    for key, value in config['DATABASE'].items():
        if not key.startswith(';'):
            # Маскируем пароль для безопасности
            db_table.add_row(key, value if key != 'Password' else '*******')

    console.print(db_table)

    # Проверка доступности сервера
    try:
        ip = socket.gethostbyname(config['DEFAULT']['Server'])
        console.print(f"\n[bold]Сетевая информация:[/bold] Сервер [green]{config['DEFAULT']['Server']}[/green] "
                      f"({ip}) порт [green]{config['DEFAULT']['Port']}[/green]")
    except socket.gaierror:
        console.print("\n[red]Ошибка![/red] Не удалось разрешить имя сервера", style="bold")


def main():
    # Создаем и загружаем конфигурацию
    config = create_config()
    config.read('config.ini')

    # Отображаем конфигурацию
    display_config(config)

    # Пример использования параметров
    ssl_enabled = config['DEFAULT'].getboolean('SSL_Enabled')
    rprint(f"\n[bold]Пример использования:[/bold] SSL {'включен' if ssl_enabled else 'выключен'}")

if __name__ == "__main__":
    main()