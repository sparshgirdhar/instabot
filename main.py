import requests

access_token= "2177622775.bcc91a8.70838b84b2ac4fc09d68e2a2ef9b1981"

base_url= "https://api.instagram.com/v1/"

def self_info():
    request_url = (base_url + 'users/self/?access_token=%s') % (access_token)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()
    print user_info

self_info()