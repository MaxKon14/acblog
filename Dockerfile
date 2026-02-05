FROM python:3.12
LABEL authors="konovalov_maksim"

COPY . /app
WORKDIR /app
RUN pip install uv
RUN uv venv
RUN ls -a
RUN pip install uv
RUN uv pip sync uv.lock
RUN ls -a
WORKDIR /app/blog/
ENTRYPOINT ["/app/.venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
