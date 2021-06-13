from app import app,logging
import os

# For Testing purposes, will put into debug mode whenever this file.
# is run directly
if __name__ == '__main__':
   #os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1" #For testing purposes only, can work with HTTP requests instead of only HTTPS requests.
   #os.environ['wsgi.url_scheme'] = 'http'
   app.run(threaded = True, host = "127.0.0.1", port = 5000, debug = True) # debug must be False for log statements to work.


