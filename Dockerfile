FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates ./templates
COPY documents ./documents

RUN echo "ctfuser:x:1337:1337:FLAG{lfi_path_traversal_success_template}:/home/ctfuser:/bin/bash" >> /etc/passwd

EXPOSE 5000

CMD ["python", "app.py"]