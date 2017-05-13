from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from time import sleep
import tweepy
import json

#Delaring some config variables
path = "/home/pi/projects/twitterFeed"
result = []
resultMessage = []
maxLineLength = 80
APIQuery = "#internetofstuff"
fontLocation = path + "/OpenSans-Semibold.ttf"
newLineSpace = 75
lineCount = 0

def exceptionHandler(exception):
    with open("errorLog.txt", "a") as errorFile:
        errorFile.write(str(exception) + "\n")
#Declaring fonts for image manipulation module
userameFont = ImageFont.truetype(font=fontLocation, size=150)
messageFont = ImageFont.truetype(font=fontLocation, size=75)

#Initialising and authenticating to Twitter API 
auth = tweepy.auth.OAuthHandler("a", "b")
auth.set_access_token("c", "d")
api = tweepy.API(auth)

while True:
    masterImg = Image.open(path + "/master.jpeg")
    width, height = masterImg.size
    try:
        APIResponse = api.search(q=APIQuery)
    except:
        exceptionHandler(sys.exc_info()[1])
    if APIResponse:
        if len(APIResponse) < 4:
            rangeValue = len(APIResponse)
        else:
            rangeValue = 4
        for tweetIndex in range(rangeValue):
            result.append(APIResponse[tweetIndex].author.screen_name)
            result.append(APIResponse[tweetIndex].text.strip())
            tweetInfo = APIResponse[tweetIndex]._json
            result.append(tweetInfo['created_at'])
        
            for lineBeginning in range(0, len(result[1]), maxLineLength):
                resultMessage.append(result[1][lineBeginning:lineBeginning + maxLineLength])
                
            draw = ImageDraw.Draw(masterImg)
            
            draw.text((25, height / 4 * tweetIndex + 25), result[0],(48,242,87), font=userameFont)
            for line in resultMessage:
                draw.text((25, height / 4 * tweetIndex + 200 + newLineSpace * lineCount), line,(57,3,255), font=messageFont)
                lineCount += 1
            draw.text((25, height / 4 * tweetIndex + (height / 4) - 125), result[2], (217,0,255), font=messageFont)
            try:
                masterImg.save(path + "/feed.jpeg")
            except:
                exceptionHandler(sys.exc_info()[1])
            result = []
            resultMessage = []
            lineCount = 0
    else:
        draw = ImageDraw.Draw(masterImg)
        draw.text((25, 0),"Post with #internetofstuff to appear hear!",(255,0,0), font=userameFont)
        try:
            masterImg.save(path + "/feed.jpeg")
        except:
            exceptionHandler(sys.exc_info()[1])

        
    sleep(15)
