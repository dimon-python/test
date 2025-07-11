import mysql.connector

cnx = mysql.connector.connect(
    host="164.132.206.179",
    user="gs300465",
    password="vkhqUPt1JmSY",
    database="gs300465")
cursor = cnx.cursor()

text = "INSERT INTO users () VALUES ()"

cursor.execute(text)
cnx.commit()