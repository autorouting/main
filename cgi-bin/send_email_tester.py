import send_email
user_email = input('What is the recipients email?  ')
route_link = 'google.com'

if len(str(user_email)) != 0 and user_email != None:
    credentials = str(open("email_config.txt", "r").read())
    credentials = credentials.split('\n')
    send_email.send_email_async(credentials[0], credentials[1], user_email, route_link)
