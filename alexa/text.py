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


def helpWithQuizMessage(artistName):
    return "You can say Start Quiz to start the quiz. Alternatively, you can say the name of another artist if you wish to change from " + artistName
