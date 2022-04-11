FROM python:3

WORKDIR /app

ENV FLASK_APP=web
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/src

CMD [ "flask", "run" ]