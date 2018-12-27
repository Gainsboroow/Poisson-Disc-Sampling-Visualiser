"""
Poisson Disc Sampling Visualiser
Created by Gainsboroow 
Github : https://github.com/Gainsboroow
Github Repository : https://github.com/Gainsboroow/Poisson-Disc-Sampling-Visualiser

How to use : 
Press any key or Right Click to start.
"""

from tkinter import *
from math import *

from random import *

height = 600
width = 1200

window = Tk()
window.title("Poisson Disc Sampling")
window.geometry(str(width)+"x"+str(height)+"+0+0")

canvas = Canvas(window, bg = "black")
canvas.place(x=0,y=0, width = width, height = height)


ovalDiameter = 3
r = 15 #Minimum Distance Between 2 samples
k = 30 #Number of samples to choose before rejection
sideSize = r / sqrt(2) #Grid Case Size


grid = [ [-1 for i in range(int(width//sideSize)+1)] for a in range(int(height//sideSize)+1) ]
activeList = [0]

def generate(event):
    global canvas, grid, activeList
    print("Start")

    canvas.destroy()
    canvas = Canvas(window, bg = "black")
    canvas.place(x=0,y=0, width = width, height = height)

    grid = [ [-1 for i in range(int(width//sideSize)+1)] for a in range(int(height//sideSize)+1) ]

    #x,y = (random()*width, random()*height)
    x,y = event.x, event.y 

    samples = [ (x,y) ]
    activeList = [0]
    grid[int(y // sideSize)][int(x // sideSize)] = 0

    canvas.create_oval(x-ovalDiameter, y-ovalDiameter, x+ovalDiameter, y+ovalDiameter, fill = 'red')

    def check(x,y):

        if not( 0 <= x < width and 0 <= y < height) : return False 
        if grid[int(y//sideSize)][int(x//sideSize)] != -1:
            return False
        
        ligMin = int(max(0,y//sideSize-2))
        ligMax = int( min(height//sideSize, y//sideSize+3) )
        colMin = int(max(0,x//sideSize-2))
        colMax = int( min(width//sideSize, x//sideSize+3) )

        for lig in range(ligMin, ligMax):
            for col in range(colMin,colMax):
                if grid[lig][col] != -1:
                    index = grid[lig][col]
                    distance = (x-samples[index][0])**2 + (y-samples[index][1])**2
                    if distance <= r**2:
                        return False
        
        return True

    while len(activeList):
        index = choice(activeList)
        sampleX, sampleY = samples[index][0], samples[index][1]
        
        foundSample = False

        for i in range(k):
            angle = random()*2*pi
            distance = r*random()+r
            x, y = sampleX + distance * cos(angle), sampleY + distance * sin(angle)

            if check(x,y):
                grid[int(y // sideSize)][int(x // sideSize)] = len(samples)
                activeList.append(len(samples))
                samples.append((x,y))
                foundSample = True
                canvas.create_oval(x-ovalDiameter, y-ovalDiameter, x+ovalDiameter, y+ovalDiameter, fill = 'red')
                
                
        if not(foundSample):
            canvas.create_oval(sampleX-ovalDiameter, sampleY-ovalDiameter, sampleX+ovalDiameter, sampleY+ovalDiameter, fill = 'green')
            activeList.remove(index)
        
        canvas.update()

    print("Done")

window.bind("<KeyPress>", generate)
window.bind("<Button-3>", generate)

window.mainloop()
