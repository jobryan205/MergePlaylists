from flask import Flask, render_template, redirect, session, request
from classes import *
import requests
import json
 
app = Flask(__name__)      
client_id = '9c6fda1a080a491bbd3910b49523da23'
client_secret = '83d5e0f8f3ec473d9473c265cb1c2ff6'
app.secret_key = 'GarlicBreadAndChill?GoodShitGoodShitAlienShitBushDid911FuckBanannaBread'
spotifyAuthEndpoint = 'https://accounts.spotify.com'
spotifyAPIEndpoint = 'https://api.spotify.com'
redirect_uri =  'http://localhost:5000/playlists'


@app.route('/playlists')
def playlists():
	# retrieving code from url
	session['code'] = request.args.get("code")

	# making post request to retrieve access_token
	requestURL = '{}/api/token'.format(spotifyAuthEndpoint)
	data = {
		'grant_type': 'authorization_code',
		'code': session['code'],
		'redirect_uri': redirect_uri,
		'client_id': client_id,
		'client_secret': client_secret
	}
	response = requests.post(requestURL, data=data)
	session['access_token'] = response.json()['access_token']
	print session['access_token']

	# making get request to get userid
	headers = {
		'Authorization': "Bearer " + session['access_token']
	}
	requestURL = '{}/v1/me'.format(spotifyAPIEndpoint)
	response = requests.get(requestURL, headers = headers)
	session['id'] = response.json()['id']


	getPlaylistsURL = '{}/v1/users/{}/playlists'.format(spotifyAPIEndpoint, session['id'])
	# print "getPlaylistsURL: "
	print getPlaylistsURL
	response = requests.get(getPlaylistsURL, headers = headers)
	data = json.loads(response.text)
	print data['items'][0]['name']

	# I coded this next part while drunk. No idea if it works or not
	playlists = []
	for playlist in data['items']:
		id = playlist['id']
		playlistURL = playlist['href']
		name = playlist['name']
		imageURLs = playlist['images'] #double check url name here
		owner = playlist['owner']['id']

		p = Playlist(name, id, owner, imageURLs, playlistURL)
		playlists.append(p)
		print p


	options = {
		'code': session['code']
	}
	return render_template('playlists.html', **options)

@app.route('/login')
def login():
	OAuthURL = '{}/authorize/?client_id={}&response_type=code&redirect_uri={}'.format(spotifyAuthEndpoint, client_id, redirect_uri)
	return redirect(OAuthURL)

@app.route('/')
def index():
	print spotifyAuthEndpoint
	return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)