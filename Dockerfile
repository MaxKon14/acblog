FROM python:3.12
LABEL authors="konovalov_maksim"

COPY . /app
WORKDIR /app
RUN pip install uv
RUN uv venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
RUN uv pip sync uv.lock
WORKDIR /app/blog/
ENTRYPOINT ["/app/.venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
