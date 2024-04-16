import requests

response = requests.get('xxxx')
print(response.status_code)
if response.status_code == 200:
  print('Application is running successfully')
else:
  print ('Application Down. Fix it!')
