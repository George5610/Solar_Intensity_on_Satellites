from vpython import *
from math import pi

#
# VARAIBLES
#
G = 6.67e-11 # gravitatinal constant (m^3 kg^-1 s^-2)
RS = 696.35e6 # radius of the sun (m)
MS = 1.989e30 # mass of the sun (kg)
HR = 3.95e26 # heat radiation from the sun "https://physics.stackexchange.com/questions/57392/calculating-the-amount-of-heat-energy-radiated-by-sun"
AF = 0.30 # absorbsion factor of polished aluminium
Tsat = 288 # temperiture of the sat (K)
TSun = 5778 # temp of the sun (K)
sigma = 5.670374419e-8 # Stefan–Boltzmann constant
ER = 1.50e11 # radius of earths orbit (m)
A = 1 # area of the sat
SHC = 900 # specific heat capacity of aluminium

#
#FUNCTIONS
#
scene = canvas(title='Solar Thermal Radiation Model  ', x=0, y=0, width=1500, height=400)
#cf = 1 # initial code freq
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
scene.caption = "\nChange Time Step: \n\n"

def setspeed(s):
    wt.text = '{:1.2f}'.format(s.value)

sl = slider(min=1, max=10000, value=1, length=400, bind=setspeed, right=15)

wt = wtext(text='{:1.2f}'.format(sl.value))

scene.append_to_caption(' Time Step \n')

#Code frequency
scene.append_to_caption("\nChange Code Frequency \n\n")

def setfreq(f):
    cft.text = '{:1.2f}'.format(f.value)

cf = slider(min=1, max=500000, value=1, length=400, bind=setfreq, right=15)

cft = wtext(text='{:1.2f}'.format(cf.value))

scene.append_to_caption(' Frequency (Hz) \n')

#
#CREATING OBJECTS
#
Sun = sphere(pos = vector(0,0,0), radius = RS, texture = "https://i.imgur.com/XdRTvzj.jpeg")
Sun.m = MS
Sun.p = Sun.m * vector(0,0,0)

sat = box(pos = vector(ER,0,0), radius = 0.05 * RS, make_trail=True)
sat.m = 100 # mass of the satellite (kg)
sat.p = sat.m * vector(0,20000,0) # inital satellite vector

#
#GRAPHS
#
t = 0 # set initial time
counter = 0
g1 = graph(scroll=True, width=1500, height=400, fast=False, xmin=0, xmax=100000, title="Intensity of Solar Radiation for distance", xtitle="Distance (km)", ytitle="Intensity (W/m^2)")
g2 = graph(scroll=True, width=1500, height=400, fast=False, xmin=0, xmax=1e100, title="Intensity of Solar Radiation over time", xtitle="Time (s)", ytitle="Intensity (W/m^2)")
g3 = graph(scroll=True, width=1500, height=400, fast=False, xmin=0, xmax=1e100, title="Temp of Sat", xtitle="Time (s)", ytitle="Temp (K)")

g1 = gcurve(graph=g1, color=color.green)
g2 = gcurve(graph=g2, color=color.red)
g3 = gcurve(graph=g3, color=color.blue)

#
#LOOP AND CALCULATIONS
#
while True: # set true for infinte or set to a max time
    rate(cf.value) # max frequency of the while loop (Hz)
    if running:
        #sat position calculations
        dt = sl.value # time step
        r = sat.pos - Sun.pos # distance from the sun
        magR = mag(r)
        F = -G * Sun.m * sat.m * norm(r) / magR**2 # force the satellite experiences due to gravity
        sat.p = sat.p + F * dt # calculates new vector based on new time and force
        sat.pos = sat.pos + sat.p * dt / sat.m

        #timers
        counter += 1
        t = t + dt

        #distance and intensity calcuations
        magRkm = magR / 1000
        Intensity = HR / ((4*pi) * magR**2) # wattage per meter squared at the sats distance from the sun

        # thermal calculations
        PowerIn = Intensity * AF * A
        PowerOut = sigma * AF * A * Tsat**4 # energy emitted
        PowerNet = PowerIn - PowerOut
        Tsat = PowerNet / (sat.m * SHC) + Tsat

        if not counter % 100: # plot sampling rate
            #plots
            g1.plot(magRkm, Intensity)
            g2.plot(t, Intensity)
            g3.plot(t, Tsat)
            print(Tsat)
            print(Intensity, " Watts/m^2 at a distance of ", magRkm, " km")
