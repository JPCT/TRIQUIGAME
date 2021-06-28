import uuid
from datetime import date
import random

class MatchPvsP():
    def __init__(self, player1, player2):
        self.id = str(uuid.uuid4())
        self.beginDate = date.today()
        self.endDate = date.min
        self.player1 = player1
        self.player2 = player2
        self.nextTurn = random.randint(1,2)
        self.player1Score = 0
        self.player2Score = 0
        symbolX = random.randint(1,2)
        self.player1Symbol = "X" if symbolX == 1 else "O"
        self.player2Symbol = "X" if symbolX == 2 else "O"
        self.lastWin = None

    def verifyIfWinner(self, data):
        symbols = ["X","O"]

        for i in symbols:
            #WIN FIRST LINE
            if data[0] == i and data[1] == i and data[2] == i:
                return (i,1)
            #WIN SECOND LINE
            if data[3] == i and data[4] == i and data[5] == i:
                return (i,2)
            #WIN THIRD LINE
            if data[6] == i and data[7] == i and data[8] == i:
                return (i,3)
            #WIN FIRST COLUMN
            if data[0] == i and data[3] == i and data[6] == i:
                return (i,4)
            #WIN SECOND COLUMN
            if data[1] == i and data[4] == i and data[7] == i:
                return (i,5)
            #WIN THIRD COLUMN
            if data[2] == i and data[5] == i and data[8] == i:
                return (i,6)
            #WIN CROSSLINE FROM LEFTTOP TO RIGHTBOTTOM
            if data[0] == i and data[4] == i and data[8] == i:
                return (i,7)
            #WIN CROSSLINE FROM RIGHTTOP TO LEFTBOTTOM
            if data[2] == i and data[4] == i and data[6] == i:
                return (i,8)

            finished = True
            for j in data:
                if j == "":
                    finished = False
            if finished == True:
                return ("-", 0)