import math
import random
#import pygame

class v3:
    x: float
    y: float
    z: float
    def __init__(self,xIn,yIn,zIn):
        self.x = xIn
        self.y = yIn
        self.z = zIn

class v2:
    x: float
    y: float
    def __init__(self,xIn,yIn):
        self.x = xIn
        self.y = yIn

    def print(self):
        print("x:\t"+ str(self.x) + "\t y:\t" + str(self.y))

    def getRoundedPos(self):
        if float(self.x)%1.0 == 0:
            tempX = self.x
        else:
            tempX = (self.x - (float(self.x)%1.0)) + 1

        if float(self.y)%1.0 == 0:
            tempY = self.y
        else:
            tempY = (self.y - (float(self.y)%1.0)) + 1

        return v2(tempX,tempY)
    
    def setRoundedPos(self):
        self.x = self.getRoundedPos().x
        self.y = self.getRoundedPos().y
        return

class map:
    width: int
    height: int
    content: [[int]]
    def __init__(self):
        #open and load from path
        return

    def defMapFromPath(self, path:str):
        with open(path) as mapFile:
            mapStr = mapFile.read()
            self.width = int(mapStr.split("\n")[0]) -1
            self.height = int(mapStr.split("\n")[1]) -1
            mapStr = mapStr.split("\n")[2]
            self.content = [[0] * self.height] * self.width
            mapArray = mapStr.split(",")
            for y in range(self.height):
                for x in range(self.width):
                    self.content[x][y] = int(mapArray[self.width * y + x])
        return

    def getBlock(self, positionToSearch:v2) -> bool:
        #positionToSearch = positionToSearch.getRoundedPos()

        #return self.content[int(positionToSearch.x)][int(positionToSearch.y)] != 1
        if int(positionToSearch.x) < self.width and int(positionToSearch.y) < self.height:
            return (self.content[int(positionToSearch.x)][int(positionToSearch.y)] != 1)
    
    def setBlock(self,positionToChange:v2,ContentSet: int) -> None:
        positionToChange = positionToChange.getRoundedPos()

        self.content[int(positionToChange.x)][int(positionToChange.y)] = ContentSet

        if int(positionToChange.x) < self.width and int(positionToChange.y) < self.height:
            self.content[int(positionToChange.x)][int(positionToChange.y)] = ContentSet


MAX_DIS = 20

def main():

    #TODO
    #   do for all directions   --> make not stupid - no chance
    #   check if is block       --> done
    #   check distance          done
    #   get min                 done

    tempMap = map()
    tempMap.defMapFromPath(".\\file.map")
    ray(v2(2,2),45,tempMap).print()

    return

def ray(startPos: v2, angleInput: float, mapInput:map) -> v2:

    #found hits
    found = []

    #view angle 0..360
    angle = 135
    angle = angleInput % 360
    if angle & 90 == 0:
        return

    #current found hit
    pos = v2(0,0)

    if angle >= 0.0 and angle < 90.0:
        #quadrant 1 (+x,+y)

        #vertical hit
        for xIter in range(startPos.x,startPos.x+MAX_DIS):
            pos.x = float(xIter)
            pos.y = math.tan(deg2rad(angle)) * (xIter-startPos.x)
            pos.y += float(startPos.y)
            #pos.print()
            found.append(v2(pos.x,pos.y))

        #horizontal hit
        for yIter in range(startPos.y,startPos.y+MAX_DIS):
            pos.y = float(yIter)
            pos.x = float(yIter-startPos.y)/math.tan(deg2rad(angle))
            pos.x += float(startPos.x)
            #pos.print()
            found.append(v2(pos.x,pos.y))

    elif angle >= 90.0 and angle < 180.0:
        #quadrant 2 (-x,+y)

        #vertical hit
        for xIter in range(startPos.x,startPos.x+MAX_DIS):
            pos.x = float(startPos.x - (xIter - startPos.x))
            pos.y = math.tan(deg2rad(angle)) * ((xIter-startPos.x)*-1)
            pos.y += float(startPos.y)
            #pos.print()
            found.append(v2(pos.x,pos.y))

        #horizontal hit
        for yIter in range(startPos.y,startPos.y+MAX_DIS):
            pos.y = float(yIter)
            pos.x = float(yIter-startPos.y)/math.tan(deg2rad(angle))
            pos.x += float(startPos.x)
            #pos.print()
            found.append(v2(pos.x,pos.y))

    elif angle >= 180.0 and angle < 270.0:
        #quadrant 3 (-x,-y)
        
        #vertical hit
        for xIter in range(startPos.x,startPos.x+MAX_DIS):
            pos.x = float(startPos.x - (xIter - startPos.x))
            pos.y = math.tan(deg2rad(angle)) * ((xIter-startPos.x)*-1)
            pos.y += float(startPos.y)
            #pos.print()
            found.append(v2(pos.x,pos.y))

        #horizontal hit
        for yIter in range(startPos.y,startPos.y+MAX_DIS):
            pos.y = float(startPos.y - (yIter - startPos.y))
            pos.x = (float(yIter-startPos.y)*-1)/math.tan(deg2rad(angle))
            pos.x += float(startPos.x)
            #pos.print()
            found.append(v2(pos.x,pos.y))

    elif angle >= 270.0 and angle < 360.0:
        #quadrant 4 (+x,-y)
        
        for xIter in range(startPos.x,startPos.x+MAX_DIS):
            pos.x = float(xIter)
            pos.y = math.tan(deg2rad(angle)) * (xIter-startPos.x)
            pos.y += float(startPos.y)
            #pos.print()
            found.append(v2(pos.x,pos.y))

        #horizontal hit
        for yIter in range(startPos.y,startPos.y+MAX_DIS):
            pos.y = float(startPos.y - (yIter - startPos.y))
            pos.x = (float(yIter-startPos.y)*-1)/math.tan(deg2rad(angle))
            pos.x += float(startPos.x)
            #pos.print()
            found.append(v2(pos.x,pos.y))

    #remove not found
    remIndx = []
    for i in range(len(found)):
        if not mapInput.getBlock(found[i]):
            remIndx.append(i)

    for i in reversed(remIndx):
        found.pop(i)

    #TODO:
    #check for hit earlier --> reduce clac
    #refactor pls

    #check min dis
    hitpos = v2(0,0)

    currentMin = MAX_DIS**2

    for i in found:
        dis = math.sqrt(i.x**2 + i.y**2)
        if dis < currentMin:
            hitpos = i
            currentMin = dis

    #print("")
    #print(currentMin)
    #hitpos.print()

    return hitpos


#MATH UTIL
def rad2deg(input: float) -> float:
    return input / (math.pi / 180.0)

def deg2rad(input: float) -> float:
    return input * (math.pi / 180.0)

if __name__ == "__main__":
    main()