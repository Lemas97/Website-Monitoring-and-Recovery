import requests
import smtplib
import os
import paramiko
import linode_api4
import time
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
APP_IP = os.environ.get('APP_IP')
SERVER_IP = os.environ.get('SERVER_IP')
CONTAINER_ID = os.environ.get('CONTAINER_ID')
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')
LINODE_INSTANCE_ID = os.environ.get('LINODE_INSTANCE_ID')

def send_notification(email_msg):
  with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    msg = f"Subject: SITE DOWN\n {email_msg} "
    smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)

def restart_container():
  print('Restarting the application')
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect(hostname=SERVER_IP, username='root', key_filename='C:\Users\LC\.ssh\id_rsa')
  stout = ssh.exec_command(f'docker start {CONTAINER_ID}')
  print(stout.readlines())
  ssh.close()

def restart_server_and_container():
  client = linode_api4.LinodeClient(LINODE_TOKEN)
  nginx_server = client.load(linode_api4.Instance, LINODE_INSTANCE_ID)
  nginx_server.reboot()
  while True:
    time.sleep(5)
    nginx_server = client.load(linode_api4.Instance, LINODE_INSTANCE_ID)
    if nginx_server.status == 'running':
      restart_container()
      break

def monitor_application():
  try:
    response = requests.get(APP_IP)
    if response.status_code == 200:
      print('Application is running successfully')
    else:
      print ('Application Down. Fix it!')
      msg = f'Application returned {response.status_code}'
      send_notification(msg)
      restart_container()
      print('Application restarted')

  except Exception as ex:
    msg = f"Subject: SITE DOWN\n Application not accessible at all"
    send_notification(msg)
    restart_server_and_container()

schedule.every(5).minutes.do(monitor_application())
while True:
  schedule.run_pending()
