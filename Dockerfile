FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /

RUN pip install --no-cache-dir poetry==1.8.2 && poetry config virtualenvs.create false && poetry install

COPY /app entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]

CMD	gunicorn main:main_app \
	--workers 4 \
	--worker-class uvicorn.workers.UvicornWorker\
	--bind=0.0.0.0:8000 \
	--access-logfile - \
    --error-logfile - \
    --log-level debug \
    --capture-output
