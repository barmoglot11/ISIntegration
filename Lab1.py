from datetime import datetime
import requests
from rich import print_json
from rich.console import Console
from rich.panel import Panel

API_URL = "http://api.languagelayer.com/detect"
api_key = "a1127ac642daf589283974145fa12380"
text_to_check = "у вас это опциональный пункт, по результатам анализа предметной области, может быть построена модель текущей деятельности. Это актуально для тех, кто какие-то сайты/интернет-магазины разрабатывает или решения, которые автоматизируют какую-то деятельности. Для остальных достаточно п.4"  # Текст для проверки

params = {
    'access_key': api_key,
    'query': text_to_check,
    'format': 1
}
console = Console()
try:
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    console.print(Panel(
        f"[bold green]✅ Успешный запрос[/]✅\n"
        f"URL: [cyan]{API_URL}[/]\n"
        f"Статус: [blue]{response.status_code}[/]\n"
        f"Время: [yellow]{datetime.now().strftime('%H:%M:%S')}[/]",
        title="Информация о запросе"
    ))

    console.print("\n[bold]Тело ответа:[/]")
    print_json(data=data)

    if "pagination" in data:
        console.print(
            f"\n📄 Страница [bold]{data['pagination']['current_page']}[/] "
            f"из [bold]{data['pagination']['total_pages']}[/]",
            style="italic"
        )

except requests.exceptions.RequestException as e:
    console.print(f"[red]❌ Ошибка запроса:[/] {str(e)}", style="bold")
