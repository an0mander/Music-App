# Getting Started with the music web client


This app authenticates with the Spotify API and the Genius API and fetches the audio features for searched tracks.
It also allows you to search a track and list out the audio features and analysis specifically for that track.


The Spotify Web API allows applications to fetch lots of data from the Spotify catalog. Some examples of of info you get are:
  - Track, artist, album search
  - High-level audio features for tracks
  - In-depth audio analysis for tracks
  - Download searched song lyrics to a text file


Spotipy is an awesome lightweight Python wrapper library for the Spotify Web API.  Using Spotipy, you can get any information
that you can get through the raw Web API.  The library does a bunch of the heavy lifting for things like authenticating
against the API, serializing request data, and deserialize response data.

LyricsGenius is a lightweight wrapper for the Genius API (Genius.com) and helps users get data like lyrics from
the Genius website

## Setup
The client access tokens would be procured by the user from Spotify and Genius for the purpose of this project


#### Install Dependencies
In order to run this program, we need to make sure python3, pip, and virtualenv are installed on your system.
To install this stuff, run (the setup.sh bash file is located in the project root folder. It will isntall packages needed for the project
```
./setup.sh
source ~/.bashrc
```
_Note: If you approve, the setup script will add a line to your bashrc (your shell startup commands) which will
automatically activate your virtual environment when you `cd` into this directory using your isolated python environment.

## Running
To run the out of the box demo, simply run
```
make run
```

After that, just follow the terminal :)
