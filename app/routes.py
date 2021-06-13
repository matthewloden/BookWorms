from flask import render_template, session, redirect, abort, url_for, request, flash# , jsonify, request, make_response
from app import logging, app
from app.form import LoginForm, RegForm
from app.DBconnect import read_users, reg_user
from app.Playlists import makePlaylist
from flask_session import Session
import logging
import os
import spotipy
import uuid
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials



def restrictroute():
    if (not ('email' in session)):
        logging.warning("User attempting to access restricted page without logging in.")
        abort(403)
    return None

def session_cache_path():
    return caches_folder + session.get('uuid')



@app.route('/')
def index():
    return redirect(url_for('landing'))


@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/recommendations')
def recommendations():
    return render_template("recommendations.html")

# Login page for end users.
@app.route('/login', methods = ['GET','POST'])
def login():
    # Initializing login form.
    form = LoginForm()
    # If the client browser makes a POST request,
    if request.method == 'POST':
        # Temporarily storing username and password data.
        email = form.email.data
        passwd = form.password.data
        usrthere = False
        usrs = read_users().to_dict('list')
        idnum = 0
        # Checking if user is in DB and getting user info if he/she is in DB.
        if (email in usrs['email']):
            usrthere = True
            idnum = usrs['email'].index(email)


        # Going to enduser routes (only). devusers cannot logging in through this normal logging in page.
        if (usrthere and passwd == usrs['password'][idnum]):
            session['email'] = str(form.email.data)
            return redirect(url_for('home'))
        elif (passwd != usrs['password'][idnum]):
            flash(f'Incorrect Password', 'warning')
        elif (not(usrthere)):
            logging.info('Incorrect email: ' + email + ' and password: ' + passwd)
            flash(f'Incorrect email. There is no account associated with {email}', 'danger')
            flash(f'Please create an account on the Registration page')
        # Otherwise.
        else:
            flash(f'Something went wrong. Please try again or contact the admin.','primary')

    # Rendering login template.
    logging.info("Loading login form on login page.")
    return render_template("login.html", title = 'Login', form = form) 


# Registration Information page
@app.route("/registration", methods = ['GET', 'POST'])
def registration():
    # Initializing registration form.
    form = RegForm()
    # If client browser makes a POST request.
    if request.method == "POST":
        # If form is validated.
        if form.validate_on_submit():
            # Registering stakeholder/enduser in the DB.
            reg_user(str(form.email.data), str(form.name.data), str(form.password.data), int(form.age.data))
            logging.info(str("Account created for" + str(form.name.data) + ". Redirecting to login page."))
            flash(f'Account created for {form.name.data}. Please enjoy using our services.', 
            'success') # using success bootstrap class
            # Redirecting to login.
            session['email'] = str(form.email.data)
            return redirect(url_for("home"))
        else:
            logging.warning("Email/username entered already exists in DB, or did not type password correctly the second time.")
            flash(f'Incorrect re-typed password or username/email entered already exists. Please try again.', 
            'danger')
    # Rendering Registration template.
    logging.info("Creating Registration form on registration template for enduser.")
    return render_template('registration.html',title = 'Registration', form = form)


# End User Homepage
@app.route("/home")
def home():
    restrictroute()
    logging.info("Session username is" + "::::" +  session['email'])
    logging.info("Loading home page template.")
    # Returning the enduser/home template.
    return render_template('index.html')



@app.route('/search')
def search():
    restrictroute()
    return render_template("advsearch.html")

@app.route('/diagnostic')
def diagnostic():
    restrictroute()
    return render_template("diagnostic.html")

@app.route('/diagnosticTest')
def diagnosticTest():
    restrictroute()
    return render_template("diagnosticTest.html")



# NOTE: Spotify authentication code modified from https://github.com/perelin/spotipy_oauth_demo/blob/master/spotipy_oauth_demo.py

SPOTIPY_CLIENT_ID='8a10a7df741b481fad99595af62208e9'
SPOTIPY_CLIENT_SECRET='525833f5f47248d882954b8f8dac49bb'
SPOTIPY_REDIRECT_URI='http://127.0.0.1:5000/playlist'
SCOPE='user-top-read playlist-modify-public'
CACHE = '.spotipyoauthcache' # not important

app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/' # should this change?
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return caches_folder + session.get('uuid')


@app.route('/playlist') 
def playlist():
    restrictroute()
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, 
                                        client_secret=SPOTIPY_CLIENT_SECRET,
                                        redirect_uri=SPOTIPY_REDIRECT_URI,
                                        scope=SCOPE,
                                        cache_handler=cache_handler,
                                        show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect(url_for('playlist'))  # modify?
        
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render_template('spotifyLogin.html', auth=auth_url)

    # Step 4. Signed in, display data
    # Calls playlist recommendation algorithm
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    bookList = ['Book 1', 'Book 2', 'Book 3']  # this depends on whatever books the user chose!

    result1 = makePlaylist(bookList[0], spotify)
    result2 = makePlaylist(bookList[1], spotify)
    result3 = makePlaylist(bookList[2], spotify)

    # book 1
    pLinkA = result1[0]
    eLinkA = result1[1]

    # book 2
    pLinkB = result2[0]
    eLinkB = result2[1]

    # book 3
    pLinkC = result3[0]
    eLinkC = result3[1]

    return render_template('playlist.html', link1=pLinkA, link2=pLinkB, link3=pLinkC,
                                            embed1=eLinkA, embed2=eLinkB, embed3=eLinkC, 
                                            book1=bookList[0], book2=bookList[1], book3=bookList[2])    
    
@app.route('/sign_out') 
def sign_out():
    restrictroute()
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect(url_for('playlist'))
    


@app.route('/default_playlist')  
def default_playlist():
    restrictroute()
    return render_template('defaultPlaylists.html')


@app.route('/logout')
def logout():
    restrictroute()
    logging.info("Popping session email.")
    session.pop('email',None) # delete curr username in session and replace w/ None
    # Redirecting to index page.
    logging.info("Redirecting to landing page.")
    return redirect(url_for('landing'))