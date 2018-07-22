import json  # for parsing json from the internets
import urllib.request  # for making a get request to the api
from tabulate import tabulate  # for printing out the table


class Human(object):
    """
    Class to represent each user of the program and to make it easy to organize
    information about the users.
    """
    username = None
    # firstName = None  # most users don't have their real names filled in
    # tracks = None  # to be implemented
    # artists = None  # to be implemented
    albums = None

    def __init__(self, username):
        """
        Create user and populate information using the last.fm api
        """
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


class Album(object):
    """
    Class to represent an album and relevent information.
    """
    name = None
    artist = None

    def __init__(self, name, artist):
        self.name = name
        self.artist = artist


def getAPIKey(filepath='../../key.secret'):
    """
    Get the API key from a file. Add '*.secret' to your .gitignore so as not
    to publish the key by accident.
    """
    with open(filepath) as f:
        apiKey = f.read().replace('\n', '')
    # print('main.py:getAPIKey: @debug apiKey =', apiKey)
    return apiKey


if __name__ == "__main__":
    apiKey = getAPIKey()
    users = [Human('discoversoar'), Human('youngflee_xyz'), Human('justinrhan'), Human('arynh')]
    top = 10  # number of albums to look at
    print("Top " + str(top) + " albums of the past week:")
    print("--------------------------------")
    usernames = [user.username for user in users]
    table = []
    for rank in range(top):
        row = [str(rank + 1)]
        for user in users:
            name = user.albums[rank].name[:30]  # only take the first 30 chars
            artist = user.albums[rank].artist[:30]  # ^
            row.append(name + '\n' + artist)
        table.append(row)

    print(tabulate(table, headers=usernames, tablefmt="fancy_grid"))
