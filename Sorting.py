from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
matplotlib.use("TkAgg")
from PIL import Image,ImageTk
from itertools import count
import random
import time

A = []
X = []
N = 20
title = None
sortedA = A.copy()
iteration = [0]


def swap(A, i, j):
    """Helper function to swap elements i and j of list A."""

    if i != j:
        A[i], A[j] = A[j], A[i]

def bubblesort(A):
    """In-place bubble sort."""

    if len(A) == 1:
        return

    swapped = True
    for i in range(len(A) - 1):
        if not swapped:
            break
        swapped = False
        for j in range(len(A) - 1 - i):
            if A[j] > A[j + 1]:
                swap(A, j, j + 1)
                swapped = True
            yield A

def insertionsort(A):
    """In-place insertion sort."""

    for i in range(1, len(A)):
        j = i
        while j > 0 and A[j] < A[j - 1]:
            swap(A, j, j - 1)
            j -= 1
            yield A

def mergesort(A, start, end):
    """Merge sort."""

    if end <= start:
        return

    mid = start + ((end - start + 1) // 2) - 1
    yield from mergesort(A, start, mid)
    yield from mergesort(A, mid + 1, end)
    yield from merge(A, start, mid, end)
    yield A

def merge(A, start, mid, end):
    """Helper function for merge sort."""
    
    merged = []
    leftIdx = start
    rightIdx = mid + 1

    while leftIdx <= mid and rightIdx <= end:
        if A[leftIdx] < A[rightIdx]:
            merged.append(A[leftIdx])
            leftIdx += 1
        else:
            merged.append(A[rightIdx])
            rightIdx += 1

    while leftIdx <= mid:
        merged.append(A[leftIdx])
        leftIdx += 1

    while rightIdx <= end:
        merged.append(A[rightIdx])
        rightIdx += 1

    for i, sorted_val in enumerate(merged):
        A[start + i] = sorted_val
        yield A

def quicksort(A, start, end):
    """In-place quicksort."""

    if start >= end:
        return

    pivot = A[end]
    pivotIdx = start

    for i in range(start, end):
        if A[i] < pivot:
            swap(A, i, pivotIdx)
            pivotIdx += 1
        yield A
    swap(A, end, pivotIdx)
    yield A

    yield from quicksort(A, start, pivotIdx - 1)
    yield from quicksort(A, pivotIdx + 1, end)

def selectionsort(A):
    """In-place selection sort."""
    if len(A) == 1:
        return

    for i in range(len(A)):
        # Find minimum unsorted value.
        minVal = A[i]
        minIdx = i
        for j in range(i, len(A)):
            if A[j] < minVal:
                minVal = A[j]
                minIdx = j
            yield A
        swap(A, i, minIdx)
        yield A

class ImageLabel(Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

def generateNewFrame():
    mainFrame.pack_forget()
    r.config(bg="#fffdf4")
    displayFrame.pack()

def displayGraph(method):

    displayFrame.pack_forget()
    
    global A,X,N,sortedA,title

    if number != "":
        N = number.get()
    if method == "b":
        title = "Bubble sort"
        generator = bubblesort(A)
    elif method == "i":
        title = "Insertion sort"
        generator = insertionsort(A)
    elif method == "m":
        title = "Merge sort"
        generator = mergesort(A, 0, N - 1)
    elif method == "q":
        title = "Quicksort"
        generator = quicksort(A, 0, N - 1)
    elif method == "s":
        title = "Selection sort"
        generator = selectionsort(A)
    else:
        return

    N = int(number.get())
    if v1.get() == 1:
        for i in range(N):
            X.append(i)
            A.append(random.randint(1,100))
    else:
        try:
            listArray = array.get()
            listArray = listArray.split(",")
            for i in range(len(listArray)):
                A.append(listArray[i])
                X.append(i)
            N = len(A)
        except Exception:
            messagebox.showerror("ERROR","Invalid Input")

    
    sortedA = A.copy()
    sortedA.sort()

    ax.set_title(title)
    bar_rects = ax.bar(X, A, align="edge")
    ax.set_xlim(0, N)
    ax.set_ylim(0, 100)
    ax.autoscale(False)
    anim = animation.FuncAnimation(fig, func=update_fig,fargs=(bar_rects, iteration), frames=generator, interval=10,repeat=False)

    plt.show()


def update_fig(A, _, iteration):
    iteration[0] += 1
  
    if A == sortedA:
        ax.clear()
        ax.bar(X, A, color="#68946C",label="Number of operations:" + str(iteration[0]))
        ax.set_yticks([])
        ax.set_xticks(X)
        ax.set_title(title, size = 20)
        ax.legend()
    else:
        ax.clear()
        ax.bar(X, A, color="#ff7f7f",label="Number of operations:" + str(iteration[0]))
        ax.set_yticks([])
        ax.set_xticks(X)
        ax.set_title(title, size = 20)
        ax.legend()
        if N>30:
            for number in range(len(A)):
                ax.text(number, A[number], A[number], horizontalalignment = "center", va="bottom", fontsize=(13*25)//N)
            return
    for number in range(len(A)):
        ax.text(number, A[number], A[number], horizontalalignment = "center", va="bottom", fontsize=13)
r = Tk()
r.config(bg="#f0f0f0")

fig, ax = plt.subplots(figsize=(10, 7))


mainFrame = Frame(bg="#f0f0f0")

gifLabel = ImageLabel(mainFrame,borderwidth=0)
gifLabel.grid(row=0,rowspan=2)
gifLabel.load('UI_Images/chart5.gif')

imgTitle = ImageTk.PhotoImage(Image.open("UI_Images/Title.jpg"))
titleLabel = Label(mainFrame,image = imgTitle)
titleLabel.grid(row=2)

imgStart = ImageTk.PhotoImage(Image.open("StartButton.jpg"))
startButton = Button(mainFrame,image= imgStart,borderwidth=0,bg= "#f0f0f0",activebackground="#f0f0f0",highlightthickness = 0, bd = 0, command = generateNewFrame)
startButton.grid(row=3)

mainFrame.pack()


#DISPLAY FRAME


displayFrame = Frame(r)
displayFrame.config(bg="#fffdf4")
v1 = IntVar(None,1)
large_font = ('Verdana',15)
array = StringVar()
number = IntVar(None,10)

imgNOI = ImageTk.PhotoImage(Image.open("UI_Images/NumberOfElements.jpg"))
sizeLabel = Label(displayFrame,image = imgNOI,bg="white",borderwidth=0)
sizeLabel.grid(row=0,column=1,columnspan=7)

enterNumber = Entry(displayFrame,textvariable = number,font = ('Verdana',15),width = 3,highlightthickness = 0, bd = 0,bg="white",fg="#6d54e8",borderwidth=0)
enterNumber.grid(row=0,column = 6)

imgA = ImageTk.PhotoImage(Image.open("UI_Images/array.jpg"))
ALabel = Label(displayFrame,image = imgA,bg="white")
ALabel.grid(row=1,column=0,columnspan=7,rowspan=2)

s1 = Radiobutton(displayFrame,variable = v1,value = 1,bg="white")
s1.grid(row=1,column=0,columnspan=2)
s2 = Radiobutton(displayFrame,variable = v1,value = 2,bg="white")
s2.grid(row=2,column=0,columnspan=2)

imgEntry = ImageTk.PhotoImage(Image.open("UI_Images/Entry.jpg"))
entryLabel = Label(displayFrame,image = imgEntry,bg="white",borderwidth=0)
entryLabel.grid(row=3,column=1,columnspan=7)

enterArray = Entry(displayFrame,textvariable = array,font = large_font,width = 37,highlightthickness = 0, bd = 0,bg="white",fg="#6d54e8",borderwidth=0)
enterArray.grid(row=3,columnspan=7)

imgBlank = ImageTk.PhotoImage(Image.open("UI_Images/BlankArea.jpg"))
blankLabel = Label(displayFrame,image = imgBlank,bg="white",borderwidth=0)
blankLabel.grid(row=4,column=1,columnspan=7)

imgMerge = ImageTk.PhotoImage(Image.open("UI_Images/MergeSort.jpg"))
mergeSButton = Button(displayFrame,image= imgMerge,borderwidth=0,bg= "#fffdf4",activebackground="#fffdf4",highlightthickness = 0, bd = 0, command = lambda : displayGraph("m"))
mergeSButton.grid(row=5,column=1,columnspan=3)

imgQuick = ImageTk.PhotoImage(Image.open("UI_Images/QuickSort.jpg"))
quickSButton = Button(displayFrame,image= imgQuick,borderwidth=0,bg= "#fffdf4",activebackground="#fffdf4",highlightthickness = 0, bd = 0, command = lambda : displayGraph("q"))
quickSButton.grid(row=5,column=4,columnspan=3)

imgInsertion = ImageTk.PhotoImage(Image.open("UI_Images/InsertionSort.jpg"))
insertionSButton = Button(displayFrame,image= imgInsertion,borderwidth=0,bg= "#fffdf4",activebackground="#fffdf4",highlightthickness = 0, bd = 0, command = lambda : displayGraph("i"))
insertionSButton.grid(row=6,column=1,columnspan=2)

imgBubble = ImageTk.PhotoImage(Image.open("UI_Images/BubbleSort.jpg"))
bubbleSButton = Button(displayFrame,image= imgBubble,borderwidth=0,bg= "#fffdf4",activebackground="#fffdf4",highlightthickness = 0, bd = 0, command = lambda : displayGraph("b"))
bubbleSButton.grid(row=6,column=3,columnspan=2)

imgSelection = ImageTk.PhotoImage(Image.open("UI_Images/SelectionSort.jpg"))
selectionSButton = Button(displayFrame,image= imgSelection,borderwidth=0,bg= "#fffdf4",activebackground="#fffdf4",highlightthickness = 0, bd = 0, command = lambda : displayGraph("s"))
selectionSButton.grid(row=6,column=5,columnspan=2)

r.mainloop()