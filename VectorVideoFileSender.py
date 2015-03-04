__author__ = 'Gerryflap'

import threading
import math
import time
import random
import VectorConversion

class VectorVideoFileSender(object):
    def __init__(self, webSocket):
        self.webSocket = webSocket
        self.active = True
        self.file_ = open("out.vvf", "r")
        self.run()


    def run(self):
        while self.active:
            vectors = self.file_.readline()
            if vectors == "":
                self.file_.seek(0)
            else:
                self.webSocket.sendMessage(vectors)
            time.sleep(0.033)