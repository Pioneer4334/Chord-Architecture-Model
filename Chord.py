# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 11:52:18 2018

@author: Pioneer
"""

import math
import random
from tkinter import *

class ChordArch:
    def __init__(self):
        self.hashTable = [False]*32
        self.h = 400
        self.k = 310
        self.r = 280
        self.win = Tk()
        self.win.title("Chord Architecture")
        self.win.state('zoomed')
        
        #Row 0
        indexFrame = Frame(self.win)
        indexFrame.grid(row=0, column=0)
        indexCanvas = Canvas(indexFrame, bg='white', width=700, height=30)
        indexCanvas.pack()
        ix = 60
        indexCanvas.create_text(30, 18, text="Index: ", font=('Helvetica', 10, 'bold'))
        indexCanvas.create_oval(ix, 10, ix+15, 25, fill="white", dash=(3, 5))
        indexCanvas.create_text(ix+52, 18, text=": Data-Item", font=('Helvetica', 10, 'bold'))
        indexCanvas.create_oval(ix+100, 10, ix+115, 25, fill="yellow", width=2)
        indexCanvas.create_text(ix+159, 18, text=": Active Node", font=('Helvetica', 10, 'bold'))
        indexCanvas.create_oval(ix+210, 10, ix+225, 25, fill="blue", dash=(3, 5))
        indexCanvas.create_text(ix+290, 18, text=": Intermediate Node", font=('Helvetica', 10, 'bold'))
        indexCanvas.create_oval(ix+365, 10, ix+380, 25, fill="green", dash=(3, 5))
        indexCanvas.create_text(ix+440, 18, text=": Result of LookUp", font=('Helvetica', 10, 'bold'))
        self.addNode = Button(self.win, text="Add Node", command=self.AddNode)
        self.addNode.grid(row=0, column=1, sticky=W)
        
        #Row 1
        Label(text="Input node ID to delete the node then press enter").grid(row=1, column=0, sticky=E)
        delFrame = Frame(self.win)
        self.deleteKey = Text(delFrame, height=1, width=5)
        #self.deleteKey.grid(row=1, column=1, sticky=W)
        self.deleteKey.bind("<Return>", self.DeleteNode)
        self.lblDelWarning = Label(delFrame, fg="red")
        #self.lblDelWarning.grid(row=1, column=1, sticky=E)
        delFrame.grid(row=1, column=1, sticky="nsew")
        self.deleteKey.pack(side="left")
        self.lblDelWarning.pack(side="left")
        
        #Row 2
        Label(text="Input data-item key for look-up then press enter").grid(row=2, column=0, sticky=E)
        lookUpFrame = Frame(self.win)
        self.lookUpKey = Text(lookUpFrame, height=1, width=5)
        self.lookUpKey.grid(row=2, column=1, sticky=W)
        self.lookUpKey.bind("<Return>", self.LookUp)
        self.lblLookUpWarning = Label(lookUpFrame, fg="red")
        lookUpFrame.grid(row=2, column=1, sticky="nsew")
        self.lookUpKey.pack(side="left")
        self.lblLookUpWarning.pack(side="left")
        self.refreshBtn = Button(self.win, text="Restore state before Look-Up", bg="green", command=self.RestoreState)
        self.refreshBtn.grid(row=2, column=2, sticky=W)
        
        #Row 3
        self.canvas = Canvas(self.win, width=900, height=800)
        self.canvas.grid(row=3, columnspan=2)
        self.tb = Text(self.win, height=39, width=50)
        self.tb.tag_configure('big', font=('Verdana', 16, 'bold'))
        self.centerText = self.canvas.create_text(self.h, self.k, text="N:5\nMaximum No of nodes: 32", width=500, justify=CENTER, font=('Helvetica', 36, 'bold'))
        
        self.Chord()
    #-------------------------------------------------------------------------------------
    
    
    def ResetWarning(self):
        self.lblDelWarning.config(text="")
        self.lblLookUpWarning.config(text="")
        self.canvas.itemconfigure(self.centerText, text="N:5\nMaximum No of nodes: 32", font=('Helvetica', 36, 'bold'))
    #-------------------------------------------------------------------------------------
    
    
    def GenerateHash(self):
        index = -1
        try:
            if self.hashTable.index(0) >= 0:
                index = random.randint(0, 31)
                while self.hashTable[index] == True:
                    index = random.randint(0, 31)
                return index * 360/32   
            else: 
                return index
        except:
            return index
    #-------------------------------------------------------------------------------------
    
    
    def MaintainOverlay(self):
        self.tb.config(state=NORMAL)
        self.tb.delete('1.0', END)
        self.tb.insert(END,'Node and Data-Item mapping\n', 'big')
        self.tb.grid(row=2, column=2)
        indexList = [x for x in range(0, 32) if self.hashTable[x] == True]
        for hashIndex in indexList:
            self.hashTable[hashIndex] = True
            prevIndex = hashIndex - 1
            degree = hashIndex * 360/32
            
            x= self.h + self.r * math.cos(math.radians(degree))
            y= self.k + self.r * math.sin(math.radians(degree))
            
            while self.hashTable[prevIndex%32] == False:
                prevIndex -= 1
                
#            overlay = "["+ str(prevIndex%32+1) + " to " + str(hashIndex) +"]"
#            ct = self.canvas.create_text(x,y-25,text=overlay)
#            cr = self.canvas.create_rectangle(self.canvas.bbox(ct),fill="white", width=2, outline="white")
            
            overlay = "Node: " + str(int(hashIndex)%32) + " Data-Item: ["+ str(int(prevIndex+1)%32) + " to " + str(int(hashIndex%32)) +"]"
            self.tb.insert(END, overlay+'\n')
        self.tb.grid(row=3, column=2, sticky=N)
        self.tb.config(state=DISABLED)
    #-------------------------------------------------------------------------------------  
        
        
    def DeleteNode(self, event):
        d = self.deleteKey.get("1.0", END)
        self.deleteKey.delete('1.0', END)
        try:
            d=int(d)
            self.RestoreState()
            if self.hashTable[d] == True:
                self.hashTable[d] = False
                degree = d * 360/32
                x = self.h + self.r * math.cos(math.radians(degree))
                y = self.k + self.r * math.sin(math.radians(degree))
                
                #Draw a data item
                self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="white", dash=(3, 5))
                self.canvas.create_text(x,y,text=int(degree*32/360))
                self.MaintainOverlay()
            else:
                self.lblDelWarning.config(text="The input key is not a node.")
        except:
            self.lblDelWarning.config(text="Please input integer value only")
    #-------------------------------------------------------------------------------------
    
    
    def RestoreState(self):
        self.ResetWarning()
        indexList = [x for x in range(0, 32) if self.hashTable[x] == True]
        for hashIndex in indexList:
            degree = hashIndex * 360/32
            x = self.h + self.r * math.cos(math.radians(degree))
            y = self.k + self.r * math.sin(math.radians(degree))
            
            #Draw a node
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="yellow", width=2)
            self.canvas.create_text(x,y,text=int(degree*32/360))
    #-------------------------------------------------------------------------------------
    
    
    def LookUp(self, event):
        self.ResetWarning()
        dk = self.lookUpKey.get("1.0", END)
        self.lookUpKey.delete('1.0', END)
        try:
            dataKey=int(dk.strip())
            self.RestoreState()
            indexList = [x for x in range(0, 32) if self.hashTable[x] == True]
            if len(indexList) > 0:
                if dataKey > indexList[-1]:
                    indexList.insert(0, indexList[0]+32)
                else:
                    indexList.append(indexList[0]+32)
            node = -1
            for hashIndex in indexList:
                degree = (hashIndex%32) * 360/32
                x = self.h + self.r * math.cos(math.radians(degree))
                y = self.k + self.r * math.sin(math.radians(degree))
                    
                if(hashIndex < dataKey):
                    self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="blue", dash=(3, 5))
                    self.canvas.create_text(x,y,text=int(degree*32/360))
                else:
                    self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="green", dash=(3, 5))
                    self.canvas.create_text(x,y,text=int(degree*32/360))
                    node = hashIndex
                    break
            if(hashIndex == -1):
                self.lblLookUpWarning.config(text="No Node found for the data-item with the provided key")
            else:
                self.canvas.itemconfigure(self.centerText, text="The node look-up starts from the node with the minimum id. \nThe blue node(s) are the intermidiate node(s) and the green node is the one which is responsible for the data-item. Here, LookUp("+str(dataKey)+")="+str(node), font=('Helvetica', 16, 'bold'))
                self.lblLookUpWarning.config(text="Data-Item key: "+str(dataKey), fg="black")
        except:
            self.lblLookUpWarning.config(text="Please input integer value only", fg="red")
    #-------------------------------------------------------------------------------------
    
    
    def AddNode(self):
        self.ResetWarning()
        degree = self.GenerateHash()
        self.RestoreState()
        if degree >= 0:
            x = self.h + self.r * math.cos(math.radians(degree))
            y = self.k + self.r * math.sin(math.radians(degree))
            
            #Draw a node
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="yellow", width=2)
            self.canvas.create_text(x,y,text=int(degree*32/360))
            hashIndex = int(degree*32/360)
            self.hashTable[hashIndex] = True
            self.MaintainOverlay()
        else:
            self.tb.config(state=NORMAL)
            self.tb.insert(END, 'Chord is full\n')
            self.tb.config(state=DISABLED)
    #-------------------------------------------------------------------------------------
    
            
    def CreateDataItem(self):
        for d in range(0, 32):
            degree = d * 360/32
            x = self.h + self.r * math.cos(math.radians(degree))
            y = self.k + self.r * math.sin(math.radians(degree))
            
            #Draw a data item
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="white", dash=(3, 5))
            self.canvas.create_text(x,y,text=int(degree*32/360))
    #-------------------------------------------------------------------------------------
    
        
    def Chord(self):
        # Draw Main Circle in Canvas
        self.canvas.create_oval(self.h-self.r, self.k-self.r, self.h+self.r, self.k+self.r)
        
        self.CreateDataItem()
        
        self.AddNode()
        
        self.win.mainloop()
    #-------------------------------------------------------------------------------------

ChordArch()
    