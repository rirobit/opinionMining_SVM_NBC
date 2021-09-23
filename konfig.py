import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="4KulupaSand!",
  database="sentista")

curl = mydb.cursor()