from alexa import mongoutils
# TODO: Add SSML

# SSML Builders
excitedStart = '<amazon:emotion name="excited" intensity="medium">'
emotionEnd = '</amazon:emotion>'

# Welcome/Start Messages
welcomeMessage = "Hello! Welcome to Song Match. I'll help you find the song that best defines you! Who is your favourite artist?"
welcomeReprompt = "I'm sorry, I didn't understand you. My favourite artist is Alan Walker,  Who is your favourite?"


def capturedArtist(artistName):
    builder = excitedStart + "I love songs by " + artistName + " too!" + emotionEnd
    return builder


def startQuiz(artistName):
    builder = "Now, whenever you're ready, say Start Quiz and answer the three questions to find your " + \
        artistName + " song!"
    return builder


# Help/Error/End Messages
helpWithArtistMessage = "You can tell me the name of your favourite singer or band and I'll take note."
goodbyeMessage = "Goodbye!"
errorMessage = "Sorry, I couldn't understand what you said. Can you reformulate?"
fallbackErrorMessage = "Sorry, it seems like my dumb developer forgot to include that feature. However, for now, you can try saying Start Quiz!"


def questionHelp(artistName, questionNumber):
    if artistName[0].lower() < 'n':
        return questionHelpSet[1][questionNumber-1]
    else:
        return questionHelpSet[2][questionNumber-1]


def helpWithQuizMessage(artistName):
    return "You can say Start Quiz to start the quiz. Alternatively, you can say the name of another artist if you wish to change from " + artistName


def getQuestion(artistName, questionNumber):
    if artistName[0].lower() < 'n':
        return questionSet[1][questionNumber-1]
    else:
        return questionSet[2][questionNumber-1]


# Question Sets
questionSet = {
    1: [
        "Which hair color do you prefer, purple or red?",
        "What do you think is a better first date, a movie or a dinner?",
        "Which city would you prefer for a vacation getaway, venice or hawaii?"
    ],
    2: [
        "Which book series do you prefer, harry potter or lord of the rings?",
        "Which movie genre do you like, drama or romance?",
        "Which sport do you prefer, Soccer or football?"
    ]
}

questionHelpSet = {
    1: [
        "Sorry, that didn't sound like a valid answer, you can either say purple or red",
        "Sorry, that didn't sound like a valid answer, you can either say movie or dinner",
        "Sorry, that didn't sound like a valid answer, you can either say venice or hawaii"
    ],
    2: [
        "Sorry, that didn't sound like a valid answer, you can either say harry potter or lord of the rings",
        "Sorry, that didn't sound like a valid answer, you can either say drama or romance",
        "Sorry, that didn't sound like a valid answer, you can either say soccer or football"
    ]
}

# Scoring


def getScore(current, answer):
    answer = answer.lower()
    return current+answer


# Repeat in case someone is stuck at the end
def repeatFinal(artistName, song):
    return "Your " + artistName + " song is " + song + "."


# Fetching Song
def getFinalResponse(artistName, score):
    return mongoutils.getSongByAnswer(artistName, score)
