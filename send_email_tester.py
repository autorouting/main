import send_email

credentials = str(open("email_config.txt", "r").read())
credentials = credentials.split('\n')
send_email.send_email(credentials[0], credentials[1], str(input('receiver email?  ')), 'https://www.google.com/')
print('Completed')