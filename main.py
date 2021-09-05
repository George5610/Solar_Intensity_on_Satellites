from vpython import *
import math

#
# VARAIBLES
#
G = 6.67e-11 # gravitatinal constant (m^3 kg^-1 s^-2)
RS = 696.35e6 # radius of the sun (m)
MS = 1.989e30 # mass of the sun (kg)
HR = 3.95e26 # heat radiation from the sun "https://physics.stackexchange.com/questions/57392/calculating-the-amount-of-heat-energy-radiated-by-sun"
AF = 0.70 # albedo of polished aluminium
Tsat = 288 # temperiture of the sat (K)
TSun = 5778 # temp of the sun (K)
sigma = 5.670374419e-8 # Stefan–Boltzmann constant
ER = 1.50e11 # radius of earths orbit (m)

#
#FUNCTIONS
#
scene = canvas(title='Solar Thermal Radiation Model  ', x=0, y=0, width=1500, height=800)
running = True
def Run(b):
    global running, remember_dt, dt
    running = not running
    if running:
        b.text = "Pause"
        dt = remember_dt
    else:
        b.text = "Run"
        remember_dt = dt
        dt = 0
    return

button(text="Pause", pos=scene.title_anchor, bind=Run)

#CAMERA BUTTON
def cam(b):
    global running
    running = not running
    if running:
        b.text = "Sat"
        scene.camera.follow(Sun) # lock the camera to the sat
    else:
        b.text = "Sun"
        scene.camera.follow(sat) # lock the camera to the sat
    return

button(text="Sat", pos=scene.title_anchor, bind=cam)

#ANIMATION SPEED
scene.caption = "Vary the rotation speed: \n\n"

def setspeed(s):
    wt.text = '{:1.2f}'.format(s.value)

sl = slider(min=1, max=10000, value=5000, length=220, bind=setspeed, right=15)

wt = wtext(text='{:1.2f}'.format(sl.value))

scene.append_to_caption(' Time Step \n')


#
#CREATING OBJECTS
#
Sun = sphere(pos = vector(0,0,0), radius = RS, texture = "https://i.imgur.com/XdRTvzj.jpeg")
Sun.m = MS
Sun.p = Sun.m * vector(0,0,0)

sat = box(pos = vector(ER,0,0), radius = 0.05 * RS, make_trail=True)
sat.m = 100 # mass of the satellite (kg)
sat.p = sat.m * vector(0,20000,5000) # inital satellite vector

#
#LOOP AND CALCULATIONS
#
t = 0 # set initial time

while True: # set true for infinte or set to a max time
    rate(400) # max frequency of the while loop (Hz)
    if running:
        #sat position calculations
        dt = sl.value # time step
        r = sat.pos - Sun.pos # distance from the sun
        F = -G * Sun.m * sat.m * norm(r) / mag(r)**2 # force the satellite experiences due to gravity
        sat.p = sat.p + F * dt # calculates new vector based on new time and force
        sat.pos = sat.pos + sat.p * dt / sat.m

        #distance and intensity calcuations
        magR = mag(r)
        magRkm = magR / 1000
        Intensity = HR / ((4*math.pi) * magR**2) # wattage per meter squared at the sats distance from the sun
        print(Intensity, " Watts/m^2 at a distance of ", magRkm, " km")
        scene.append_to_caption('\n',Intensity, " Watts/m^2")
        t = t + dt
