levelDict = { "loops": [], "operators":[]}

class level:
    def __init__(self):
        self.solution= ''
        self.exout = ''
        self.input = ''
        self.lnum = 0
        self.comment = ''
        self.func = None

    def __str__(self):
        return self.solution + " " + self.exout+ " " + self.input + " " + self.lnum + " " + self.comment

def getLevel(s,n):
    if( s == "loops"):
        if(n< len(levelDict[s])):
            return levelDict[s][n]
    elif( s== "operators"):
        if(n < len(levelDict[s])):
            return levelDict[s][n]
    l = level()
    return l

ques = level()
ques.comment = """ Addition Logic : a + b """
ques.func = lambda x,y : x + y

levelDict["operators"].append(ques)
