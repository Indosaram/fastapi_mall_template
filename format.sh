export PIPENV_IGNORE_VIRTUALENVS=1

pipenv run isort .
pipenv run black -l 80 -t py38 --skip-string-normalization .