FROM python:3.12.7

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh
ENTRYPOINT "/app/startup.sh"
