from desktop.application_runner import DesktopApplicationRunner
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    DesktopApplicationRunner(os.getenv("API_URL")).run()


if __name__ == "__main__":
    main()
