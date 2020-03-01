"""
# @author - Zach Jansma
#
# Date Written - 02/02/2020
# Last Updated - 02/29/2020
#
# Purpose - Impliment a web service solution utilizing Spotify API App
#	- User will type artist/band into command line interface
#	- Will search for artist using API call and bring back:
#		* Top 5 tracks of artist
#		* 3 Similar Artist
#
"""
#### Import Libraries ####
import spotipy # Spotify API for handling all requests
from spotipy.oauth2 import SpotifyClientCredentials # To authenticate when sending queries to Spotify
import re # Regex for user input sanitation
import sys # For properly exiting the program

# Quick greeting when user first starts the program
def initialGreeting():

	# Output the greeting when the user first starts the program
	print(">>> Welcome to the Spotify command line API! ") 
	print(">>> type !help for help or !quit to quit")
	print(">>> Type an artist's name to get their top 5 tracks and similar artists\n")
    
# Initalize our connect to spotify using spotipy creds. If successful, 
#   return the authentication for querying spotify
def initSpotify():

    # This will attempt to connect to spotify SPOTIPY_USER_CREDENTIALS    
    try:
    	# Create connection string
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

        # Try a dummy query to see if it works
        result = sp.search('test', limit=1, type='artist')

    # If you have internet issues, you'll get a connectionerror  
    except ConnectionError as err:
    	print(str(err) + ", is your internet working??")
    	sys.exit(1)
        
    # If there is an error connecting, print out error, and message to check README
    except spotipy.oauth2.SpotifyOauthError as err:
    	print(str(err) + ", Double check your Client ID and Secret - They may not be correct!\n")
    	sys.exit(2)
    
    # deleted unused variable
    del result

    # Return the connection header
    return sp


# If the user gives a ! command, print information requested
def exInput(user_input):

	# Print new line to clean output
	print("")

	# Loop through to produce information based on ! command:
    # Help for general program usage
	if(user_input == "!help"):
        
        # Information on how to use the API
		print("Band Search Usage:")
		print("Type the name of a band, singer, or songwriter you wish to know about")
		print("If the artist is on Spotify, we'll pull back the top 5 tracks, ")
		print("as well as some similar artists!\n")
		print("Additional commands - !about, !favs, !quit\n")
    
    # A bit of information about myself and the program
	elif(user_input == "!about"):
        
        # A little bit about me
		print("Written by - Zach Jansma")
		print("Made with love and a good amount of coffee.")
		print("This program is also vegan friendly.\n")
        
    # My favorite artists
	elif(user_input == "!favs"):

		# My fav artists!
		print("Thanks for asking! My favorite artists at the moment are: ")
		print("Post Malone, Lizzo, Mac Miller, and Bonobo to name a few.\n")

	# User wishes to quit the program
	elif(user_input == "!quit"):

		# Thank them for using the program and exit!
		print(">>> Thanks for using the program! ")
		sys.exit(0)
        
    # if garbage was given, let user know all commands they can use
	else:

		print("Hmm, not sure what you mean. Try one of these commands:")
		print("!about, !favs, !help, !quit\n")


# Method used to sanatize user input. If a user hits an error, will add to error counter
#	will continue to ask for input until no errors are thrown
def cleanUserInput():

	# Keep looping until proper input is given
	while True:

		# Ask for an artist name
		name = input(">>> Please input a name of an artist/band: \n")

		# If the user doesn't enter anything, prompt again
		if(not name):
			pass
		else:

			# Error counter to check how many errors occur
			err_counter = 0

			# User has called ! function
			if(name[0] == '!'):
				exInput(name)

				# while not a true error, I want to keep looping
				err_counter = err_counter + 1

			# Ensure only ascii characters were given
			if(err_counter == 0):
				try:
					name.encode("ascii")
				except UnicodeDecodeError:
					print("Please use only Alpha-numeric characters for searching")
					err_counter = err_counter + 1
				except UnicodeEncodeError:
					print("Please use only use Alpha-numeric characters found in the English Langauge")
					err_counter = err_counter + 1

			# Check for any weird characters in input
			if(err_counter == 0):
				if(re.search(r'[^a-zA-Z0-9_\s\.!,]',name)):

					# Print error type, add to counter
					print("Please only use Alpha-numeric characters for searching")
					err_counter = err_counter + 1

			# Ensure query is less than or equal to 50 characters
			if(err_counter == 0):
				if(len(name) > 50):

					# Print error type, add to counter
					print("Name too long - please keep query equal or under 50 characters.")
					err_counter = err_counter + 1

			# If no errors were thrown, break out of the loop
			if(err_counter == 0):
				break

	return name


# searchSpotify will utilize API call to bring back information about artist
def searchSpotify(artist_name, sp):

	# Search for artist - will bring back 3 artist incase user mispelled
	#	If credentials are not properly set up, may error out here
	result = sp.search(artist_name, limit=3, type='artist')

	# If a blank item is returned, spotify couldn't search the artist
	if(len(result['artists']['items']) == 0):

		# Let users know something went wrong
		print("Hmm.... Spotify didn't return any results. Did you type the name correctly?\n")

	# If the top hit = user input, we've got a match! 
	#	make sure to match case - cast all to lower
	elif(result['artists']['items'][0]['name'].lower() == artist_name.lower()):

		# We found our artist!
		print(artist_name + " - Found!\n")
		
		# Grab artist ID; append nessicary header info
		artist_id = 'spotify:artist:' + result['artists']['items'][0]['id']

		# Grab top 5 tracks using id
		topFive = sp.artist_top_tracks(artist_id)

		# Print out top 5 tracks; use counter to limit amount of tracks
		counter = 1

		print("Top 5 Tracks: ")

		for track in topFive['tracks']:

			# Print the formatted track names
			print(str(counter) + ".) " + str(track['name']))
			
			# Incriment the counter
			counter = counter + 1

			# Once we've printed our top 5, break out
			if(counter > 5):
				break

		# Bring back related artists
		print("\nIf you like " + artist_name + ", check out these related artists: ")

		# Get similar artists
		similarArtists = sp.artist_related_artists(artist_id)

		# Print out 3 similar artists, similar fashion as before w/ counter
		counter = 1

		for artist in similarArtists['artists']:

			# Print out the first two names with commas after
			if(counter < 3):
				# Print out artist, making sure to keep them all on the same line
				print(artist['name'], end=", ")

				# incriment counter
				counter = counter + 1

			# After the 3rd artist, end with new line
			else: 
				print(artist['name'])
				print("")
				break

	# We weren't returned a blank list, but our query didn't quite match up
	else:

		print("Spotify had some trouble finding the exact name. Maybe you meant: \n")

		# Loop through all 3 suggestions brough back
		for name in result['artists']['items']:
			print(name['name'])

		# Print new line to clean output
		print("")


# Main interface used for directing user. Will take the spotipy authenticator
def mainInterface(sp_creds):

	# Loop in main interface until user gives !quit command
	while True:

		# Ask for an artist/band name
		artist_name = cleanUserInput()

		# Check user input
		if(artist_name[0] == "!"): # ! command - special command
			exInput(artist_name)

		else:
			# Let the user know we're searching their query 
			print("\n>>> ... searching ....\n")

			# Call the Spotify API
			searchSpotify(artist_name,sp_creds) 

		# Ask if the user wants to continue
		print(">>> Type another artist, or type !quit to exit the program.")


if __name__ == "__main__":

	# Make sure we can connect to spotify
    sp_creds = initSpotify()

    # Greet the user
    initialGreeting()
    
    # if statement if something goes wrong
    mainInterface(sp_creds)
