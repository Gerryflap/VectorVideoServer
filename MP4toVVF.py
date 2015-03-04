__author__ = 'Gerryflap'
#This script will convert a given file to a VectorVideoFile
import subprocess as sp
import VectorConversion
import threading
from multiprocessing import Process, Queue
import time
import random
import thread
import sys

running = True
def getPixel(frame, x, y, width):
    i = (x + y*width)*3
    if(len(frame) > i+2 and x < width and x >= 0 and y >= 0):
        return (frame[i], frame[i+1], frame[i+2])
    else:
        return -1

def colorDifference(col1, col2):
    diff = 0
    for c1, c2 in zip(col1, col2):
        diff += abs(c1 - c2)
    return diff

def getPixelChaos(frame, x, y, width):
    chaos = 0
    thisColor = getPixel(frame, x ,y ,width)
    if(thisColor == -1):
        return -1
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if(dx != 0 and dy != 0):
                color = getPixel(frame, x+dx, y+dy, width)
                if(color != -1):
                    chaos += colorDifference(thisColor, color)
    return chaos

def getMaxChaos(frame, x, y, width):
    chaos = getPixelChaos(frame, x, y, width)
    maxdx = 0
    maxdy = 0
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            if(dx != 0 and dy != 0):
                tempChaos = getPixelChaos(frame, x+dx, y+dy, width)
                if(tempChaos != -1):
                    if (chaos < tempChaos):
                        maxdx = dx
                        maxdy = dy
                        chaos = tempChaos

    return maxdx, maxdy

def generateVectorFrame2(frame, width, q, maxDist, minChaos, thisframenum, outputQueue):
    #global framenum
    framenum = thisframenum
    print("Generating vector frame %i"%(thisframenum))
    vectors = []
    q = int(q)
    qs = q ** 2
    for x in range(width):
        x = x
        for y in range(len(frame)/(width)):
            y = y
            if(getPixelChaos(frame, x, y, width) > minChaos):
                vectors.append([x, y, minChaos + 1])
    print len(vectors)
    vectorFrame = VectorConversion.VectorFrame()

    finalVectors = vectors
    vectorFrame.addVector(finalVectors[0][0], finalVectors[0][1], False)
    finalVectors = finalVectors[1:]
    thisVector = finalVectors[0]
    closeEnough = False
    while len(finalVectors) > 2:
        closestDistance = 1000000000
        closestVector = [-1000, -1000]

        for vector in finalVectors:
            if(vector != thisVector):
                #Distance is used as a squared, because taking the square root only takes time and is not needed to find the closest point
                tempDist = ((vector[0] - thisVector[0])**2.0 + (vector[1] - thisVector[1])**2.0)
                if(tempDist < closestDistance and tempDist != 0):
                    closestDistance = tempDist
                    closestVector = vector
        vectorFrame.addVector(thisVector[0], thisVector[1], closeEnough and thisVector[2] > minChaos)
        closeEnough = closestDistance**0.5 < maxDist
        if(closestVector[0] != -1000):
            finalVectors.remove(thisVector)
            thisVector = closestVector
        else:
            finalVectors.remove(thisVector)
            thisVector = finalVectors[0]

    print("Done generating vector frame %i"%(thisframenum))
    outputQueue.put([thisframenum, vectorFrame.finalize()])


def generateVectorFrame(frame, width, q, maxDist, minChaos):
    vectors = []
    finalVectors = []
    q = int(q)
    for i in range(len(frame)/(3*q)):
        vectors.append([(i*q)%width, (i*q)/width])
    print len(vectors)
    vectorFrame = VectorConversion.VectorFrame()

    #decide vector points
    while len(vectors) != 0:
        toBeFinalized = []
        for vector in vectors:
            x = vector[0]
            y = vector[1]
            (dx, dy) = getMaxChaos(frame, x, y, width)
            if dx == 0 and dy == 0:
                if getPixelChaos(frame, x, y, width)>minChaos:
                    toBeFinalized.append([vector , [getPixelChaos(frame, x, y, width)]])
                else:
                    vector[0] = x + int(random.random()*4-2)
                    vector[1] = y + + int(random.random()*4-2)
            else:
                vector[0] = x + dx
                vector[1] = y + dy
        for vector in toBeFinalized:
            vectors.remove(vector[0])
            finalVectors.append(vector[0] + vector[1])

    vectorFrame.addVector(finalVectors[0][0], finalVectors[0][1], False)
    finalVectors = finalVectors[1:]
    thisVector = finalVectors[0]
    closeEnough = False
    #draw lines
    while len(finalVectors) > 2:
        closestDistance = 1000000000
        closestVector = [-1000, -1000]

        for vector in finalVectors:
            if(vector != thisVector):
                #Distance is used as a squared, because taking the square root only takes time and is not needed to find the closest point
                tempDist = ((vector[0] - thisVector[0])**2.0 + (vector[1] - thisVector[1])**2.0)
                if(tempDist < closestDistance and tempDist != 0):
                    closestDistance = tempDist
                    closestVector = vector
        vectorFrame.addVector(thisVector[0], thisVector[1], closeEnough and thisVector[2] > minChaos)
        closeEnough = closestDistance**0.5 < maxDist
        if(closestVector[0] != -1000):
            finalVectors.remove(thisVector)
            thisVector = closestVector
        else:
            finalVectors.remove(thisVector)
            thisVector = finalVectors[0]
    return vectorFrame.finalize()

def generateVectorVideoFile(outputFile, frames, width, q, maxDist, minChaos):
    print("Started generation")
    frameQueue = Queue()
    outputFrames = {}
    outputFile = open(outputFile, "w")
    print(frames)
    global running
    currentFrame = 0
    lastFrame = 0
    while running or (frames.qsize() != 0):
        if(frames.qsize() > 0):
            tempFrame = frames.get()
            print("Starting thread")
            p = Process(target=generateVectorFrame2, args=(tempFrame, width, q, maxDist, minChaos, currentFrame, frameQueue))
            p.start()
            print("Thread started!")
            currentFrame += 1
        try:
            newFrame = frameQueue.get_nowait()
            outputFrames[str(newFrame[0])] = newFrame[1]
        except Exception as e:
            pass
        if(str(lastFrame+1) in outputFrames):
            outputFrame = outputFrames.pop(str(lastFrame+1))
            outputFile.write(outputFrame+'\n')
            outputFile.flush()
            lastFrame += 1
        else:
            print(frames)
            time.sleep(0.1)
    outputFile.close()
    running = False


if __name__ == '__main__':
    #FFMPEG_BIN = "ffmpeg" # on Linux ans Mac OS
    FFMPEG_BIN = "ffmpeg.exe" # on Windows

    #fileLocation = raw_input("Video file path: ")
    command = [ FFMPEG_BIN,
                '-i',"C:\Users\Gerryflap\Pictures\\test.mov",
                '-f', 'image2pipe',
                '-pix_fmt', 'rgb24',
                '-vcodec', 'rawvideo', '-']
    #command = [ FFMPEG_BIN, '-help']
    pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
    frames = Queue()
    raw_image = " "
    framenum = 0
    outputFile = "out.vvf"
    p = Process(target=generateVectorVideoFile, args=(outputFile, frames, 360, 840, 10, 400))
    p.start()
    while(len(raw_image) != 0):
        raw_image = pipe.stdout.read(360*640*3)
        pipe.stdout.flush()
        image = []
        for char in raw_image:
            image.append(ord(char))
        frames.put(image)
    print(frames.qsize())
    while running:
        time.sleep(1)