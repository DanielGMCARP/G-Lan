from rich.progress import Progress
import time
import random

with Progress() as progress:
    task = progress.add_task("[cyan]Descargando...", total=100)
    while not progress.finished:
        progress.update(task, advance=random.randint(1, 5))
        time.sleep(0.3)
