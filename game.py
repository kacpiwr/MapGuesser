import random
import turtle
import json
import urllib.request
from re import X
import time
from turtle import Turtle, Screen, pen, pendown, screensize
import tkinter as tk
from tkinter import ttk


def initTurtle():
    screen = Screen()
    screen.tracer(8, 25)
    screen.bgcolor('lightblue')
    screen.setworldcoordinates(-500, -500, 500, 500)
    return screen


class Loader:
    url = "https://raw.githubusercontent.com/mledoze/countries/master"

    def __init__(self):
        countries_json = json.load(
            urllib.request.urlopen(f"{self.url}/dist/countries.json"))

        self.countries = [[all['translations']['pol']['common'], all['cca3'].lower()] for all in countries_json]

    def get_map(self):
        number = random.randint(0, len(self.countries))
        # number=100
        return (json.load(urllib.request.urlopen(
            f"{self.url}/data/{self.countries[number][1]}.geo.json")),
                self.countries[number][0])


class Map:

    def __init__(self, screen):
        self.stop = False
        self.index = 0
        self.list = []
        self.proba = 1
        self.country = 0
        self.stoprocent = 0
        self.wynikprocent = 0
        self.loader = Loader()
        self.screen = screen
        self.turtle = Turtle()

    def stop_run(self):
        self.stop = not self.stop
        self.draw()

    def draw(self):
        if self.index >= len(self.list):
            self.loser()
        elif not self.stop:

            i = self.list[self.index]
            if i[2]:
                self.turtle.pendown()
            else:
                self.turtle.penup()
            (x, y) = (i[0], i[1])
            x = float(x)
            y = float(y)

            x = (x - self.min[0]) * self.scale / 2 - (self.maks[0] - self.min[0]) * self.scale / 2
            y = (y - self.min[1]) * self.scale - (self.maks[1] - self.min[1]) * self.scale / 2
            self.turtle.goto(x, y)
            self.turtle.pendown()
            self.wynikprocent += 1
            self.index += 1
            self.screen.ontimer(self.draw, 10)
        else:
            self.reading()

    def skalowanie(self, my_data):

        maks = [-1000000.0, -10000.0]
        min = [1000000.0, 10000000.0]
        i = 0
        draw = True
        for feature in my_data['features']:

            if feature['geometry']['type'] == 'Polygon':
                for polygon in feature['geometry']['coordinates']:
                    draw = False
                    for coordinate in polygon:
                        (x, y) = coordinate
                        a = "{}, {}".format(x, y)
                        if maks[0] is None or x > maks[0]:
                            maks[0] = x
                        if maks[1] is None or y > maks[1]:
                            maks[1] = y
                        if min[0] is None or x < min[0]:
                            min[0] = x
                        if min[1] is None or y < min[1]:
                            min[1] = y
                        self.stoprocent += 1
                        self.list.append([x, y, draw])
                        draw = True

            if feature['geometry']['type'] == 'MultiPolygon':
                for multi_polygon in feature['geometry']['coordinates']:
                    for polygon in multi_polygon:
                        draw = False
                        for coordinate in polygon:
                            (x, y) = coordinate
                            a = "{}, {}".format(x, y)
                            if maks[0] is None or x > maks[0]:
                                maks[0] = x
                            if maks[1] is None or y > maks[1]:
                                maks[1] = y
                            if min[0] is None or x < min[0]:
                                min[0] = x
                            if min[1] is None or y < min[1]:
                                min[1] = y
                            self.list.append([x, y, draw])
                            draw = True
        scale_x = maks[0] - min[0]
        scale_y = maks[1] - min[1]
        scale = scale_x if scale_x > scale_y else scale_y
        scale = 600 / scale
        return scale, maks, min

    def ok(self):
        if self.proba < 3:
            self.winner()
        else:
            self.loser()

    def no(self):
        if self.proba < 3:
            i = 3 - self.proba
            lives.config(text=f"Lives={i}")
        else:
            self.loser()

    def loser(self):
        self.stop = True
        self.turtle.penup()
        self.turtle.goto(0, 0)
        self.turtle.color("red")
        self.turtle.write(f"LOSER!\n{self.country}", True, align="center", font=('Arial', 20, 'bold'))
        # del mapa

    def winner(self):
        self.stop = True
        self.turtle.penup()
        self.turtle.goto(0, 0)
        self.turtle.color("green")
        self.turtle.write("WINNER WINNER\nCHICKEN DINNER!", True, align="center", font=('Arial', 20, 'bold'))
        # del mapa

    def gra(self):
        self.turtle.color("black")

        (my_data, selected) = self.loader.get_map()
        self.stoprocent = 0
        self.wynikprocent = 0

        self.country = selected.upper()
        self.turtle.penup()

        self.turtle.color("black")
        self.screen.clearscreen()
        self.stop = False
        self.index = 0
        self.list = []
        self.proba = 1

        (self.scale, self.maks, self.min) = self.skalowanie(my_data)

        proba = 0
        self.turtle.down()
        spacja = int(0)
        self.turtle.penup()
        graj = 0
        i = 0

        self.draw()

    def reading(self):

        self.answer = textBox.get('1.0', tk.END)
        self.answer = (self.answer.replace('\n', '')).upper()

        if self.answer == self.country:
            self.ok()
        elif self.answer != "":
            self.no()
            self.proba += 1
        textBox.delete('1.0', tk.END)


def startgra():
    turtle.penup()
    turtle.goto(0, 0)
    turtle.clearscreen()
    mapa = Map(screen)
    mapa.gra()


screen = initTurtle()
turtle.clearscreen()
mapa = Map(screen)
button = tk.Button(screen.getcanvas().master, text="Stop", height=1, width=10, command=mapa.stop_run)
button.pack()
read = tk.Button(screen.getcanvas().master, text="Read", height=1, width=10, command=mapa.reading)
read.pack()
button.place(relx=0.43, rely=0.8)
read.place(relx=0.43, rely=0.75)
textBox = tk.Text(screen.getcanvas().master, height=2, width=20)
textBox.pack()
textBox.place(relx=0.4, rely=0.87)
lives = tk.Label(screen.getcanvas().master, text="Lives=3", height=2, width=20)
lives.pack()
lives.place(relx=0.4, rely=0.07)
start = tk.Button(screen.getcanvas().master, text="Start", height=1, width=10, command=mapa.gra)
start.pack()
start.place(relx=0, rely=0.5)

screen.listen()
screen.mainloop()


