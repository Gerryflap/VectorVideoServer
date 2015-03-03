__author__ = 'Gerryflap'

class VectorFrame(object):
    def __init__(self):
        self.string = '{"type":"FRAME", "vectorData": ['

    def addVector(self, x, y, draw):
        """x position, y position and whether or not a line is drawn from the previous point to this point"""
        self.string += '{"x":%i, "y":%i, "draw":%s}, '%(x, y, str(draw).lower())

    def finalize(self):
        return self.string[:-2] + ']}'

