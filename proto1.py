import math
from xml.etree import ElementTree as ET
from decimal import *
from time import sleep
# import RPi.GPIO as GPIO

getcontext().prec = 6
tree = ET.parse('spline9p_newz.xml')
root = tree.getroot()

print("this is bullshit and the x y and z values")

# for child in root[1][0][2][0][0]:
#  print(child.attrib, child.tag)
x_val = []
y_val = []
z_val = []
getcontext().prec = 6
for GEO_POINT in root.iter("GEO_POINT"):
    x_val.append(GEO_POINT.attrib["x"])
    y_val.append(GEO_POINT.attrib["z"])
    z_val.append(GEO_POINT.attrib["y"])
    # elif GEO_POINT.attrib == "y":
    # y_values.append(hasattr(y))
# elif GEO_POINT.attrib == "z":
# z_value.append(hasattr(z))

# convert to float:
for index, item in enumerate(x_val):
    x_val[index] = float(item)

for index, item in enumerate(y_val):
    y_val[index] = float(item)

for index, item in enumerate(z_val):
    z_val[index] = float(item)

print(x_val)
print(y_val)
print(z_val)

xn = 0
yn = 0
zn = 0

x_distance = []
y_distance = []
z_distance = []

size_of_x_values = len(x_val)
while xn < size_of_x_values - 1:
    x_1 = x_val[xn]
    x_2 = x_val[xn + 1]
    dist_x = (x_2) - (x_1)
    #  print("Distance between", dist_x)
    x_distance.append(dist_x)
    xn += 1
print("X Distances", x_distance)

size_of_y_values = len(y_val)
while yn < size_of_y_values - 1:
    y_1 = y_val[yn]
    y_2 = y_val[yn + 1]
    dist_y = float(y_2) - float(y_1)
    #  print("Distance between", dist_y)
    y_distance.append(dist_y)
    yn += 1
print("Y Distances", y_distance)

size_of_z_values = len(z_val)
while zn < size_of_z_values - 1:
    z_1 = z_val[zn]
    z_2 = z_val[zn + 1]
    dist_z = float(z_2) - float(z_1)
    # print("Distance between", dist_z)
    z_distance.append(dist_z)
    zn += 1
print("Z Distances", z_distance)
# print("here come da feed length")
# Distances saved in x_distance, y and z_distance

feed_length = []
xy_length = []

### Feed Length ###
a = 0
while a < len(x_distance):
    x_dist = x_distance[a]
    y_dist = y_distance[a]
    z_dist = z_distance[a]
    length = math.sqrt((x_dist ** 2 + z_dist ** 2 + y_dist ** 2))
    feed_length.append(length)
    xy = math.sqrt(x_dist ** 2 + y_dist ** 2)
    xy_length.append(xy)
    a += 1
print("here come da feed length", feed_length)

xy_phi = []
orientation_xy = []
xy_degree = []
b = 0


### XY Angle and orientation
while b + 2 < len(x_val):
    # feed length for cos check!
    # spitze minus fuß!
    x1_x = (x_val[b + 1]) - (x_val[b])
    x1_y = (y_val[b + 1]) - (y_val[b])
    x2_x = (x_val[b + 1]) - (x_val[b + 2])
    x2_y = (y_val[b + 1]) - (y_val[b + 2])
    phi_rad_xy = math.acos(
        ((x1_x * x2_x + x1_y * x2_y) / (math.sqrt(x1_x ** 2 + x1_y ** 2) * math.sqrt(x2_x ** 2 + x2_y ** 2))))
    phi_xy = phi_rad_xy * 180 / math.pi
    bend_ang_xy = 180 - phi_xy
    bend_ang_rad_xy = bend_ang_xy * math.pi / 180
    if bend_ang_xy < round(180, 8):
        xy_degree.append(bend_ang_xy)
    else:
        xy_degree.append(0)
    xy_phi.append(phi_xy)  #########CHANGE BETA TO BEND ANG ! ! ! ! !#####################################################
    orthv_x = x1_y * (-1) / 10000
    orthv_y = x1_x / 10000
    checkp_x = x_val[b] + orthv_x
    checkp_y = y_val[b] + orthv_y
    # Vektor Punkt von Gerade zu Punkt
    c1_x = x_val[b + 2] - x_val[b]
    c1_y = y_val[b + 2] - y_val[b]
    normal_distxy_part = abs(c1_x * orthv_x + c1_y * orthv_y)
    normal_distxy = (normal_distxy_part / math.sqrt((orthv_x ** 2 + orthv_y ** 2)))
    c2_x = x_val[b + 2] - checkp_x
    c2_y = y_val[b + 2] - checkp_y
    normal_distxy2_part = abs(c2_x * orthv_x + c2_y * orthv_y)
    normal_distxy2_checkp = (normal_distxy2_part / math.sqrt((orthv_x ** 2 + orthv_y ** 2)))

    if round(normal_distxy, 8) < round(normal_distxy2_checkp, 8):
        orientation_xy.append("CCW")
    else:
        orientation_xy.append("CW")

    print("B is", b, "phi is", round(phi_xy, 5), "Orientation is", orientation_xy[b], "Bending Angle is", xy_degree[b])
    b += 1




orientation_xz = []
xz_phi = []
xz_degree = []
c = 0

#### XZ Angle and orientation #############
while c + 2 < len(x_val):
    # feed length for cos check!
    # spitze minus fuß!
    x1_x = (x_val[c + 1]) - (x_val[c])
    x1_z = (z_val[c + 1]) - (z_val[c])
    x2_x = (x_val[c + 1]) - (x_val[c + 2])
    x2_z = (z_val[c + 1]) - (z_val[c + 2])
    phi_rad_xz = math.acos(
        ((x1_x * x2_x + x1_z * x2_z) / (math.sqrt(x1_x ** 2 + x1_z ** 2) * math.sqrt(x2_x ** 2 + x2_z ** 2))))
    phi_xz = phi_rad_xz * 180 / math.pi
    bend_ang_xz = 180 - phi_xz
    bend_ang_rad_xz = bend_ang_xz * math.pi / 180
    if bend_ang_xz < round(180, 8):
        xz_degree.append(bend_ang_xz)
    else:
        xz_degree.append(0)
    xz_phi.append(
        phi_xz)  #########CHANGE BETA TO BEND ANG ! ! ! ! !#####################################################
    orthv2_x = x1_z * (-1) / 10000
    orthv_z = x1_x / 10000
    checkp_x = x_val[c] + orthv2_x
    checkp_z = z_val[c] + orthv_z
    # Vektor Punkt von Gerade zu Punkt
    c1_x = x_val[c + 2] - x_val[c]
    c1_z = z_val[c + 2] - z_val[c]
    normal_distxz_part = abs(c1_x * orthv2_x + c1_z * orthv_z)
    normal_distxz = (normal_distxz_part / math.sqrt((orthv2_x ** 2 + orthv_z ** 2)))
    c2_x = x_val[c + 2] - checkp_x
    c2_z = z_val[c + 2] - checkp_z
    normal_distxz2_part = abs(c2_x * orthv2_x + c2_z * orthv_z)
    normal_distxz2_checkp = (normal_distxz2_part / math.sqrt((orthv2_x ** 2 + orthv_z ** 2)))

    if round(normal_distxz, 8) < round(normal_distxz2_checkp, 8):
            orientation_xz.append("CCW")
    else:
            orientation_xz.append("CW")

    print("C is", c, "phi is", round(phi_xz, 5), "Orientation is", orientation_xz[c], "Bending Angle is", xz_degree[c])


    c += 1


#   XY Bending Motor
DIR_xy = 20   # Direction GPIO Pin
STEP_xy = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR_xy = 200   # Steps per Revolution (360/1.8)

# # GPIO.setmode(GPIO.BCM)
# GPIO.setup(DIR_xy, GPIO.OUT)
# GPIO.setup(STEP_xy, GPIO.OUT)
# GPIO.output(DIR_xy, CW)
#
# MODE_xy = (14, 15, 18)
# Gpio.setup(MODE_xy, GPIO.OUT)
# RESOLUTION = {'Full': (0, 0, 0),
#               'Half': (1, 0, 0),
#               '1/4': (0, 1, 0),
#               '1/8': (1, 1, 0),
#               '1/16': (0, 0, 1),
#               '1/32': (1, 0, 1)}
# GPIO.output(MODE_xy, RESOLUTION['1/32'])



#   XZ Bending Motor
DIR_xz = 20   # Direction GPIO Pin
STEP_xz = 21  # Step GPIO Pin

SPR_xz = 200   # Steps per Revolution (360/1.8)

# # GPIO.setmode(GPIO.BCM)
# GPIO.setup(DIR_xz, GPIO.OUT)
# GPIO.setup(STEP_xz, GPIO.OUT)
# GPIO.output(DIR_xz, CW)
#
# MODE_xz = (14, 15, 18)
# Gpio.setup(MODE_xz, GPIO.OUT)
# RESOLUTION = {'Full': (0, 0, 0),
#               'Half': (1, 0, 0),
#               '1/4': (0, 1, 0),
#               '1/8': (1, 1, 0),
#               '1/16': (0, 0, 1),
#               '1/32': (1, 0, 1)}
# GPIO.output(MODE_xz, RESOLUTION['1/32'])


d = 0
while d < len(feed_length):
    #  append feed_length and steps


    if orientation_xz[d] == "CW":
            step_count_xz = int(float(xz_degree[d])*(1 / 0.01125))  #  Bei 1:20 und 1/8 microstepping!
    else:
            step_count_xz = int(float(xz_degree[d])*(1 / 0.01125)*-1)

    delayfor05RPSxz = 2 / (SPR_xz * 8)
    print("xz Steps", [d], step_count_xz)
        # for x in range(step_count_xz):
        #     GPIO.output(STEP_xz, GPIO.HIGH)
        #     sleep(delayfor2RPS)
        #     GPIO.output(STEP_xz, GPIO.LOW)
        #     sleep(delay)

    sleep(0.5)




    if orientation_xy[d] == "CW":
        step_count_xy = int(float(xy_degree[d])*(1/0.03214))    #  Bei 1:1,75!
    else:
        step_count_xy = int(float(xy_degree[d])*(1/0.03214))*-1

    delayfor05RPSxy = 2 / (SPR_xy * 32)     # 0,00015625*2
    print("xy steps", [d], step_count_xy)
    # for x in range(step_count_xy):
    #     GPIO.output(STEP_xy, GPIO.HIGH)
    #     sleep(delayfor05RPSxy)
    #     GPIO.output(STEP_xy, GPIO.LOW)
    #     sleep(delayfor05RPSxy)

    sleep(.5)
    d += 1

    # GPIO.output(DIR_xy, CCW)



#GPIO.cleanup()