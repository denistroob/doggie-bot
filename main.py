import time
import requests
import re
import mysql.connector
import os
from mailjet_rest import Client

# Wait for DB to be up (that's gross I know) 
time.sleep(20)

# Mysql Config
db = mysql.connector.connect(
  user="root",
  password="root",
  host="doggies-db",
  port="3306",
  database="doggies"
)
cursor = db.cursor()

# Mailjet config

mailjet = Client(auth=(os.environ['MAILJET_API_KEY'], os.environ['MAILJET_API_SECRET']), version='v3.1')

def dog_exists(dog_id):
  sql = "SELECT * FROM links WHERE dog_id = %s"
  values = (dog_id, )
  cursor.execute(sql, values)
  result = cursor.fetchall()
  if result:
    for x in result:
      print('Dog found in DB: ', x)
    return(True)
  return False

def add_new_dog(dog_id, title, url):
  sql = "INSERT INTO links (dog_id, url, title) VALUES (%s, %s, %s)"
  values = (dog_id, title, url)
  cursor.execute(sql, values)
  print('Dog added to DB: ', values)
  db.commit()

def notify(dog_id, title, url):
  data = {
    'Messages': [
      {
        'From': {
          'Email': os.environ['EMAIL'],
          'Name': os.environ['NAME']
        },
        'To': [
          {
            'Email': os.environ['EMAIL'],
            'Name': os.environ['NAME']
          }
        ],
        'Subject': 'New dog - ' + dog_id,
        'HTMLPart': '<h3>New dog on dogs.ie!</h3>' +
                    '<p>Title: ' + title + '</p>' +
                    '<p>Link: <a href=' + url + '>' + url + '</a></p>',
        'CustomID': dog_id
      }
    ]
  }
  result = mailjet.send.create(data=data)
  print('Notification Email Sent.')

while True:
  # Links for each dogs are formatted like this:
  # <td ><a href="https://dogs.ie/dog/880589/" title="Golden Retrievers     0876538908 for sale.">
    
  for search_url in os.environ['SEARCH_URLS'].split(','):
    print('\nScanning url: ', search_url)
    r = requests.get(search_url)
    dogs = re.findall(r"(?<=<td ><a href=\")(.*)(?=\")", r.text)

    for elem in dogs:
      elem = elem.split('\"')
      url = elem[0]
      title = elem[2]
      dog_id = url[20:-1]
      print('\nDog ID:', dog_id)
      print('Title:', title)
      print('URL:', url)

      if not dog_exists(dog_id):
        add_new_dog(dog_id, title, url)
        notify(dog_id, title, url)

  print('\nNext Search in 1 min.')
  time.sleep(60)
