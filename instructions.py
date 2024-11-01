import pygame, json, os

class Controls():
    def __init__(self):
        file = open("./Assets/config.json")
        self.data = json.load(file)
        file.close()

    def changeKey(self, player, dictKey, keyValue, keyUnicode):
        self.data[player][dictKey] = keyValue
        self.data[player]["unicode"][dictKey] = keyUnicode

        saveData = json.dumps(self.data, indent = 4)

        file = open("./Assets/config.json", "w")
        file.write(saveData)
        file.close()

    def reset(self):
        file = open("./Assets/def.json", "r")
        self.data = json.load(file)
        file.close()

        file = open("./Assets/config.json", "w")
        file.write(json.dumps(self.data, indent = 4))
        file.close()

        
