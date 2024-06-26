import math
import random
import pygame

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
        #return v2(int(self.x),int(self.y))
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

    def len(self):
        return math.sqrt(self.x**2 + self.y**2)

class map:
    width: int
    height: int
    content: [[0 for i in range(50)] for j in range(50)]

    def __init__(self):
        #open and load from path
        return

    def defMapFromPath(self, path:str):
        with open(path) as mapFile:
            mapStr = mapFile.read()
            self.width = int(mapStr.split("\n")[0]) -1
            self.height = int(mapStr.split("\n")[1]) -1
            self.content = [[0 for i in range(self.width)] for j in range(self.height)]
            #+2 offset
            for y in range(self.height):
                #tempLN = ""
                for x in range(self.width):
                    tempVal = mapStr.split("\n")[2+y].split(",")[x]
                    self.content[x][y] = int(tempVal)
                    #tempLN += tempVal
                    #print("x:" + str(x) + " y:" + str(y) + "  = " + tempVal)
                #print(tempLN)
            #print("\n")

        return

    def getBlock(self, positionToSearch:v2) -> bool:
        positionToSearch = positionToSearch.getRoundedPos()

        #return self.content[int(positionToSearch.x)][int(positionToSearch.y)] != 1
        if int(positionToSearch.x) < self.width and int(positionToSearch.y) < self.height:
            if int(positionToSearch.x) > 0 and int(positionToSearch.y) > 0:
                return (self.content[int(positionToSearch.x)][int(positionToSearch.y)] != 1)
        return True
    
    def setBlock(self,positionToChange:v2,ContentSet: int) -> None:
        positionToChange = positionToChange.getRoundedPos()

        #self.content[int(positionToChange.x)][int(positionToChange.y)] = ContentSet

        if int(positionToChange.x) < self.width and int(positionToChange.y) < self.height:
            if int(positionToChange.x) > 0 and int(positionToChange.y) > 0:
                self.content[int(positionToChange.x)][int(positionToChange.y)] = ContentSet

    def printMap(self) -> None:
        for y in range(self.height):
            tempLN = ""
            for x in range(self.width):
                tempLN += str(self.content[x][y])
            print(tempLN)
        print("\n")


MAX_DIS = 20
FOV = 90

def main():

    pygame.init()

    size = (800,800)

    surface = pygame.display.set_mode(size)
    
    rectColor = (200,255,200)

    #TODO
    #   do for all directions   --> make not stupid - no chance
    #   check if is block       --> done
    #   check distance          done
    #   get min                 done

    tempMap = map()
    tempMap.defMapFromPath("./file.map")
    #tempMap.printMap()

    currentAngle = 44
    printScale = 30.0
    currentPosition = v2(2,2)
    while True: # main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    currentAngle -= 5
                elif event.key == pygame.K_RIGHT:
                    currentAngle += 5
        points = [0]
        curentAngleNormal = 0
        for i in range(int(currentAngle - (FOV/2)), int(currentAngle + (FOV/2))+1):
            #print(ray(v2(2,2),i,tempMap).len())

            if(ray(currentPosition,i,tempMap).len() < 0.01):
                dis_ = (ray(currentPosition,i-2,tempMap).len() + ray(v2(2,2),i+2,tempMap).len())/2
                #hyp = 1.0/math.cos(deg2rad(curentAngleNormal-(FOV/2)))
                #dis_ = dis_ * 1.0/hyp
                points.append(dis_)
                continue

            disRay = ray(currentPosition,i,tempMap).len()
            #hyp = 1.0/math.cos(deg2rad(curentAngleNormal-(FOV/2)))
            #disRay = disRay * 1.0/hyp
            points.append(disRay)
            curentAngleNormal += 1

        for i in range(FOV):
            x_ = (i/FOV)*size[0]
            w_ = size[0]/FOV+1

            h_ = printScale*(points[i])
            """
            hMax = size[1]-2
            hMin = 5
            if h_ >= hMax:
                h_ = hMax-1
            pre = h_ / hMax
            pre = 1 - pre
            h_ = pre * h_
            if h_ <= hMin:
                h_ = hMin
            """
            
            y_ = size[1]/2-(h_/2)
            pygame.draw.rect(surface, rectColor, pygame.Rect(x_, y_, w_, h_))

        pygame.display.update()

        #pygame.display.flip()

        #currentAngle += 0.1

        surface.fill((0,0,0))

    return

def ray(startPos: v2, angleInput: float, mapInput:map) -> v2:

    #found hits
    found = []

    while(angleInput < 0.0):
        angleInput = 360.0 + angleInput

    #view angle 0..360
    #angle = 135
    angle = angleInput % 360
    if angle % 90 == 0:
        return v2(0,0)

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
