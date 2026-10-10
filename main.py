from reader import *
from my_bot import *
import sys

def has_file():
    if len(sys.argv) == 1:
        print("Usage: python3 main.py <path_to_file>")
        sys.exit(1)

def main(attachment):
    has_file()
    #csv_file = get_csv(sys.argv[1])
    template_write(attachment)

