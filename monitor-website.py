import requests
import smtplib
import os

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

def send_notification(email_msg):
  with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    msg = f"Subject: SITE DOWN\n {email_msg} "
    smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)


try:
  response = requests.get('xxxx')
  if response.status_code == 200:
    print('Application is running successfully')
  else:
    print ('Application Down. Fix it!')
    msg = f'Application returned {response.status_code}'
    send_notification(msg)
except Exception as ex:
  with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
      msg = f"Subject: SITE DOWN\n Application not accessible at all"
      send_notification(msg)
