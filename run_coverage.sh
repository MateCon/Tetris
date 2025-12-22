source venv_testing/bin/activate
coverage run -m pytest
coverage report
coverage html
open htmlcov/index.html
deactivate
