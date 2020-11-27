import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import urllib

def send_email(sender_email, password, receiver_email, route='https://www.google.com/'):
  t = time.localtime()
  timestamp = time.strftime("%A %B %d %Y %I:%M %p", t) 
  message = MIMEMultipart("alternative")
  message["Subject"] = 'Your Route Has Been Generated, ' + timestamp 
  message["From"] = sender_email
  message["To"] = receiver_email

  htmlfile = open("email_contents.html", "r")
  html = htmlfile.read().replace("_blank_1_", route).replace("_blank_2_", urllib.parse.quote_plus(str(route)))
  htmlfile.close()
  content = MIMEText(html, "html")


  message.attach(content)


  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
