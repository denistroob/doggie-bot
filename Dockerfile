FROM python:3
WORKDIR /doggie-bot
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python3","-u","main.py"]
