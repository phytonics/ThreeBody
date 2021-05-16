# A Simulation of the Three Body System
# Adapted from 'GravitySim' by Matt Sprengel

from tkinter import *
import math
import time

def globalReset():  # utility function used by both speedTest() and 'reset' button
    global r1, v1, a1, r2, v2, a2, r3, v3, a3, m1, m2, m3, size1, size2, size3

    r1, v1, a1 = [1400, 300], [-u/2, (u/2) * math.sqrt(3)], [0, 0]
    r2, v2, a2 = [1300, 300 - 100 * math.sqrt(3)], [u, 0], [0, 0]
    r3, v3, a3 = [1200, 300], [-u/2, -(u/2) * math.sqrt(3)], [0, 0]

    size1, size2, size3 = 7.5 * m1 ** (1.0 / 3.0), 7.5 * m2 ** (1.0 / 3.0), 7.5 * m3 ** (1.0 / 3.0)
    canvas.delete("uno", "dos", "tres")  # deleting velocity indicator lines
    car()


def setMass1():  # gets the value inside entry box, sets mass to that value
    global m1, size1
    m1 = float(mass1.get())
    size1 = 7.5 * m1 ** (1.0 / 3.0)
    mass1.delete(0, 'end')


def setMass2():
    global m2, size2
    m2 = float(mass2.get())
    size2 = 7.5 * m2 ** (1.0 / 3.0)
    mass2.delete(0, 'end')


def setMass3():
    global m3, size3
    m3 = float(mass3.get())
    size3 = 7.5 * m3 ** (1.0 / 3.0)
    mass3.delete(0, 'end')


def speedUp():  # bound to speed up button
    global dt
    dt *= 2


def slowDown():
    global dt
    dt /= 2


def drag(event):  # changes the location of the body to current mouse coordinates
    xm, ym = event.x, event.y

    rm1 = math.sqrt(((xm - r1[0]) ** 2) + ((ym - r1[1]) ** 2))
    rm2 = math.sqrt(((xm - r2[0]) ** 2) + ((ym - r2[1]) ** 2))
    rm3 = math.sqrt(((xm - r3[0]) ** 2) + ((ym - r3[1]) ** 2))

    clickableRadius1, clickableRadius2, clickableRadius3 = 2 * size1, 2 * size2, 2 * size3

    if rm1 < clickableRadius1:
        a1[0], a1[1] = 0, 0
        v1[0], v1[1] = 0, 0
        r1[0], r1[1] = xm, ym
        canvas.delete("uno")

    if rm2 < clickableRadius2:
        a2[0], a2[1] = 0, 0
        v2[0], v2[1] = 0, 0
        r2[0], r2[1] = xm, ym
        canvas.delete("dos")

    if rm3 < clickableRadius3:
        a3[0], a3[1] = 0, 0
        v3[0], v3[1] = 0, 0
        r3[0], r3[1] = xm, ym
        canvas.delete("tres")


def wasRightClicked(event):  # checks to see if ball was right-clicked
    global pressed1, pressed2, pressed3
    xm, ym = event.x, event.y

    rm1 = math.sqrt(((xm - r1[0]) ** 2) + ((ym - r1[1]) ** 2))
    clickableRadius1 = size1 / 2
    if rm1 < clickableRadius1:
        pressed1 = 1  # toggles "pressed" to on, allowing for velSet function

    rm2 = math.sqrt(((xm - r2[0]) ** 2) + ((ym - r2[1]) ** 2))
    clickableRadius2 = size2 / 2
    if rm2 < clickableRadius2:
        pressed2 = 1

    rm3 = math.sqrt(((xm - r3[0]) ** 2) + ((ym - r3[1]) ** 2))
    clickableRadius3 = size3 / 2
    if rm3 < clickableRadius3:
        pressed3 = 1


def makeVelLine(event):  # this func is called upon right-click-motion. Draws.
    global pressed1, newVel1, pressed2, newVel2, pressed3, newVel3
    vxm, vym = event.x, event.y
    velScale = 10  # bigger velScale ---> less velocity in relation to how far user dragged mouse away from body
    if pressed1 == 1:
        canvas.delete("uno")
        canvas.create_line(r1[0], r1[1], vxm, vym, fill="green", width=1,
                           tags="uno")
        newVel1[0], newVel1[1] = (vxm - r1[0]) / velScale, (vym - r1[1]) / velScale
    if pressed2 == 1:
        canvas.delete("dos")
        canvas.create_line(r2[0], r2[1], vxm, vym, fill="green", width=1,
                           tags="dos")
        newVel2[0], newVel2[1] = (vxm - r2[0]) / velScale, (vym - r2[1]) / velScale
    if pressed3 == 1:
        canvas.delete("tres")
        canvas.create_line(r3[0], r3[1], vxm, vym, fill="green", width=1,
                           tags="tres")
        newVel3[0], newVel3[1] = (vxm - r3[0]) / velScale, (vym - r3[1]) / velScale


def velLineSet(_):  # this function is called upon mouse release. Sets vel.
    global newVel1, newVel2, newVel3, pressed1, pressed2, pressed3
    if pressed1 == 1:
        v1[0], v1[1] = newVel1[0], newVel1[1]
        newVel1[0], newVel1[1] = 0, 0
        if gameState == 1:
            canvas.delete("uno")
        pressed1 = 0
    if pressed2 == 1:
        v2[0], v2[1] = newVel2[0], newVel2[1]
        newVel2[0], newVel2[1] = 0, 0
        if gameState == 1:
            canvas.delete("dos")
        pressed2 = 0
    if pressed3 == 1:
        v3[0], v3[1] = newVel3[0], newVel3[1]
        newVel3[0], newVel3[1] = 0, 0
        if gameState == 1:
            canvas.delete("tres")
        pressed3 = 0


def showInfo():
    # This function runs once every time step. Shows vel, position.
    # The below conditionals allow for the velocity info to be updated on the screen WHILE drawing velset line
    # and not just after vel line is released
    if pressed2 == 1:
        str1 = "Yellow:   v = [%.3f, %.3f]\nRed:        v = [%.3f, %.3f]\nB" \
               "lue:       v = [%.3f, %.3f]" % (newVel2[0], newVel2[1], v3[0],
                                                v3[1], v1[0], v1[1])
        canvas.delete("velinfo")
        canvas.create_text(10, 30, text=str1, fill="green", anchor=W, justify=LEFT,
                           tags="velinfo")
    if pressed1 == 1:
        str1 = "Yellow:   v = [%.3f, %.3f]\nRed:        v = [%.3f, %.3f]\nB" \
               "lue:       v = [%.3f, %.3f]" % (v2[0], v2[1], v3[0], v3[1],
                                                newVel1[0], newVel1[1])
        canvas.delete("velinfo")
        canvas.create_text(10, 30, text=str1, fill="green", anchor=W, justify=LEFT,
                           tags="velinfo")
    if pressed3 == 1:
        str1 = "Yellow:   v = [%.3f, %.3f]\nRed:        v = [%.3f, %.3f]\nB" \
               "lue:       v = [%.3f, %.3f]" % (v2[0], v2[1], newVel3[0],
                                                newVel3[1], v1[0], v1[1])
        canvas.delete("velinfo")
        canvas.create_text(10, 30, text=str1, fill="green", anchor=W, justify=LEFT,
                           tags="velinfo")
    if pressed2 == 0 and pressed1 == 0 and pressed3 == 0:
        str2 = "Yellow:   v = [%.3f, %.3f]\nRed:        v = [%.3f, %.3f]\nB" \
               "lue:       v = [%.3f, %.3f]" % (v2[0], v2[1], v3[0], v3[1], v1[0],
                                                v1[1])
        canvas.delete("velinfo")
        canvas.create_text(10, 30, text=str2, fill="green", anchor=W, justify=LEFT,
                           tags="velinfo")
    str3 = "Yellow:   r = [%d, %d]\nRed:        r = [%d, %d]\nB" \
           "lue:       r = [%d, %d]" % (r2[0], r2[1], r3[0], r3[1], r1[0], r1[1])
    canvas.delete("posinfo")
    canvas.create_text(10, 570, text=str3, fill="green", anchor=W, justify=LEFT,
                       tags="posinfo")
    str4 = "Yellow:   Mass = %.3f\nRed:        Mass = %.3f\nB" \
           "lue:       Mass = %.3f" % (m2, m3, m1)
    canvas.delete("massinfo")
    canvas.create_text(990, 30, text=str4, fill="green", anchor=E, justify=RIGHT,
                       tags="massinfo")
    str5 = "Euler-Cromer Method"
    canvas.delete("RAWR")
    canvas.create_text(990, 590, text=str5, fill="green", anchor=E, justify=RIGHT, tags="RAWR")


def updateScreen():  # deletes old, draws new circles at current position
    canvas.delete("blue", "yellow", "red", "cm")
    canvas.create_oval(r1[0] % 2000 - (size1 / 2), r1[1] - (size1 / 2), r1[0] % 2000 + (size1 / 2), r1[1] +
                       (size1 / 2), outline="blue", fill="blue", tags="blue")
    canvas.create_oval(r2[0] % 2000 - (size2 / 2), r2[1] - (size2 / 2), r2[0] % 2000 + (size2 / 2), r2[1] +
                       (size2 / 2), outline="yellow", fill="yellow",
                       tags="yellow")
    canvas.create_oval(r3[0] % 2000 - (size3 / 2), r3[1] - (size3 / 2), r3[0] % 2000 + (size3 / 2), r3[1] +
                       (size3 / 2), outline="red", fill="red", tags="red")
    canvas.create_oval(rcm[0] % 2000 - 1, rcm[1] - 1, rcm[0] % 2000 + 1, rcm[1] + 1,
                       outline="white", fill="white", tags="cm")
    showInfo()
    root.update()


def calculate(x, x_dot):
    global dt
    x1, x2, x3 = x
    x_dot1, x_dot2, x_dot3 = x_dot
    x2 = [x2[0] + x_dot2[0] * dt, x2[1] + x_dot2[1] * dt]
    x1 = [x1[0] + x_dot1[0] * dt, x1[1] + x_dot1[1] * dt]
    x3 = [x3[0] + x_dot3[0] * dt, x3[1] + x_dot3[1] * dt]
    return x1, x2, x3


def calculate_trajectories():  # Euler-Cromer Method
    global G, m1, r1, v1, a1, m2, r2, v2, a2, m3, r3, v3, a3, rcm
    rMag_12 = math.sqrt((r1[0] - r2[0]) ** 2 + (r1[1] - r2[1]) ** 2)
    rMag_13 = math.sqrt((r1[0] - r3[0]) ** 2 + (r1[1] - r3[1]) ** 2)
    rMag_23 = math.sqrt((r2[0] - r3[0]) ** 2 + (r2[1] - r3[1]) ** 2)
    rHat_21 = [(r2[0] - r1[0]) / rMag_12, (r2[1] - r1[1]) / rMag_12]
    rHat_12 = [-rHat_21[0], -rHat_21[1]]
    rHat_23 = [(r2[0] - r3[0]) / rMag_23, (r2[1] - r3[1]) / rMag_23]
    rHat_32 = [-rHat_23[0], -rHat_23[1]]
    rHat_13 = [(r1[0] - r3[0]) / rMag_13, (r1[1] - r3[1]) / rMag_13]
    rHat_31 = [-rHat_13[0], -rHat_13[1]]
    a21Mag = -m1 * G / (rMag_12 ** 2)
    a12Mag = a21Mag * (m2 / m1)
    a23Mag = -m3 * G / (rMag_23 ** 2)
    a32Mag = a23Mag * (m2 / m3)
    a13Mag = -m3 * G / (rMag_13 ** 2)
    a31Mag = a13Mag * (m1 / m3)
    a2 = [(rHat_21[0] * a21Mag) + (rHat_23[0] * a23Mag),
          (rHat_21[1] * a21Mag) + (rHat_23[1] * a23Mag)]
    a1 = [(rHat_12[0] * a12Mag) + (rHat_13[0] * a13Mag),
          (rHat_12[1] * a12Mag) + (rHat_13[1] * a13Mag)]
    a3 = [(rHat_31[0] * a31Mag) + (rHat_32[0] * a32Mag),
          (rHat_31[1] * a31Mag) + (rHat_32[1] * a32Mag)]

    v1, v2, v3 = calculate(
        (v1, v2, v3),
        (a1, a2, a3)
    )
    r1, r2, r3 = calculate(
        (r1, r2, r3),
        (v1, v2, v3)
    )

    rcm = [
        (m1 * r1[0] + m2 * r2[0] + m3 * r3[0]) / (m1 + m2 + m3),
        (m1 * r1[1] + m2 * r2[1] + m3 * r3[1]) / (m1 + m2 + m3)
    ]


def car():  # draws scene whenever the calculations aren't running
    global gameState, rcm
    root.title(title)
    gameState = 0
    j = 0
    while gameState == 0:
        j += 1
        rcm = [(m1 * r1[0] + m2 * r2[0] + m3 * r3[0]) / (m1 + m2 + m3),
               ((m1 * r1[1] + m2 * r2[1] + m3 * r3[1]) / (m1 + m2 + m3))]
        if j % refreshScale == 0:
            updateScreen()
            j = 0


def gameOn():  # runs the physics in a loop until told to stop
    global gameState
    root.title("Calculating...")
    canvas.delete("uno", "dos", "tres")  # deleting velocity indicator lines
    i = 0
    gameState = 1
    while gameState == 1:
        i += 1
        calculate_trajectories()
        if i % refreshScale == 0:  # only updates screen here
            i = 0
            updateScreen()


title = "A Simulation of a Three-Body Systems"

pressed1 = 0  # toggles for wasRightClicked handler
pressed2 = 0
pressed3 = 0

newVel1 = [0, 0]  # toggles for drag set velocity handler
newVel2 = [0, 0]  # newVel interim global allows the actual velocity to not instantly
newVel3 = [0, 0]  # and continuously change during the right-click+drag


# GLOBAL PHYSICS VARIABLES
# r = position, v = velocity, a = acceleration, m = mass
G = 1000

s = 200
u = math.sqrt(5)

m1 = 1.0
r1, v1, a1 = [1400, 300], [-u / 2, (u / 2) * math.sqrt(3)], [0, 0]
size1 = 7.5 * m1 ** (1.0 / 3.0)

m2 = 0.5
r2, v2, a2 = [1300, 300 - 100 * math.sqrt(3)], [u, 0], [0, 0]
size2 = 7.5 * m2 ** (1.0 / 3.0)

m3 = 1.0
r3, v3, a3 = [1200, 300], [-u / 2, -(u / 2) * math.sqrt(3)], [0, 0]
size3 = 7.5 * m3 ** (1.0 / 3.0)

# center of mass of the system
rcm = [
    (m1 * r1[0] + m2 * r2[0] + m3 * r3[0]) / (m1 + m2 + m3),
    (m1 * r1[1] + m2 * r2[1] + m3 * r3[1]) / (m1 + m2 + m3)
]


# GUI Screen, widgets, buttons, bindings
root = Tk()
root.state('zoomed')
root.title(title)
frame = Frame(width=1000, height=50, bg="black")
frame.pack(fill=BOTH)


# Creating start, stop, reset buttons. Binding them to relevent functions.
start = Button(frame, text="Start", command=gameOn, bg="green")
start.pack(side=LEFT, padx=5)
stop = Button(frame, text="Stop", command=car, bg="green")
stop.pack(side=LEFT, padx=5)
reset = Button(frame, text="Reset", command=globalReset, bg="green")
reset.pack(side=LEFT, padx=5)


# Creating mass editing entry box and buttons
mb1 = Button(frame, text="Set Mass", command=setMass1, bg="Blue", fg="white")
mb1.pack(side=RIGHT, padx=10, pady=3)
mass1 = Entry(frame, width=5, bg="black", fg="white", insertbackground="white", insertwidth=1)
mass1.pack(side=RIGHT, padx=5)
mb2 = Button(frame, text="Set Mass", command=setMass2, bg="Yellow")
mb2.pack(side=RIGHT, padx=10)
mass2 = Entry(frame, width=5, bg="black", fg="white", insertbackground="white", insertwidth=1)
mass2.pack(side=RIGHT, padx=5)
mb3 = Button(frame, text="Set Mass", command=setMass3, bg="Red", fg="white")
mb3.pack(side=RIGHT, padx=10)
mass3 = Entry(frame, width=5, bg="black", fg="white", insertbackground="white", insertwidth=1)
mass3.pack(side=RIGHT, padx=5)


# Creating speed up and slow down buttons
speedup = Button(frame, text="Speed Up", command=speedUp, bg="Black", fg="White")
speedup.pack(side=LEFT, padx=20)
slowdown = Button(frame, text="Slow Down", command=slowDown, bg="Black", fg="White")
slowdown.pack(side=LEFT, padx=5)


# Creating main black canvas under all of the buttons we just made
canvas = Canvas(root, width=1000, height=600, bg="black")
canvas.pack(fill=BOTH, expand=1)
# Binding mouse movements and events to their corresponding functions
canvas.bind('<B1-Motion>', drag)
canvas.bind('<Button-3>', wasRightClicked)
canvas.bind('<B3-Motion>', makeVelLine)
canvas.bind('<ButtonRelease-3>', velLineSet)


# Timing the user's CPU on a dummy run through of the calculations
def speedTest():
    global refreshScale, dt
    t1 = time.time()
    i = 0
    while gameState == 2:
        i += 1
        calculate_trajectories()
        if i % 20000 == 0:
            t2 = time.time()
            iters_per_second = 20000.0 / (t2 - t1)
            print("Euler-Cromer iterations per second: %d" % int(iters_per_second))
            refreshScale = int(iters_per_second / 120.0)  # 120 Hz desired
            dt = 1 / (refreshScale * 4.3859)  # 4.3859 works well.. experimentally
            globalReset()
            break


updateScreen()
refreshScale, dt = 0, 0.0  # initializing refreshScale and time-step
gameState = 2
speedTest()  # computes dt and refresh scale ---> also starts main loop
