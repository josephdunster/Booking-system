import sqlite3
from flask import Flask, session
from DateConversions import *
from datetime import date
import smtplib
from email.message import EmailMessage
from SearchesAndSorts import *
from RetrieveDataFromDatabase import *
from Validation import Hash
from AddingRecordsToDatabase import *
from flask import Flask

# A connection to the database is established
connection = sqlite3.connect('System.db')
cursor = connection.cursor()

cursor.execute("INSERT INTO TypeOfEvents (TypeOfEvent, PricePerAdult, PricePerChild) VALUES (?, ?, ?)", 
                ("Wedding1", 79, 39.5))

cursor.execute("INSERT INTO TypeOfEvents (TypeOfEvent, PricePerAdult, PricePerChild) VALUES (?, ?, ?)", 
                ("Wedding2", 89, 44.5))

cursor.execute("INSERT INTO TypeOfEvents (TypeOfEvent, PricePerAdult, PricePerChild) VALUES (?, ?, ?)", 
                ("Wedding3", 99, 49.5))

cursor.execute("SELECT * FROM TypeOfEvents")
rows = cursor.fetchall()

for row in rows:
    print(row)

connection.commit()
connection.close()