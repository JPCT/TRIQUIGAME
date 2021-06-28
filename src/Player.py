import uuid
import json
from pathlib import Path

class Player():
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.totalPoints = 0
        self.totalWins = 0
        self.totalLoses = 0

    def saveData(self, win, bot=None):
        my_data = {
            "id": self.id,
            "name": self.name,
            "totalPoints": self.totalPoints,
            "totalWins": self.totalWins,
            "totalLoses": self.totalLoses
        }

        path = Path("data/playersData.json")
        
        if path.exists():
            with open(path) as fp:
                data = json.load(fp)
                existsPlayer = False
                for i in data:
                    if i["name"] == self.name:
                        if bot == None:
                            i["totalPoints"] = i["totalPoints"] + 100 if win else i["totalPoints"] + 20
                        elif bot == True:
                            i["totalPoints"] = i["totalPoints"] + 30 if win else i["totalPoints"] - 20
                        i["totalWins"] = i["totalWins"] + 1 if win else i["totalWins"]
                        i["totalLoses"] = i["totalLoses"] + 1 if not win else i["totalLoses"]
                        existsPlayer = True
                if existsPlayer == False:
                    data.append(my_data)

            with open(path, 'w') as f:
                json.dump(data, f, ensure_ascii=False,indent=4)
        else:
            with open(path, 'w') as f:
                json.dump([my_data], f, ensure_ascii=False,indent=4)
        