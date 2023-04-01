install:
		poetry install
lint:
		poetry run flake8 task_manager
freeze:
		poetry run pip --disable-pip-version-check list --format=freeze > requirements.txt
migrations:
		poetry run python manage.py makemigrations
migrate:
		poetry run python manage.py migrate
dev:
		poetry run python manage.py runserver
ready_to_trans:
		poetry run django-admin makemessages --ignore="static" --ignore=".env" -l ru
translate:
		poetry run django-admin compilemessages
static:
		poetry run python manage.py collectstatic
test:
		poetry run python manage.py test -v 2 ./task_manager/tests/
test-coverage:
		poetry run coverage run manage.py test ./task_manager/tests/
		poetry run coverage report --omit=*/tests/*,*/migrations/*
		poetry run coverage xml --omit=*/tests/*,*/migrations/*



