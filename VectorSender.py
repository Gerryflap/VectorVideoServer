__author__ = 'Gerryflap'

import threading
import math
import time
import random

class VectorSender(object):
    def __init__(self, webSocket):
        self.webSocket = webSocket
        self.count = 0
        self.active = True
        #self.thread = threading._start_new_thread(self.run)
        self.run()

    def run(self):
        while self.active:
            vectors = '['
            vectors += '{"x":%i, "y":%i, "draw":false}'%(300-150*math.sin(self.count), 300-150*math.cos(self.count))
            vectors += ', {"x":%f, "y":%f, "draw":true}'%(300+150*math.sin(self.count), 300+150*math.cos(self.count))
            vectors += ', {"x":%f, "y":%f, "draw":true}'%(300+150*math.sin(self.count), 300-150*math.cos(self.count))
            vectors += ', {"x":%f, "y":%f, "draw":true}'%(300-150*math.sin(self.count), 300+150*math.cos(self.count))
            vectors += ', {"x":%f, "y":%f, "draw":true}'%(300-150*math.sin(self.count), 300-150*math.cos(self.count))
            for i in range(int(self.count*100)):
                vectors += ', {"x":%f, "y":%f, "draw":false}'%(random.random()*600, random.random()*600)
                vectors += ', {"x":%f, "y":%f, "draw":true}'%(random.random()*600, random.random()*600)
            vectors += ']}'
            self.webSocket.sendMessage('{"type":"FRAME", "vectorData":%s'%(str(vectors)))
            self.count += 0.01
            time.sleep(0.033)