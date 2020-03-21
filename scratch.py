#  Scratch File to test logic


def getScore(current, answer):
    answer = answer.lower()
    score = current
    ans = ['red', 'movie', 'venice', 'harry potter', 'drama', 'soccer']
    if answer in ans:
        score.append('1')
        return score
    else:
        score.append('2')
        return score


score = getScore('', 'purple')
print(score)
