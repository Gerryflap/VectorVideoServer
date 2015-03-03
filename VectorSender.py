__author__ = 'Gerryflap'

import threading
import math
import time
import random
import VectorConversion

def genereateMick(vectors, x, y):
    vectors.addVector(x + 0, y + 150, False)
    vectors.addVector(x + 0, y + 0, True)
    vectors.addVector(x + 50, y + 100, True)
    vectors.addVector(x + 100, y + 0, True)
    vectors.addVector(x + 100, y + 0, True)
    vectors.addVector(x + 100, y + 150, True)
    vectors.addVector(x + 150, y + 150, False)


class VectorSender(object):
    def __init__(self, webSocket):
        self.webSocket = webSocket
        self.count = 0
        self.active = True
        #self.thread = threading._start_new_thread(self.run)
        self.run()

    def run(self):
        while self.active:
            t = time.time()
            vectors = VectorConversion.VectorFrame()
            vectors.addVector(300-150*math.sin(self.count), 300-150*math.cos(self.count), False)
            vectors.addVector(300+150*math.sin(self.count), 300+150*math.cos(self.count), True)
            vectors.addVector(300+150*math.sin(self.count), 300-150*math.cos(self.count), True)
            vectors.addVector(300-150*math.sin(self.count), 300+150*math.cos(self.count), True)
            vectors.addVector(300-150*math.sin(self.count), 300-150*math.cos(self.count), True)
            #genereateMick(vectors, random.random()*600, random.random()*600)
            genereateMick(vectors, self.count*10, 100)
            self.webSocket.sendMessage(vectors.finalize())
            self.count += 0.01
            dt = time.time()-t

            time.sleep(0.013)