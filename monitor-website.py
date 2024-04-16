import requests
import smtplib
import os
import paramiko

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
APP_IP = os.environ.get('APP_IP')
SERVER_IP = os.environ.get('SERVER_IP')
CONTAINER_ID = os.environ.get('CONTAINER_ID')

def send_notification(email_msg):
  with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    msg = f"Subject: SITE DOWN\n {email_msg} "
    smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)

try:
  response = requests.get(APP_IP)
  if response.status_code == 200:
    print('Application is running successfully')
  else:
    print ('Application Down. Fix it!')
    msg = f'Application returned {response.status_code}'
    send_notification(msg)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=SERVER_IP, username='root', key_filename='C:\Users\LC\.ssh\id_rsa')
    stdin, stout, stderr = ssh.exec_command(f'docker start {CONTAINER_ID}')
    print(stout.readlines())
    ssh.close()
    print('Application restarted')

except Exception as ex:
  with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
      msg = f"Subject: SITE DOWN\n Application not accessible at all"
      send_notification(msg)
