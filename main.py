import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

access_token = "2177622775.bcc91a8.70838b84b2ac4fc09d68e2a2ef9b1981"

base_url = "https://api.instagram.com/v1/" #instagram API

def self_info():
    request_url = (base_url + 'users/self/?access_token=%s') % (access_token)
    print "GET request url : %s" % (request_url) #Get information about the owner of the access token
    user_info = requests.get(request_url).json()

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

def get_user_id(insta_username):
  request_url = (base_url + 'users/search?q=%s&access_token=%s') % (insta_username, access_token)
  print 'GET request url : %s' % (request_url) #Get information of the user using the username
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
    print 'GET request url : %s' % (request_url) #Get information about a user
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
    print "GET request url is: %s" %request_url #Get the most recent media of the user
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

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    print "GET request url is: %s" % request_url #Get the most recent media of a user
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    print 'GET request url : %s' % (request_url) #Url to get the id of the post
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

#Set a like on media by current user

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (base_url + "media/%s/likes") %(media_id)
    payload = {"access_token": access_token}
    print 'POST request url : %s' % (request_url)
    post_like= requests.post(request_url, payload).json()

    if post_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

#Set a comment on media by current user

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": access_token, "text" : comment_text}
    request_url = (base_url + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"

#Identifies whether the comment is negative or positive and delete it if it's negative

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (base_url + 'media/%s/comments/?access_token=%s') % (media_id, access_token)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (base_url + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, access_token)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'

def start_bot():
    show_menu = True

    while show_menu:
        menu_choices = "Hey! Welcome to instaBot! \n What do you want to do? \n a.Get your own details\n b.Get details of a user by username\n c.Get your own recent post\n d.Get the recent post of a user by username\n e.Get a list of people who have liked the recent post of a user\n f.Like the recent post of a user\n g.Get a list of comments on the recent post of a user\n h.Make a comment on the recent post of a user\n i.Delete negative comments from the recent post of a user\n j.Exit"
        choice = raw_input(menu_choices)
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice == "j":
            print "================================="
            print "            InstaBot             "
            print "   Developed by Sparsh Girdhar   "
            print "================================="
            print ""
            exit()
        else:
            print "Wrong Choice :/"

start_bot()