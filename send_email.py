import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email, route='filler'):
  sender_email = "autorouting.app"
  password = 'ElegantPiano'
  message = MIMEMultipart("alternative")
  message["Subject"] = "Your Route has Been Generated!"
  message["From"] = sender_email
  message["To"] = receiver_email

  # Create the plain-text and HTML version of your message
  html = """\
  <html>
    <body>
      <p>Hi,<br>
        Your route is: blah blah blah
        <br>
       Generated with: <a href="http://www.techworldconnect.com/delivery/">Autorouting</a> 
    </p>
  </body>
</html>
"""

  html1 =  html[:60]
  html2 = html[80:]
  html = html1 + str(route) + html2
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