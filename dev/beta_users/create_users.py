import requests
import csv
url = 'http://localhost:8000/v1/auth/register/'
# data = {
#     "sid" : "00001",
#     "email" : "00001@test.proqod.com",
#     "password" : "123",
#     'user_type' : '0',
#     'is_admin' : '0',
# }

with open('beta_users.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for [sid, user_type, is_admin, password] in spamreader:
        data = {
            "sid": sid,
            "email": "%s@test.proqod.com" % sid,
            "password": password,
            'user_type': user_type,
            'is_admin': is_admin
        }
        print "\ncreated user: %s\n" % data

        response = requests.post(url, data=data)
