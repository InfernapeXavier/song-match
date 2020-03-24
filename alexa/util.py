import secrets
from alexa import mongoutils
import six
# TODO: Add SSML

# SSML Builders
excitedStart = '<amazon:emotion name="excited" intensity="medium">'
emotionEnd = '</amazon:emotion>'

# Welcome/Start Messages
welcomeMessage = "Hello! Welcome to Song Match. I'll help you find the song that best defines you! Who is your favourite artist?"
welcomeReprompt = "I'm sorry, I didn't understand you. My favourite artist is Alan Walker,  Who is your favourite?"


def capturedArtist(artistName):
    builder = excitedStart + "I love " + artistName + "!" + emotionEnd
    return builder


def startQuiz(artistName):
    builder = "Now, whenever you're ready, say Start Quiz to find your " + \
        artistName + " song!"
    return builder


# Help/Error/End Messages
helpWithArtistMessage = "You can tell me the name of your favourite singer or band and I'll take note."
goodbyeMessage = "Goodbye!"
errorMessage = "Sorry, I couldn't understand what you said. Can you please reformulate?"
fallbackErrorMessage = "Sorry, it seems like my dumb developer forgot to include that feature. However, for now, you can try saying Start Quiz!"
exitMessage = "To try the quiz with another artist, just say their name. To exit, say Bye!"


def questionHelp(setNumber, questionNumber):
    return questionHelpSet[setNumber][questionNumber-1]


def questionFallback(setNumber, questionNumber):
    return questionFallbackSet[setNumber][questionNumber-1]


def helpWithQuizMessage(artistName):
    return "You can say Start Quiz to start the quiz. Alternatively, you can say the name of another artist if you wish to change from " + artistName


def getQuestion(setNumber, questionNumber):
    return questionSet[setNumber][questionNumber-1]


def getQuestionSet(artistName):
    if artistName[0].lower() < "n":
        setNumber = 1
    else:
        setNumber = 2
    return setNumber


# Question Sets
questionSet = {
    1: [
        "What color do you want to dye your hair next?",
        "Which place makes a better hot chocolate, starbucks or dunkin donuts",
        "Which country is ideal for a vacation getaway?"
    ],
    2: [
        "What is the last book that you read?",
        "What is your favorite movie genre?",
        "What is your favorite sport?"
    ]
}

questionHelpSet = {
    1: [
        "You can say the name of any color",
        "You can say either starbucks or dunkin donuts",
        "You can say the name of any country"
    ],
    2: [
        "You can say the name of any book",
        "You can say whatever genre you like, for instance, Horror",
        "You can say the name of any sport like soccer or football"
    ]
}

questionFallbackSet = {
    1: [
        "Sorry, that didn't sound like a valid answer, you can say the name of any color",
        "Sorry, that didn't sound like a valid answer, you can say either starbucks or dunkin donuts",
        "Sorry, that didn't sound like a valid answer, you can say the name of any country"
    ],
    2: [
        "Sorry, that didn't sound like a valid answer, you can say the name of any book",
        "Sorry, that didn't sound like a valid answer, you can say whatever genre you like, for instance, Horror",
        "Sorry, that didn't sound like a valid answer, you can say the name of any sport like soccer or football"
    ]
}


# Scoring
def getScore(current, slots):
    score = ""
    for _, slot in six.iteritems(slots):
        if slot.value is None:
            pass
        else:
            score = current+slot.value
    return score


# Repeat in case someone is stuck at the end
def finalResponse(artistName, song):
    return "Your " + artistName + " song is " + song + "." + " " + exitMessage


# Fetching Song
def getFinalResponse(artistName, score):
    song = mongoutils.getSongByAnswer(artistName, score)
    return song
