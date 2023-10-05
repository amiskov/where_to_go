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
runprod:
	$(MAKE) mig && \
	$(MAKE) collectstatic && \
	rm -f gunicorn_error.log && \
	poetry run gunicorn where_to_go.wsgi \
		--error-logfile gunicorn_error.log \
		-b 0.0.0.0:5001 \
		--pid gunicorn.pid \
		--daemon
killprod:
	kill `cat gunicorn.pid`
