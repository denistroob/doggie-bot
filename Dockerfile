FROM python:latest
WORKDIR /doggie-bot
COPY script.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python3","-u","script.py"]
