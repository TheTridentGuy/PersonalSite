FROM python:3.13-slim
WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "10", "-b", "0.0.0.0:8000", "app:app"]