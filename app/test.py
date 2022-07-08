import smtplib, ssl

sender = 'test@test.com'
receivers = ['postmaster@inventorius.com']

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""
context = ssl.create_default_context()

try:
   smtpObj = smtplib.SMTP('localhost', 25)
   smtpObj.sendmail(sender, receivers, message)         
   print("Successfully sent email")
except Exception as e:
    print(e)
    print("Error: unable to send email")
