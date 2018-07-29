import json  # for parsing json from the internets
import urllib.request  # for making a get request to the api
from tabulate import tabulate  # for printing out the table
from flask import Flask, render_template  # for generating and serving the web page
from app import app

class Human(object):
    """
    Class to represent each user of the program and to make it easy to organize
    information about the users.
    """
    username = None
    picture = None
    # firstName = None  # most users don't have their real names filled in
    # tracks = None  # to be implemented
    # artists = None  # to be implemented
    albums = None
    scrobbles = None

    def __init__(self, username):
        """
        Create user and populate information using the last.fm api
        """
        apiKey = getAPIKey()
        self.username = username.strip()  # get rid of any whitespace
        self.albums = []
        raw = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=user.getweeklyalbumchart&user='
                                     + self.username + '&api_key=' + apiKey
                                     + '&format=json').read().decode('utf-8')
        parser = json.JSONDecoder()
        parsed = parser.decode(raw)  # this comes out as a combination of dictionaries and lists
        albumsRaw = parsed['weeklyalbumchart']['album']  # dig through this mess
        for album in albumsRaw:  # add each album object to the list
            name = album['name']
            # print("adding", name)
            artist = album['artist']['#text']
            self.albums.append(Album(name, artist))
        raw = urllib.request.urlopen('http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user='
                                     + self.username + '&api_key=' + apiKey
                                     + '&format=json').read().decode('utf-8')
        parsed = parser.decode(raw)
        images = parsed['user']['image']
        scrobbles = parsed['user']['playcount']
        image = images[-1]['#text']
        self.picture = image
        self.scrobbles = scrobbles


class Album(object):
    """
    Class to represent an album and relevent information.
    """
    name = None
    artist = None

    def __init__(self, name, artist):
        self.name = name
        self.artist = artist


def getAPIKey(filepath='key.secret'):
    """
    Get the API key from a file. Add '*.secret' to your .gitignore so as not
    to publish the key by accident.
    """
    with open(filepath) as f:
        apiKey = f.read().replace('\n', '')
    # print('main.py:getAPIKey: @debug apiKey =', apiKey)
    return apiKey


@app.route('/')
def renderPage():
    users = [Human('discoversoar'), Human('youngflee_xyz'),
             Human('justinrhan'), Human('arynh')]
    top = 10  # number of albums to look at
    # print("Top " + str(top) + " albums of the past week:")
    # print("--------------------------------")
    usernames = [user.username for user in users]
    pictures = [user.picture for user in users]
    scrobbles = [user.scrobbles for user in users]
    albums = []
    for rank in range(top):
        row = []
        for user in users:
            name = user.albums[rank].name  # only take the first 30 chars
            row.append(name)
        albums.append(row)

    artists = []
    for rank in range(top):
        row = []
        for user in users:
            artist = user.albums[rank].artist  # only take the first 30 chars
            row.append(artist)
        artists.append(row)

    # print(tabulate(albums, headers=usernames, tablefmt="fancy_grid"))

    # generate index to list map
    twoDToOneD = []
    for i in range(top):
        twoDToOneD.append([k + len(users) * i for k in range(1, len(users) + 1)])

    page = render_template('index.html',
                           numAlbums=[i for i in range(1, top * len(users) + 1)],
                           rowList=[i for i in range(top)],
                           colList=[i for i in range(len(users))],
                           albums=albums,
                           artists=artists,
                           #links=0,
                           albumMatrixToList=twoDToOneD,
                           widthPercent=100/(len(users)+1),
                           zipped=zip(usernames, pictures),
                           usersToPass=zip(usernames, scrobbles))
    return page


if __name__ == "__main__":
    app.run(debug=True)
