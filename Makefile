run:
	poetry run python manage.py runserver
mig:
	poetry run python manage.py migrate
mkmig:
	poetry run python manage.py makemigrations
shell:
	poetry run python manage.py shell_plus --ipython
collectstatic:
	poetry run python manage.py collectstatic --no-input
load:
	poetry run python manage.py load_place $$(cat places.txt)
isort:
	poetry run isort . --skip-glob **/migrations
