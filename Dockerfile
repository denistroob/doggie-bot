FROM python:latest
WORKDIR /doggie-bot
COPY main.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python3","-u","main.py"]
