""" Main module """

from command_line import start
from database import Citations

def main():
    ''' Main function '''
    db = Citations()
    start(db)

if __name__ == "__main__":
    main()
