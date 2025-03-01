FROM python:3.11-slim-buster

WORKDIR /flask-crypto-app

COPY requirements.txt .

RUN pip install --no--cache--dir -r requirements.txt

COPY . .

ENV FLASK_APP=app
ENV FLASK_ENV=development

EXPOSE 5000

ENTRYPOINT [ "sh", "./entrypoint.sh"]

CMD ["python3", "run.py"]