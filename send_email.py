import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

def send_email(receiver_email, route='filler route insert route here'):
  sender_email = "autorouting.app"
  password = 'ElegantPiano'
  message = MIMEMultipart("alternative")
  subject_lines = ['Your Route Has Been Generated!', 'Route Generation Completed!', 'Here is Your Custom Route']
  message["Subject"] = random.choice(subject_lines)
  message["From"] = sender_email
  message["To"] = receiver_email

  # Create the plain-text and HTML version of your message
  html = """\
  <html>
    <body>
      <p>Hi,<br>
        Your route is: blah blah blah
        <br><br><br>
       <i>Generated by the Autorouting Application at: <a href="http://www.techworldconnect.com/delivery/">http://www.techworldconnect.com/delivery/</a> <br>
       -The Autorouting Team</i>
    </p>
  </body>
</html>
"""

  html1 =  html[:60]
  html2 = html[80:]
  html = html1 + '<b>' + str(route) + '</b>' + html2
  content = MIMEText(html, "html")


  message.attach(content)


  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )

send_email('jaden.mu@gmail.com')
print(1)