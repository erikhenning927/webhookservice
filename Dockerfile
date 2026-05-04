FROM python:3.11.3-slim-bullseye
LABEL maintainer="henningerik2@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_INDEX_URL=https://pypi.org/simple/
ENV PATH="/scripts:/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    unixodbc \
    unixodbc-dev \
    libffi-dev \
    libpq-dev \
    wget \
    curl \
    gnupg \
    bash && \
    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
    msodbcsql18 \
    mssql-tools18 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python -m venv /venv

WORKDIR /app
COPY . /app  
COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

ENV PYTHONPATH=/app
EXPOSE 5004

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5004"]