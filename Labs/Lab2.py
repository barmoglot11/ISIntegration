from rich import print
from rich.json import JSON
import json

data = {
    "имя": "Алексей",
    "возраст": 28,
    "активен": True,
    "навыки": ["Python", "SQL", "Docker"],
    "метаданные": {
        "дата_регистрации": "2023-01-15",
        "премиум": False
    }
}

print("[bold magenta]Исходный словарь:[/]")
print(JSON.from_data(data))

print("\n[bold yellow]Результат сериализации JSON:[/]")
print(JSON(json.dumps(data)))
