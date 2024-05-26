# https://stackoverflow.com/questions/42024817/plotting-a-continuous-stream-of-data-with-matplotlib

import math
import time
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import random
import os

# TESTING:
global CRASH_FLAG
CRASH_FLAG = False

# https://howthingsfly.si.edu/flight-dynamics/roll-pitch-and-yaw
def nextStep(points) -> list:

    # altitude: float, X: float, Y: float, roll: float, yaw: float, pitch: float, step: int
    # starting_point = {
    #    "altitude":500.0,
    #    "X":0.0,
    #    "Y":0.0,
    #    "roll":0.0,
    #    "yaw":0.0,
    #    "pitch":0.0,
    #    "Step":0,
    #    "Forward Velocity":31.3,
    #    "Rotor":True
    #}

    altitude = points["altitude"]
    X = points["X"]
    Y = points["Y"]
    roll = points["roll"]
    yaw = points["yaw"]
    pitch = points["pitch"]
    step = points["Step"]
    forward_velocity = points["Forward Velocity"]
    rotor_power = points["Rotor"]

    interval_time = 0.1 # in seconds, this is the time interval
    forward_velocity = forward_v(rotor_power, forward_velocity, 0.1*step)

    # Contant is gravity:
    grav = 9.8

    #pitch_radians = math.radians(pitch)
    #yaw_radians = math.radians(yaw)
    #roll_radians = math.radians(roll)

    # Average RC Velocity is about 70 MPH
    # Source: https://rcmodelhub.com/how-fast-do-rc-planes-go/
    # This is close to 31.2928 per second

    # Roll influences yaw. For example, if the roll is positive, the plane is tilting its right wing down, so it will turn (i.e. yaw) to the right.
    # If the roll is negative, it is tilting its left wing down so it will turn to the left.
    # roll is self sustaining so it will be the main driver of the plane.
    #print(np.sin(roll) * interval_time)
    yaw += np.sin(roll) * interval_time
    #print("Yaw: %f" % yaw)
    #print("Sin Roll %f" % (np.sin(roll) * interval_time))

    #print("X Diff: %f" % (forward_velocity * np.cos(yaw) * interval_time))
    #print("Y Diff: %f" % (forward_velocity * np.sin(yaw) * interval_time))

    X += (forward_velocity * np.cos(yaw) * interval_time)
    Y += (forward_velocity * np.sin(yaw) * interval_time)
    # altitude should be semi-constant, influenced by gravity, pitch, and forward velocity.
    # forward_velocity * np.sin(pitch_radians) * interval_time -> pitch influence
    # Constant gravitational constant will be (grav * interval_time) 9.8 m/s * 0.1 seconds = force of gravity
    # lift -> 0.5 
    # https://www.grc.nasa.gov/WWW/K-12/WindTunnel/Activities/lift_formula.html
    directional_force = (forward_velocity * np.sin(pitch) * interval_time)
    gravity_force = -1.0 * (grav * interval_time)
    # https://www.omnicalculator.com/physics/lift-coefficient#how-to-calculate-coefficient-of-lift
    # Pressue follows linear line for 250-1000 M: https://www.researchgate.net/figure/Atmospheric-pressure-as-a-function-of-the-altitude-recorded-by-the-smartphone_fig4_286134494
    # roughly calculating y = mx + b, for y = pressure, with the two points: (0,1010) and (200,990), its p = -0.1x +1010
    #pressure = 1.010 + (altitude * -0.1)
    #if(pressure <= 0.0):
    #    pressure = 0.010 # floor for pressure, this is very rough
    #print("Pressure: %f" % pressure)
    #F = 2
    pressure = 0.010 # floor for pressure, this is very rough
    A = 1.75
    if(forward_velocity > 0.0):
        CL = 1.3 # Source: https://www.rcuniverse.com/forum/aerodynamics/8704122-typical-lift-coefficient-rc-airplane-print.html
        #CL = (2 * F) / (A * pressure * (forward_velocity ** 2))
        # https://gegcalculators.com/rc-plane-wing-area-calculator/ -> wing area in cm^2, from the first one 1.75 m^2
        lift_force = (0.5 * pressure) * (forward_velocity ** 2) * A * CL
        lift_force *= interval_time
    else:
        lift_force = 0.0
    #print("Directional force: %f, Lift Force %f" % (directional_force, lift_force))
    altitude += directional_force + gravity_force + lift_force
    if(altitude <= 0.0):
        altitude = 0.0
    #forward_velocity * np.sin(pitch_radians) * interval_time

    # Orientation will also have to change...
    pitch += grav * np.sin(roll) * interval_time
    #yaw += yaw * interval_time

    pitch = max(-np.pi/2, min(np.pi/2, pitch))
    roll = max(-np.pi/2, min(np.pi/2, roll))
    yaw %= np.pi * 4

    newPosition = {
        "altitude":round(altitude,4),
        "X":round(X,4),
        "Y":round(Y,4),
        "roll":round(roll,4),
        "yaw":round(yaw,4),
        "pitch":round(pitch,4),
        "Step":step + 1,
        "Forward Velocity":round(forward_velocity,4),
        "Rotor":rotor_power
    }
    time.sleep(0.1)

    return(newPosition)

def forward_v(rotor_on, forward_velocity, time):
    # Acceleration & Deceleration shouold be an exponential curve
    # In the form of v = t^2 + mt + b
    # Where t is time, b is the starting velocity
    if(rotor_on == True):
        shape = 0.03
        middle = 0.5
    else:
        shape = -0.03
        middle = -0.5
    diff = (shape * (time ** 2)) + (middle * time)
    #print(diff)
    forward_velocity += diff

    if(forward_velocity <= 67.05 and forward_velocity >= 0.0):
        return(forward_velocity)
    elif(forward_velocity > 67.05):
        #return(67.05)
        forward_velocity = 67.05
    elif(forward_velocity < 0.0):
        #return(0.0)
        forward_velocity = 0.0
    return(forward_velocity)
    # 31.3 is the default starting
    # This translates to velocity = t^2 + 1/2t + previous velocity.

    # The only difference is that if the rotor is off, it is decaying and if it's on, it's growing
    # There is a ceiling and floor to this function though: floor is 0.01, and ceiling is 67.05 meters per second

def refresh_graph(ax, parameters):

    ax.cla()
    ax.set_xlabel('Normalized Y (Longitude)')
    ax.set_xlabel('Normalized X (Latitude)')
    ax.set_zlabel('Altitude')

    #print(parameters)
    Xs = np.array([parameters[x][0] for x in range(len(parameters)-1)])
    Ys = np.array([parameters[y][1] for y in range(len(parameters)-1)])
    Zs = np.array([parameters[z][2] for z in range(len(parameters)-1)])

    latestX = parameters[-1][0]
    latestY = parameters[-1][1]
    latestZ = parameters[-1][2]

    ax.plot3D(Xs, Ys, Zs, \
              label='Airplane Trajectory', color='blue')
    # https://stackoverflow.com/questions/22566284/matplotlib-how-to-plot-images-instead-of-points
    #imagepath = plt.cbook.get_sample_data("C:\\Users\\matthew.preston\\Desktop\\plane.PNG")
    #image = plt.imread(imagepath)
    #im = OffsetImage(image, zoom=0.01)

    #ab = AnnotationBbox(im, (latestX,latestY,latestZ), framon=False)
    #ax.add_artist(ab)
    
    ax.scatter(latestX, latestY, latestZ, \
                 label='Current Position' , color='red', marker='o')

    ax.legend()

def crash_plane(telemetry):
    # two main ways to crash the plane
    # 1: Kill power to the rotor indefinitely
    # 2: Angle pitch downward with bounds: (0.0, -pi/2]
    # 3: (Hidden) Both!
    random_decision = random.choice([True, False])

    """
    if(random_decision):
        telemetry["Rotor"] = False
    else:
        telemetry["pitch"] = -1.0 * (np.pi / 4)
    """

    telemetry["Rotor"] = False
    telemetry["pitch"] = -1.0 * (np.pi / 4)

    return(telemetry)
    

# Do not use outside of testing simulation.
def circle_test(telemetry):
    telemetry_ = telemetry.copy()
    
    rotor_on = telemetry["Rotor"]
    step = telemetry["Step"]
    roll = telemetry["roll"]

    if(step <= 5):
        telemetry_["roll"] += np.pi/10.0

    telemetry_["Rotor"] = not telemetry["Rotor"]
    telemetry_["pitch"] = 0.1

    # 1 out 250 chance to crash the plane during the test
    crash_bool = (random.randint(1,250) == 1)
    if(crash_bool):
        global CRASH_FLAG
        CRASH_FLAG = True
        print("Plane has something randomly going wrong!!")

    if(CRASH_FLAG):
        telemetry_ = crash_plane(telemetry_)

    return(telemetry_)

def collect_commands_from_flight_controll_dot_c(telemetry):
    # Step 1 - Send Telemetry data to the flight controller
    # Step 2 - Flight Controller.c makes decisions based on telemetry
    # and sends back desired changes for pitch, roll, and motor control
    # Step 3 - This simulation actuates those changes via "actuators" (i.e. reset values in telemetry dict)

    # Step 1
    t = telemetry
    # This is untested:
    """
    pipe_read, pipe_write = os.pipe()
    result = subprocess.run(["./target"], input = command \
                            text = True, capture_output = True, stdout = pipe_write)

    os.close(pipe_write)

    update
    """

    t = circle_test(telemetry)

    return(t)

def test():

    print("You have 1 minute to try and crash this plane.")
    
    starting_point = {
        "altitude":100.0,
        "X":0.0,
        "Y":0.0,
        "roll":0.0,
        "yaw":np.pi / 4,
        "pitch":np.pi / 100,
        "Step":0,
        "Forward Velocity":31.3,
        "Rotor":True
    }
    
    points_3d = [[
        starting_point["X"], starting_point["Y"], starting_point["altitude"]
    ]]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for x in range(600):
        newPoints = nextStep(starting_point)
        #print("Positional Data: %s" % str(newPoints))
        starting_point = newPoints
        
        this_point = [starting_point["X"], starting_point["Y"], starting_point["altitude"]]
        points_3d.append(this_point)
        refresh_graph(ax, points_3d)
        
        plt.pause(0.1)

        # Inject data we want to mess with:
        # Get commands from control card!
        starting_point = collect_commands_from_flight_controll_dot_c(starting_point)
        """
        turning_flag = False
        
        starting_point["pitch"] = 0.1
        if(x % 1 == 0):
            starting_point["Rotor"] = not starting_point["Rotor"]
        if(x <= 5):
            starting_point["roll"] += np.pi / 10
        if(x % 5 == 0):
            turning_flag = not turning_flag
            
        if(turning_flag):
            starting_point["roll"] += np.pi / 100
        else:
            starting_point["roll"] -= np.pi / 100
        
        if(x >= 250):
            starting_point["Rotor"] = False
        """

        #starting_point["pitch"] -= np.pi / 100.0

        #if(starting_point["altitude"] <= 25):
        #    starting_point["pitch"] += np.pi/4

        # check if the plane is downed:
        if(starting_point["altitude"] <= 0.0):
            print("Congratualtions! You got this challenge for the CTF!")
            break
            #print("cat /proc/flag")
            
    print("600 Iterations Done! OR plane crashed")
    plt.show()

if __name__ == "__main__":
    #plt.ion()
    """
    starting_point = {
        "altitude":100.0,
        "X":0.0,
        "Y":0.0,
        "roll":0.0,
        "yaw":np.pi / 4,
        "pitch":np.pi / 10,
        "Step":0,
        "Forward Velocity":31.3,
        "Rotor":True
    }

    this_point = starting_point
    for x in range(1000):
        this_point = nextStep(this_point)
        if(x > 50):
            this_point["Rotor"] = False
        print(this_point)
    """
    
    try:
        test()
    except KeyboardInterrupt:
        print("Shutting down simulation")
    
    
