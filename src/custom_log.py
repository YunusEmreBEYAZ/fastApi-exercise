from datetime import datetime

def log(time, tag="", message=""):
  time = str(datetime.now())
  with open("log.txt", "w+") as log:
    log.write(f"{time}: {tag}: {message}\n")


def custom_call_log(message:str):

  log("API called", message)