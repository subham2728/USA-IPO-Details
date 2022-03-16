#pip install finnhub-python
import finnhub
import os
from dotenv import load_dotenv
import datetime
from datetime import date
import array
import json
import smtplib

load_dotenv()
API_KEY = os.environ.get("API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
PASSWORD = os.environ.get("PASSWORD")
PORT_NUMBER = os.environ.get("PORT_NUMBER")

date_today = date.today()
print("Today's date = ",date_today)

date_today_str = str(date_today)
date_extract = datetime.datetime.strptime(date_today_str, "%Y-%m-%d")

date_day = int(date_extract.day)
date_month = int(date_extract.month)
date_year = int(date_extract.year)

finnhub_client = finnhub.Client(api_key=API_KEY)

month_array = array.array('i',[0,31,28,31,30,31,30,31,31,30,31,30,31])
count = 0
days = 30

if date_year%4==0:
    month_array[2] = 28

while count < days:
    date_day = date_day+1
    count = count+1

    if date_day > month_array[date_month]:
        date_day = 1
        date_month = date_month+1

    if date_month > 12:
        date_month = 1
        date_year = date_year + 1

        if date_year % 4==0:
            month_array[2] = 29

        else:
            month_array[2] = 28

future_year = str(date_year)
future_date = str(date_month)
future_day = str(date_day)

future_date = future_year + '-' + future_date + '-' + future_day

future_date_object = datetime.datetime.strptime(future_date, "%Y-%m-%d").date()

print("Date after",days,"days = ",future_date_object)

json_date = finnhub_client.ipo_calendar(_from = "date_today", to = "2022-04-15")

# print(type(json_date))

json_formatted = json.dumps(json_date, indent=2)

server=smtplib.SMTP('smtp.gmail.com',PORT_NUMBER)
server.starttls()

server.login(SENDER_EMAIL,PASSWORD)

print("Login success")

server.sendmail(SENDER_EMAIL,RECEIVER_EMAIL,json_formatted)
print("Mail sent")


