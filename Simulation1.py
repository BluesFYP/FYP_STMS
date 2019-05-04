import operator
import time
import math
import pyglet
import random
from pyglet.window import Window

#load the required images
def load(filename):
    return pyglet.sprite.Sprite(pyglet.image.load("resources/"+filename))

screen = Window(1366, 700,
                resizable=True,
                caption="Traffic Simulation",
                config=pyglet.gl.Config(double_buffer=True),
                vsync=False)

background = load("background.png")
background.scale = (min(background.height, 768) /max(background.height, 768) )  #setting the scale to resize the background image to perfect size of thr disply screen

#initiating list with the names of the possible images of cars
car_images = ["red_car.png", "green_car.png", "blue_car.png"]  
truck_images =  ["truck.png"]
bike_images = ["blue_bike.png","yellow_bike.png"]
bus_images = ["bus.png"]

t0 = time.time()
#class for all type of vehicles
class Vehicle:
    def __init__(self, vehicle_type,lane,line):
        global car_images #use the globaly defined list of cars
        global  truck_images # use the globaly defined truck images
        self.vehicle_type = vehicle_type #initiate the car type
        self.lane1 = lane #set the lane of vehicle
        if  vehicle_type == "truck":
            self.car = load(random.choice(truck_images))
        elif vehicle_type == "car":
            self.car = load(random.choice(car_images))
        elif vehicle_type == "bike":
            self.car = load(random.choice(bike_images))
        elif vehicle_type == "bus":
            self.car = load(random.choice(bus_images))
        if vehicle_type in ["bus", "truck", "car"]:
            self.car.scale_x = 0.125 #scale the image width by the factor 
            self.car.scale_y = 0.125 #scale the image height by the factor
        else:
            self.car.scale_x = 0.2778 #scale the image of bike
            self.car.scale_y = 0.2542 #scale the image of the bike
        
        #setting the initial postion of vehicles for lane a
        if lane.lane == "a":
            self.car.x = 0 - (self.lane1.col*75) #setting the X cordinate of the car, 0.125*(sprite height=480) = 60 in which we are adding 15  
            self.car.y = 768-(315+(self.lane1.row*30)) #setting the Y cordinate of the car, 0.125*(sprite width=240) = 30 
            if self.lane1.row == 0: # the lane of cars from the top of the screen   
                self.lane2 = random.choice(["b", "c"])
            else:
                self.lane2 = random.choice(["c", "d"])
            self.car.rotation = 90   # the clockwise rotation of sprite for lane a   
            self.lane1.col += 1 # changing y position 

        #condtion for lane "b"
        elif lane.lane == "b":
            self.car.rotation = 180   # the clockwise rotation of sprite for lane b
            self.car.x = 740 + (self.lane1.row*33)      #setting the X cordinate of the car to draw the next sprite to be 33 pixels away from the first car sprite
            self.car.y = 768 + (self.lane1.col*75)  #setting the Y cordinate of the car, to start appearing behind 75 pixels of the background pixels cordinate
            if self.lane1.row == 0:    # If the cars are in the first lane that is from the right of the screen then these cars can go to following lanes 
                self.lane2 = random.choice(["a", "d"])
            else:
                self.lane2 = random.choice(["d", "c"])
            self.lane1.col += 1

        #condtion for lane "c"                
        elif lane.lane == "c":
            self.car.x = 1366 + (self.lane1.col*75) #setting the X cordinate of the car, 0.125*(sprite height=480) = 60 +15
            self.car.y = 768 -(420+(self.lane1.row*30)) #setting the Y cordinate of the car, 0.125*(sprite width=240) = 30
            if self.lane1.row == 0:
                self.lane2 = random.choice(["b", "a"])
            else:
                self.lane2 = random.choice(["a", "d"])
            self.car.rotation = -90   # the clockwise rotation of sprite for lane a
            self.lane1.col += 1 # changing y position

        #condtion for lane "d"
        elif lane.lane == "d":
            self.car.x = 635 + (self.lane1.row*33)      # setting the x  coordinate of the cr sprite to appear from the 635 pixel of the  background image with next 33 pixels away  
            self.car.y = 0 - (self.lane1.col*75)  # setting y coordinate of the car sprite to be 75 pixels behind the visible background image 
            if self.lane1.row == 0:   #
                self.lane2 = random.choice(["a", "b"])
            else:
                self.lane2 = random.choice(["b", "c"])
            self.lane1.col += 1
    
    def move(self):

        #condition when traffic is coming from lane "a"
        if self.lane1.lane == "a":
            if self.lane1.light == "red" and self.car.x < 510 and self.lane1.moving:
                self.car.x += 3
                if self.car.x >= 510:
                    self.lane1.moving = False
                    self.lane1.reached = True
            elif self.lane1.light == "green" or (self.lane1.light == "red" and self.car.x >= 530):
                #condition when destination lane is "b"
                if self.lane2 == "b":
                    if self.car.y >= 453:   #the intersection point of lane1 of car (1080 - 494 = 586)
                        if self.car.x == 668:
                            self.car.y += 3
                        elif self.car.y == 453 and self.car.x < 668:
                            if self.car.x < 628.36:
                                self.car.x += 3
                            else:
                                self.car.rotation -= 4.6
                                self.car.x += 2

                #condition when destination lane is "c"
                elif self.lane2 == "c":
                    self.car.x += 3

                #condtion when destination lane is "d"
                elif self.lane2 == "d":
                    if self.car.y <= 423:   #the intersection point of lane1 of car (1080 - 494 = 586)
                        if self.car.x >= 732:
                            self.car.y -= 3
                        elif self.car.y <= 423 and self.car.x < 732:
                            if self.car.x < 607.87:
                                self.car.x += 3
                            else:
                                self.car.x += 3.5
                                self.car.rotation += 2.5
                                self.car.y -= 0.9
        #condition when traffic is coming from lane "b"
        elif  self.lane1.lane == "b":
            if self.lane1.light == "red" and self.car.y > 550 and self.lane1.moving:
                self.car.y -= 3
                if self.car.y <= 555:
                    self.lane1.moving = False
                    self.lane1.reached = True
            elif self.lane1.light =="green" or (self.lane1.light == "red" and self.car.y < 550):
                #condition when destination lane is "b"
                if self.lane2 == "a":
                    if self.car.x <= 740:  # 740 is for setting the display sprite postion
                        if self.car.y <= 345: # 768 - 444                        
                            self.car.x -= 3
                        elif self.car.x <= 740 and self.car.y > 345:    # 768 - 423 = 345
                            if self.car.y > 423:
                                self.car.y -= 3
                            else:
                                self.car.rotation += 3.46
                                self.car.y -= 3
                                self.car.x -= 1


                #condtion when destination lane is "c"
                elif self.lane2 == "c":
                    if self.car.x >= 773:
                        if self.car.y <= 425:
                            self.car.x += 3

                        elif self.car.x >= 773 and self.car.y > 425:    # 768 - 423 = 345
                            if self.car.y > 482:
                                self.car.y -= 3
                            else:
                                self.car.y -= 2
                                self.car.rotation -= 3.17
                                self.car.x += 0.9

                #condition when destination lane is "d"
                elif self.lane2 == "d":
                    self.car.y -= 3

            #condition when traffic is coming from lane "c"
        elif self.lane1.lane == "c":
            if self.lane1.light == "red" and self.car.x > 869 and self.lane1.moving:
                self.car.x -= 3
                if self.car.x <= 878:
                    self.lane1.moving = False
                    self.lane1.reached = True
            elif self.lane1.light == "green" or (self.lane1.light == "red" and self.car.x < 875):
                #condtion when destination lane in "d"
                if self.lane2 == "d":
                    if self.car.y <= 318:   #the intersection point of lane1 of car (1080 - 494 = 586)
                        if self.car.x <= 745:
                            self.car.y -= 3
                        elif self.car.y == 318 and self.car.x > 745:
                            if self.car.x > 800:
                                self.car.x -= 3
                            else:
                                self.car.rotation -= 3.27
                                self.car.x -= 2
            
                #condtion when destination lane is "a"
                elif self.lane2 == "a":
                    self.car.x -= 3

                #condtion when destination lane is "b"
                elif self.lane2 == "b":
                    if self.car.y >= 298:   #the intersection point of lane1 of car (1080 - 494 = 586)
                        if self.car.x <= 668:
                            self.car.y += 3
                        elif self.car.y >= 298 and self.car.x > 668:
                            if self.car.x > 792:
                                self.car.x -= 3
                            else:
                                self.car.x -= 3.5
                                self.car.rotation += 2.5
                                self.car.y += 0.9
        #condition when traffic is coming from lane "d"
        elif self.lane1.lane == "d":
            if self.lane1.light == "red" and self.car.y < 210 and self.lane1.moving:
                self.car.y += 3
                if self.car.y >= 210:
                    self.lane1.moving = False
                    self.lane1.reached = True
            elif self.lane1.light =="green" or (self.lane1.light == "red" and self.car.y > 215):
                #condition when destination lane is "b"
                if self.lane2 == "a":
                    if self.car.x <= 635:  
                        if self.car.y >= 345:                       
                            self.car.x -= 3
                        elif self.car.x == 635 and self.car.y <= 345:    # 768 - 423 = 345
                            if self.car.y < 288:
                                self.car.y += 3
                            else:
                                self.car.rotation -= 4.7
                                self.car.y += 3


                #condtion when destination lane is "c"
                elif self.lane2 == "c":
                    if self.car.x >= 668:
                        if self.car.y >= 425:
                            self.car.x += 3

                        elif self.car.x >= 668 and self.car.y < 425:    # 768 - 423 = 345
                            if self.car.y < 347:
                                self.car.y += 3
                            else:
                                self.car.y += 2
                                self.car.rotation += 2.3
                                self.car.x += 0.9

                #condition when destination lane is "d"
                elif self.lane2 == "b":
                    self.car.y += 3
        return

    def draw(self):
        self.car.draw()

class lane_segment:
    def __init__(self, lane):
        self.light = "red" # to keep trck of signl setting by defut to red
        self.timer_logic = False # flg to check the logic for timer to be pre-timed or our logic 
        self.reached = False # to check hs the crs reched the zebr crossing when signl is red

        #loading sprites for signal lights and storing them in a list
        self.lights = []
        self.lights.append(load("green_light.png"))
        self.lights.append(load("red_light.png"))
        
        scale = 0.03 #factor to scale down the sprite of light to appropriate size
        self.lane = lane # it is a string tht keep track of the name of the lane 
        self.moving = True # to mke the crs rech zebr crossing while the signl is red
        self.col = 1 # for positioing of the car
        self.row = 0
        self.count = 0
        self.t0 = 0
        self.t1 = 0

        #setting the x-axix, y-axis, and rotation according the lane
        if lane == "a": 
            if self.timer_logic:
                self.t0 = 10
                self.t1 = 10
            self.l_x = 10
            self.l_y = 650
            x = 563.475
            y = 244.622
            rotation = -90
        elif lane == "b":
            if self.timer_logic:
                self.t0 = 20
                self.t1 = 10
            self.l_x = 872
            self.l_y = 650
            x = 844.50
            y = 244.622
            rotation = 0
        elif lane == "c":
            if self.timer_logic:
                self.t0 = 30
                self.t1 = 10
            self.l_x = 872
            self.l_y = 35
            x = 844.50
            y = 516.26
            rotation = 90                                            
        elif lane == "d":
            if self.timer_logic:
                self.t0 = 40
                self.t1 = 10
            self.l_x = 10
            self.l_y = 35
            x = 563.475
            y = 516.26
            rotation = 180
        for i in self.lights:
                i.x = x
                i.y = 768-y
                i.rotation = rotation
                i.scale = scale
        self.label = pyglet.text.Label("", font_name = "Castellar", font_size = 20, x = self.l_x, y = self.l_y, color = (255,255,255,255), bold = True)
        self.label_time = pyglet.text.Label("", font_name = "Castellar", font_size = 20, x = self.l_x, y = self.l_y-25, color = (255,255,255,255), bold = True)

    def draw(self):
        global check
        global count
        if self.light == "red":
            self.lights[1].draw()
        else:
            self.lights[0].draw()
        if check:
            if self.t0 == self.t1:
                self.light = "green"
        if self.t0 > 0 and check:
            if count == 60:
                count = 0
                self.t0 = self.t0 - 1
            else:
                count+=1
        else:
            self.light = "red"
        self.label.text = "Total vehicles on lane "+self.lane+": "+str(self.count)
        self.label_time.text = "Timer left :"+str(self.t0)+" sec"
        self.label.draw()
        self.label_time.draw()

count = 0
check = False
def on_draw():
    global lanes   
    global sarak
    global check
    check = True
    screen.clear()
    background.draw()
    for i in lanes:
        if lanes[i].reached == False:
            check = False
        lanes[i].draw()
    for i in sarak:
      for j in sarak[i]:
          if (j.car.x > 1366 or j.car.y > 768 or j.car.y < 0) and j.lane1.lane == "a":
              sarak[i].remove(j)
              lanes[i].count -= 1
          elif (j.car.x < 0 or j.car.x > 1366 or j.car.y < 0) and j.lane1.lane == "b":
              sarak[i].remove(j)
              lanes[i].count -= 1
          elif (j.car.x < 0 or j.car.y > 768 or j.car.y < 0) and j.lane1.lane == "c":
              sarak[i].remove(j)
              lanes[i].count -= 1
          elif (j.car.x < 0 or j.car.x > 1366 or j.car.y > 768) and j.lane1.lane == "d":
              sarak[i].remove(j)
              lanes[i].count -= 1
          else:
              j.move()
              j.draw()

sarak = {} #is a dictionary that holds the list of vehicles for the specific lane 
lanes = {"a":0,"b":0,"c":0,"d":0}
for i in lanes:
    lanes[i] = lane_segment(i) #

def main(line1,line2,lane):
    global lanes
    global sarak
    a = [] #list to keep record of all the vehicles on specific segment

    ##populating the segment
    #populating line1 of the segment
    for i in line1:
        b = Vehicle(i,lanes[lane],"1")
        a.append(b)
    #populating line2 of the segment
    lanes[lane].row = 1 # changing the line
    lanes[lane].col = 1 # setting X to default
    for i in line2:
        b = Vehicle(i,lanes[lane],"2")
        a.append(b)
    sarak[lane] = a

def updated(dt):
    on_draw()
   
pyglet.clock.schedule_interval(updated, 1 / 60)

f = open("count1.txt")
l = ["a","b","c","d"]
j =  -1
cot = {}
for i in f.readlines():
    if i.split(" ")[0] == "file":
        a = []
        j += 1
        no = 0
    else:
        c = i.strip("\n")
        c = c.split("=")[1].split(",")
        no += len(c)
        a.append(c)
    if len(a) >=2:
        lanes[l[j]].count = no
        if no >= 37:
            no = 15
        elif no < 37 and no >= 20:
            no = 10
        else:
            no = 5
        if lanes[l[j]].timer_logic != True:
            lanes[l[j]].t1 = no
        cot[l[j]] = no
        main(a[0],a[1],l[j])

cot = dict(sorted(cot.items(), key = operator.itemgetter(1), reverse = True))

total_timer = 0
for i in cot:
    if lanes[i].timer_logic != True:
        total_timer += cot[i]
        lanes[i].t0 = total_timer

# Launch the application
pyglet.app.run()

