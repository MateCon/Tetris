from desktop.application_runner import DesktopApplicationRunner
from dotenv import load_dotenv
import os
from pathlib import Path
import sys

if getattr(sys, "frozen", False):
    base_dir = Path(sys._MEIPASS)
else:
    base_dir = Path(__file__).resolve().parents[1]

load_dotenv(base_dir / ".env")

def main():
    DesktopApplicationRunner(os.getenv("API_URL")).run()


if __name__ == "__main__":
    main()
