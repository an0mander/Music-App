import json
import spotipy
import spotipy.util
import pprint
import lyricsgenius
scope = 'user-library-read playlist-read-private'


################################################################################
# Main Function
################################################################################
def main():

    global artist_name, artist_name
    print_header('Music Web Client', length=50)

    # Run our function
    retry = True
    while retry:
        try:
            print("""
How would you like to choose your tracks ?:
1.) Search for a song and display technical information about your selection
2.) Search for a artist - returns popular songs, lyrics and song information """)
            program_choice = int(input('Choice: '))
        except ValueError as e:
            print('Error: Invalid input.')
            continue
        if program_choice > 2:
            print("Sorry, your response must be either 1 or 2")
            continue
        elif program_choice < 0:
            print("Sorry your response must be not be negative")


        spotify = None
        selected_tracks = []
        if program_choice == 1:
            token = spotipy.oauth2.SpotifyClientCredentials(client_id='YOUR CLIENT ID HERE', client_secret='YOUR SECRET ID HERE')
            cache_token = token.get_access_token()
            spotify = spotipy.Spotify(cache_token)
            selected_tracks = search_track(spotify)
        elif program_choice == 2:
            artist_name = input("\nWhat artist would you like to search for: ")

        if selected_tracks:
            try:
                print("""
To get audio features for this track enter 1:
1.) Audio Features (Low-Level)""")
                display_choice = int(input('Choice: '))
            except ValueError as e:
                print('Error: Invalid input.')
                continue
            if display_choice > 1:
                print("Sorry, your response must be either 1 or 2")
                continue
            elif display_choice < 0:
                print("Sorry your response must be non negative")

            if display_choice == 1:
                get_audio_features(spotify, selected_tracks, pretty_print=True)

        elif artist_name:
            try:
                print("""
What would you like to see for your selection? :
1.) Get 50 most popular artist tracks 
2.) Return information about an artist and song
3.) Get lyrics for songs from chosen artist""" )
                display_choice = int(input('Choice: '))
            except ValueError as e:
                print('Error: Invalid input.')
                continue
            if display_choice > 3:
                print("Sorry, your response must be either 1 or 2")
                continue
            elif display_choice < 0:
                print("Sorry your response must be non negative")

            if display_choice == 1:
                try:
                    print(artist_name)
                    artist_tracks(artist_name)
                except Exception as e:
                    print("Could not retrieve artists tracks")
            elif display_choice == 2:
                try:
                    song_name = input('What song would you like to get information for?  ')
                    all_song_info(artist_name, song_name)
                except Exception as e:
                    print("Could not retrieve information")
            elif display_choice == 3:
                try:
                    song_name = input('What song would you like to get lyrics for?  ')
                    get_lyrics(artist_name, song_name)
                except Exception as e:
                    print("Could not retrieve lyrics")

        # Prompt the user to run again

        retry_input = input('\nRun the program again? (Y/N): ')
        yes = {'yes', 'y', 'ye', ''}
        no = {'no', 'n'}

        retry = input().lower()
        if retry_input in yes:
            retry = True
        elif retry_input in no:
            retry = False
        else:
            print("Please respond with 'y' or 'n'")
            continue

################################################################################
# API Fetch Functions
################################################################################


def get_audio_features(spotify, tracks, pretty_print=False):
    """
    Given a list of tracks, get and print the audio features for those tracks!
    :param spotify: An authenticated Spotipy instance
    :param tracks: A list of track dictionaries
    """
    if not tracks:
        print('No tracks provided.')
        return

    # Build a map of id->track so we can get the full track info later
    track_map = {track.get('id'): track for track in tracks}

    # Request the audio features for the chosen tracks (limited to 50)
    print_header('Getting Audio Features...')
    tracks_features_response = spotify.audio_features(tracks=track_map.keys())
    track_features_map = {f.get('id'): f for f in tracks_features_response}

    # Iterate through the features and print the track and info
    if pretty_print:
        for track_id, track_features in track_features_map.items():
            # Print out the track info and audio features
            track = track_map.get(track_id)
            print_audio_features_for_track(track, track_features)

    return track_features_map


def print_audio_features_for_track(track, track_features):
    """
    Given a track and a features response, print out the desired audio features for that track
    :param track:
    :param track_features:
    :return:
    """
    desired_features = [
        'tempo',
        'time_signature',
        'mode',
        'loudness',
        'energy',
        'danceability',
        'acousticness',
        'instrumentalness',
        'liveness',
        'speechiness',
        'valence'
    ]

    print('\n  {}'.format(track_string(track)))
    for feature in desired_features:
        # Pull out the value of the feature from the features
        feature_value = track_features.get(feature)

        # Print the feature value
        print('    {}: {}'.format(feature, feature_value))


################################################################################
# User Defined Functions
################################################################################

def search_track(spotify):
    """
        This function will allow the user to search a song title and pick the song from a list in order to fetch
        the audio features/analysis of it
        :param spotify: A spotipy client connection token
    """
    keep_searching = True
    selected_track = None

    # Initialize Spotipy
    token = spotipy.oauth2.SpotifyClientCredentials(client_id='YOUR CLIENT ID HERE',client_secret='YOUR SECRET ID HERE')
    cache_token = token.get_access_token()
    spotify = spotipy.Spotify(cache_token)

    # We want to make sure the search is correct
    while keep_searching:
        search_term = input('\nWhat song would you like to search: ')

        # Search spotify
        results = spotify.search(search_term, 50) #returns a max of 50 tracks
        tracks = results.get('tracks', {}).get('items', [])

        if len(tracks) == 0:
            print_header('No results found for "{}"'.format(search_term))
        else:
            # Print the tracks
            print_header('Search results for "{}"'.format(search_term))
            for i, track in enumerate(tracks):
                print('  {}) {}'.format(i + 1, track_string(track)))

        # Prompt the user for a track number, "s", or "c"
        track_choice = input('\nChoose a track #, "s" to search again, or "c" to cancel: ')
        try:
            # Convert the input into an int and set the selected track
            track_index = int(track_choice) - 1
            selected_track = tracks[track_index]
            keep_searching = False
        except (ValueError, IndexError):
            # We didn't get a number.  If the user didn't say 'retry', then exit.
            if track_choice != 's':
                # Either invalid input or cancel
                if track_choice != 'c':
                    print('Error: Invalid input.')
                keep_searching = False

    # Quit if we don't have a selected track
    if selected_track is None:
        return

    # Request the features for this track from the spotify API
    # get_audio_features(spotify, [selected_track])

    return [selected_track]


def print_audio_analysis_for_track(track, track_analysis):
    """
    Given a track and a analysis response, print out the analysis JSON
    :param track:
    :param track_analysis:
    :return:
    """
    print('\n  {}'.format(track_string(track)))
    print(json.dumps(track_analysis, indent=2))


def track_string(track):
    """
    Given a track, return a string describing the track:
    Track Name - Artist1, Artist2, etc...
    :param track:
    :return: A string describing the track
    """
    track_name = track.get('name')
    artist_names = ', '.join([artist.get('name') for artist in track.get('artists', [])])
    return '{} - {}'.format(track_name, artist_names)


def artist_tracks(artist_name):
    """""
    Get an artists top songs
    :param artists
    :return: A json text wall that has all artists tracks
    """

    genius = lyricsgenius.Genius("x8RadVSvYwnXPmR6VtduFObQqk9JgeWLIdjOh-QxD30hIv-fWbRJbXMm9I6O54Qq")
    # Using search to get correct artist and title
    print_header('Search results for songs by {}'.format(artist_name))
    artist = genius.search_artist(artist_name, max_songs=50,
                      sort='popularity', per_page=20,
                      get_full_info=True,
                      allow_name_change=False,
                      artist_id=None)

    #print_header('Search results for songs by {}"'.format(artist_name))
    result = artist.songs
    return result

def all_song_info(artist_name, song_name):

    genius = lyricsgenius.Genius("x8RadVSvYwnXPmR6VtduFObQqk9JgeWLIdjOh-QxD30hIv-fWbRJbXMm9I6O54Qq")

    song = genius.search_song(song_name, artist=artist_name,get_full_info=True)
    song_album = song.album
    song_album_url = song.album_url
    song_year = song.year
    featured_artists = song.featured_artists
    song_url = song.url

    print_header('Search results for "{} by {}"'.format(song_name, artist_name))
    print(
    "Year: {}".format(song_year),
    "Album: {}".format(song_album),
    "Featured Artists: {}".format(featured_artists),
    "Song Album URL: {}".format(song_album_url),
    "Song URL: {}".format(song_url), sep='\n')

def get_lyrics(artist_name,song_name):
    """""
    Get lyrics to a specific song
    :param artist_name, song_name
    :return: A string with song lyrics
    """
    genius = lyricsgenius.Genius("x8RadVSvYwnXPmR6VtduFObQqk9JgeWLIdjOh-QxD30hIv-fWbRJbXMm9I6O54Qq")
    # Using search to get correct artist and title
    song = genius.search_song(song_name, artist_name)
    print_header('Lyrics for "{} by {}"'.format(song_name, artist_name))
    #result = pprint.pprint(song.lyrics)
    result = print("{}".format(song.lyrics))
    return result


def print_header(message, length=50):
    """
    print a message with decorative stars around the message
    :param message: The message you want to print
    :param length: The number of stars you want to surround it
    """
    print('\n' + ('*' * length))
    print(message)
    print('*' * length)


if __name__ == '__main__':
    main()
