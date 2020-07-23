import random
import requests
import re
import xml.etree.ElementTree as ET
from TenhouDecoder import getGameObject
import hashlib

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class GameInstance(metaclass=Singleton):
    
    def __init__(self):
        self.MAX_PLAYERS = 4 # WARNING NEVER EVER SET TO 3!
        self.waiting = []
        self.lastError = ""
        self.players = {}
        self.rules = "000B"
        self.rules_traslations = ["","","","",
                      "","Shugi 5000","Shugi 2000","Show Tsumokiri",
                      "","3+5","","3Player",
                      "Full Hanchan","No Kuitan","No Aka dora","Always on?"][::-1]

    def reset(self):
        self.waiting = []
        self.lastError = ""
        self.players = {}
        self.rules = "000B"

    def translateRules(self):
        rules = int(self.rules,16)
        ret = ""
        for i in range(16):
            ret += self.rules_traslations[i] + " "
            if rules&1:
                ret += "True"
            else:
                ret += "False"
            ret += "\n"
            rules = rules >> 1
        return ret

    def parseGame(self,log):
        rex = re.search("log=(.*)[&]{0,1}",log)
        if rex == None:
            self.lastError = "Invalid log URL"
            return 1
        try:
            rex = rex.group(1).split("&")[0]
        except:
            self.lastError = "Some error parsing log URL"
            return 1
            
        game = getGameObject(log)
        names = [n.name for n in game.players]
        owari = [j for i,j in  enumerate(game.owari.split(",")) if i % 2 == 0][:self.MAX_PLAYERS]
        #import pdb
        #pdb.set_trace()
        ret = []
        for i,score in enumerate(owari):
            ret.append([(float(score)/10)-30,names[i]])
        above = len([i for i in ret if i[0] >= 0])
        ret.sort()
        ret = ret[::-1]
        uma = []
        if above == 1:
            uma = [+12,-1,-3,-8]
        if above == 2:
            uma = [+8 ,+4,-4,-8]
        if above == 3:
            uma = [+8 ,+3,+1,-8]
        if above == 4:
            uma = [+8,+4,-4,-8]
        for i,j in enumerate(uma):
            ret[i][0] = ret[i][0] + j

        self.lastError = ret
        return 0
