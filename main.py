import discord
import random
import os
from googleapiclient.discovery import build

client = discord.Client()
DISCORD_TOKEN = os.getenv('DISCORD_API_KEY')
GOOGLE_TOKEN = os.getenv('GOOGLE_API_KEY')


@client.event  # startup
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# Function that will take in a youtube channel's ID and randomly print one of their video's URL into discord channel
async def print_random_video(message, channelID):
    youtube = build('youtube', 'v3', developerKey=GOOGLE_TOKEN)
    request = youtube.channels().list(part='contentDetails',
                                      id=channelID)  # First request retrieves the upload playlist ID, which holds every single upload of a youtube channel
    response = request.execute()

    playlistID = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']  # Grab Upload playlist ID
    request = youtube.playlistItems().list(part="contentDetails", playlistId=playlistID,
                                           maxResults=50)  # Second request retrieves the videoIDs found within the uploads playlist
    response = request.execute()

    uploadList = []  # Hold every upload ID within the upload playlist

    for i in response['items']:
        if i['kind'] == "youtube#playlistItem":
            uploadList.append(i['contentDetails']['videoId'])

    nextPageToken = response['nextPageToken']  # Grab page token for the next set of 50 videos

    request = youtube.playlistItems().list(part="contentDetails", playlistId=playlistID, maxResults=50,
                                           pageToken=nextPageToken)  # Third request to get next set of videos
    response = request.execute()
    for i in response['items']:
        if i['kind'] == "youtube#playlistItem":
            uploadList.append(i['contentDetails']['videoId'])

    totalUploads = response['pageInfo']['totalResults']  # Total uploads on the channel
    print("size of uploadList: ", len(uploadList))  # Check to see how big the random video pool is

    # Prints the total uploads of the channel along with the random video
    await message.channel.send("This channel has " + str(
        totalUploads) + " uploads. Here's one: \n" "https://www.youtube.com/watch?v=" + random.choice(uploadList))


@client.event  # Bot responding to specific strings or commands from users
async def on_message(message):
    if message.author.bot:  # Ensure the bot isn't responding to itself
        return

    userInput = message.content.split()

    if userInput[0] == "!joey":
        joeysID = "UCC9uqoIkY8Nd7J9Gnk98W1w"  # Unique YouTube Channel identifiers
        await print_random_video(message, joeysID)

    if userInput[0] == "!chugs":
        chugsID = "UCIvMEZips_QKqajfXGY_C5Q"
        await print_random_video(message, chugsID)


# end
client.run(DISCORD_TOKEN)
