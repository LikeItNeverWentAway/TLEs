print("Importing libraries...")

import requests
from ftplib import FTP
from urllib import request


url = 'https://www.space-track.org/ajaxauth/login'
headers = {'Host':'www.space-track.org', 'Content-Type':'application/x-www-form-urlencoded'}

print('Downloading data... ', end = '')
js = request.urlopen('https://celestrak.com/SpaceTrack/spacetrack.js')
js = js.readlines()
print('Done')


print('Processing data for the satellites launched in the last 30 days:')
print('Retrieving Norad Satellite IDs from file... ', end = '')
last30 = js[54]
last30 = str(last30)
last30 = last30.split()
last30 = last30[3]
last30 = last30.split('"')
request_last30=last30[1]

print('Found',len(request_last30)//6,'satellites')

query_last30 = 'https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/'+request_last30+'/orderby/NORAD_CAT_ID%20desc/predicates/OBJECT_NAME,TLE_LINE1,TLE_LINE2/format/3le'

print('Sending authentification and TLE data POST request to space-track.com...')
payload ={'identity':'MAIL','password':'PASSWORD','query':query_last30}
r_last30 = requests.post(url, data=payload, stream=True)
print('Status code: ',r_last30.status_code, '- Request successfully sent')
data_last30 = r_last30.text
data_last30 = data_last30.replace('\r','')

print('\n')

print('Processing data for the brightest satellites...')
print('Retrieving Norad Satellite IDs... ', end ='')

brightest_a = js[60]
brightest_a = str(brightest_a)
brightest_a = brightest_a.split()
brightest_a = brightest_a[3]
brightest_a = brightest_a.split('"')
request_brightest_a=brightest_a[1]


brightest_b = js[63]
brightest_b = str(brightest_b)
brightest_b = brightest_b.split()
brightest_b = brightest_b[3]
brightest_b = brightest_b.split('"')
request_brightest_b=brightest_b[1]

print('Found',len(request_brightest_a+request_brightest_b)//6,'satellites.')


query_brightest = 'https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/'+request_brightest_a + request_brightest_b +'/orderby/OBJECT_NAME%20asc/predicates/OBJECT_NAME,TLE_LINE1,TLE_LINE2/format/3le'




payload ={'identity':'MAIL','password':'PASSWORD','query':query_brightest}
r_brightest = requests.post(url, data=payload, stream=True)
print(r_brightest.status_code, r_brightest.reason)
data_brightest = r_brightest.text
data_brightest = data_brightest.replace('\r','')

print('Storing TLE Data...')
file=open('sat.txt','w')
file.write(data_last30 + data_brightest)
file.close
print('File ready for transfer.')

print('Establishing ftp connection to FTPSERVER...' , end ='')
server = FTP('HOST','ID','PASS')
print(' Ready')
file_transfer=open('sat.txt','rb')
server.cwd('www')
print('Beginning transfer...')
print(server.storbinary('STOR ''sat.txt', file_transfer))
file_transfer.close()
print('Done.')
