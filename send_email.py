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

  html1 = """\
  <html>
    <body>
      <p>Hi,<br>
        Your route is: <a href="
  """
  html2 =         """
  "><b>Here</b></a><br>Or scan this QR code:<img src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data="""
  html3 = """"/><br><br><br>
       <i>Generated by the Autorouting Application at: <a href="http://www.techworldconnect.com/delivery/">http://www.techworldconnect.com/delivery/</a> <br>
       -The Autorouting Team</i>
    </p>
  </body>
</html>
"""
  html = html1 + str(route) + html2 + urllib.parse.quote_plus(str(route)) + html3
  content = MIMEText(html, "html")


  message.attach(content)


  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
