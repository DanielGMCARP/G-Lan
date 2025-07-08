from prompt_toolkit.shortcuts import ProgressBar
import time
import random

with ProgressBar(title="Descargando...") as pb:
    for i in pb(range(100)):
        time.sleep(random.uniform(0.05, 0.2))
