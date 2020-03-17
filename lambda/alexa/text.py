welcomeMessage = "Hello! Welcome to Song Match. I'll help you find the song that best defines you! Who is your favourite artist?"
welcomeReprompt = "My favourite artist is Ariana Grande. Who is your favourite?"


def capturedArtist(artistName):
    builder = "I love songs by " + artistName + " too!"
    return builder


def startQuiz(artistName):
    builder = "Now, please answer these three questions to help me match you to your " + \
        artistName + " song!"
    return builder
