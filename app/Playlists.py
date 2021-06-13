# gets artist seeds for recommendations
def getArtists(sp):
    results = sp.current_user_top_artists(limit=15, offset=0, time_range='medium_term')
    items = results['items']
    return items

# generates recommended tracks
def getRecs(artists, sp):
    tracks = []
    trackNames = []
    artistNames = []
    for i in range(0, len(artists)):
        artist = artists[i]
        results = sp.recommendations(seed_genres=sp.recommendation_genre_seeds(), seed_artists=[artist['id']], limit=1)
        for track in results['tracks']:
            trackNames.append(track['name'])
            artistNames.append(track['artists'][0]['name'])
            tracks.append(track['uri'])

    return tracks

# creates a new playlist
def createPlaylist(name, sp):
    playlist = sp.user_playlist_create(sp.me()['id'], name)
    return playlist, playlist['id']

# finds a playlist by name so that new ones are not made every time
def findPlaylist(name, sp):
    pl = 0  # default if not found
    id = 0  # default if not found
    playlists = sp.user_playlists(sp.me()['id'], limit=50, offset=0)
    for playlist in playlists['items']:
        if playlist['name'] == name:
            pl = playlist
            id = playlist['id']
        
    return pl, id

# adds songs to playlist
def addToPlaylist(tracks, playlistID, sp):
    sp.playlist_add_items(playlist_id=playlistID, items=tracks)

# gets playlist link
def getLink(playlist):
    playlistLink = playlist['external_urls']['spotify']

    return playlistLink

# makes a playlsit for a given book
def makePlaylist(bookName, sp):
    returnList = []
    pl, plID = findPlaylist(bookName, sp) 

    if plID == 0:  # playlist not found, create one
        artists = getArtists(sp)
        tracks = getRecs(artists, sp)
        pl, plID = createPlaylist(bookName, sp)
        addToPlaylist(tracks, plID, sp)
        '''songs = []
        for song, artist in zip(songNames, artistList):
            songs.append(song+" by "+artist)'''

    plLink = getLink(pl)
    embedLink = "https://open.spotify.com/embed/playlist/" + plID

    # return embed link, playlist link, and list of artists + songs
    returnList.append(plLink)
    returnList.append(embedLink)

    return returnList
        
# for testing purposes
'''def main():
    bookList = ['P&P', 'TKR', 'PJ']  # this depends on whatever books the user chose!
    result1 = makePlaylist(bookList[0])
    result2 = makePlaylist(bookList[1])
    result3 = makePlaylist(bookList[2])
    print(result1, '\n', result2, '\n', result3)
#main()'''