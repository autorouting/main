import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import urllib
from threading import Thread

def send_email(sender_email, password, receiver_email, route='https://www.google.com/'):
  t = time.localtime()
  timestamp = time.strftime("%A %B %d %Y %I:%M %p", t) 
  message = MIMEMultipart("alternative")
  message["Subject"] = 'Your Route Has Been Generated, ' + timestamp 
  message["From"] = sender_email
  message["To"] = receiver_email

  htmlfile = open("email_contents.html", "r")
  html = htmlfile.read().format_map({
    "routelink": route,
    "qrdata": urllib.parse.quote_plus(route)
  })
  htmlfile.close()
  content = MIMEText(html, "html")


  message.attach(content)


  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )

def send_email_async(sender_email, password, receiver_email, route='https://www.google.com/'):
  send_email_thread = Thread(target = send_email, args=(sender_email, password, receiver_email, route))
  send_email_thread.start()

