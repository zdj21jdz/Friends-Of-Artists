# ReadMe for Friends of Artist app

This is the official README for setting up the Friends_Of_Artists search app.
Developed by - Zach Jansma

### Purpose of The Program
The purpose of this program is to find the top 5 tracks of a related artist, and then find 3 related artists. You can use this tool as a way to find new artist that are similar to the one you already like!

### Initial Setup
Friends_Of_Artists is written in python 3. Ensure you have the most up to date python 3 library prior to running.
In order to run this on your local, you will need to install the spotipy library:
```
pip3 install spotipy
```

You will need to create a client ID and Secret through the spotify developer dashboard. Create an app, and then set up your ID and secret as environment variables.<br>

If you wish to configure spotipy for your local app settings, set the follow variables:

Linux:<br>
export SPOTIPY_CLIENT_ID=your_id_from_spotitfy_here<br>
export SPOTIPY_CLIENT_SECRET=your_client_secret

Windows:<br>
set SPOTIPY_CLIENT_ID=your_id_from_spotitfy_here<br>
set SPOTIPY_CLIENT_SECRET=your_client_secret

### Running the program
FriendsOfArtists is a command line interface that will retrieve the top 5 tracks of an 
artists on Spotify, as well as 3 similar artists. The intended input is an artist's name, or a 
special function that can give the user additional information (such as typing !help 
for a quick note on how to use the interface). 

To execut in the command line, type the following command:
```
python3 Friends_Of_Artists.py
```

#### Input
Once the program launches, the expected input will be a single artist, such as:

Post Malone

The input stream will be capped out at 50 characters - if a user tries to input more, an error 
will be thrown asking the user to keep their query under 50 characters.

Additionally, the program will only accept alpha-numeric characters, periods, commas, dashes, and exclamation marks.

#### Output
The output will return top 5 tracks and 3 similar artists in this fashion:<br>
… searching …

Post Malone – Found!

 Top Tracks:

1.) Circles

2.) Goodbyes (feat. Young Thug)

3.) Wow.

4.) Sunflower – Spider-Man: Into the Spider-Verse

5.) rockstar (feat. 21 Savage)

If you like Post Malone, check out these related artists:

Rae Sremmurd, Huncho Jack, Lil Skies

#### Error handling
The input from the user should be less than or equal to 50 characters, and should only contain
alpha-numeric input, including dashes (-), commas (,) and periods (.). If the user's 
query contains anything outside of these parameters, the program will ask until valid input is given.

When the program first searches for an artist, the top 3 hits are brought back. If the 
first hit does not match with user's input, the program will ask for clarification on the 
artist name and print out the top 3 artists.

