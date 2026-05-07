from datetime import datetime
from colorama import  Fore


def displayLog(message: str):
  """Função para mostrar logs com timestamp."""
  date = datetime.now()
  print(Fore.BLUE + f'[{date}]: {message}')