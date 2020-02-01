import turtle
class Window(object):
    def __init__(self):
        self = turtle.Screen()
        self.colormode(255)
        self.bgcolor("black")
        self.title("Boilerplate,please replace")
        self.tracer(0, 0)
        self.delay(0)
    def print(self,number):
        pen = self.turtle()
        pen.write(number)


a = Window()
a.print(5)