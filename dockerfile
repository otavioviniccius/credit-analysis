FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
# ou requirements.txt
# COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir fastapi uvicorn[standard] joblib scikit-learn pandas numpy pydantic

COPY src /app/src
COPY data/models /app/data/models

ENV PYTHONPATH=/app/src

EXPOSE 8000
CMD ["uvicorn", "credit.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
