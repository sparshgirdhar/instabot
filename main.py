import requests, urllib

access_token= "2177622775.bcc91a8.70838b84b2ac4fc09d68e2a2ef9b1981"

base_url = "https://api.instagram.com/v1/"

def self_info():
    request_url = (base_url + 'users/self/?access_token=%s') % (access_token)
    print "GET request url : %s" % (request_url)
    user_info = requests.get(request_url).json()
    print user_info

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print "Username: %s" % (user_info['data']['username'])
            print "No. of followers: %s" % (user_info['data']['counts']['followed_by'])
            print "No. of people you are following: %s" % (user_info['data']['counts']['follows'])
            print "No. of posts: %s" % (user_info['data']['counts']['media'])
        else:
            print "User does not exist!"
    else:
        print "Status code received is other than 200!"

insta_username="megha_tyagii"

def get_user_id(insta_username):
  request_url = (base_url + 'users/search?q=%s&access_token=%s') % (insta_username, access_token)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()

  if user_info['meta']['code'] == 200:
      if len(user_info['data']):
          return user_info['data'][0]['id']
      else:
          return None
  else:
      print 'Status code other than 200 received!'
      exit()

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (base_url + 'users/%s?access_token=%s') % (user_id, access_token)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'

def get_own_post():
    request_url = (base_url + 'users/self/media/recent/?access_token=%s') % (access_token)
    print "GET request url is: %s" %request_url
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

get_own_post()
