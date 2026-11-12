# Imports
from datetime import datetime


def current_time_code():
  """
  Time code for mapping specific time with code.
  """
  now = datetime.now()
  return now.strftime("%d%m%y_%H%M%S")


def current_time():
  """ Get Current Time in {DD-MM-YY & HH:MM:SS}
  """
  now = datetime.now()
  return now.strftime("%d-%m-%y %H:%M:%S")


def log(message):
  """
  Use of this function for prints log in single line with
  current time when file/function executes
  """
  time = current_time()
  print(f"{time} {message}")

