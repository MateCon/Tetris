source venv_desktop/bin/activate
pyinstaller --onefile --windowed --add-data "assets:assets" src/desktop_main.py
deactivate
