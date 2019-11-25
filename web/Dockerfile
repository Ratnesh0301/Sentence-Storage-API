FROM python:3
WORKDIR /Rest_API/web
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python","app.py"]