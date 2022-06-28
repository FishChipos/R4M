# NOTES:
# 1 is left and back, 0 is right and front

# Black magic don't touch
pins.set_pull(DigitalPin.P20, PinPullMode.PULL_UP)

# Main logic and callback functions
def main():
    global ir1_read, ir2_read
    global intersectionCount, atIntersection, isMoving, isTurning, isOffCourse
    global active

    if (force_read == 0 and not active):
        active = True

    elif (force_read == 0 and active):
        active = False

    if (not active):
        return

    if (ir1_read == 0 and ir2_read == 0):
        atIntersection = True

    if (not atIntersection):
        isMoving = True

    if (atIntersection and not isTurning):
        
        isTurning = True
        intersectionCount += 1

        atIntersection = False

        if intersectionCount == 1:
            turn_direction = 1
            pass

        elif intersectionCount == 2:
            pass

        elif intersectionCount == 3:
            pass

        elif intersectionCount == 4:
            pass

def move():
    global isMoving, isTurning, direction

    if (not isMoving or isTurning or not active):
        return

    set_gb(direction, speed, 1 - direction, speed)

def turn():
    global isTurning, turn_direction
    global ir1_read, ir2_read 
    global turn_counter1, turn_counter2

    if (not isTurning or not active):
        return

    set_gb(turn_direction, turn_speed, turn_direction, turn_speed)

    if (turn_counter1 + turn_counter2 >= 4):
        isTurning = False
        turn_counter1 = 0
        turn_counter2 = 0
        return

    if (ir1_read == 0 and turn_counter1 == 0):
        turn_counter1 = 1

    elif (ir1_read == 1 and turn_counter1 == 1):
        turn_counter1 = 2

    if (ir2_read == 0 and turn_counter2 == 0):
        turn_counter2 = 1

    elif (ir2_read == 1 and turn_counter2 == 1):
        turn_counter2 = 2

def read_sensors():
    global ir1_read, ir2_read, force_read

    ir1_read = pins.digital_read_pin(ir1)
    ir2_read = pins.digital_read_pin(ir2)
    force_read = pins.digital_read_pin(force)

def check_angle():
    if (isTurning or not active):
        return

    if (ir1_read == 0 and ir2_read == 1):
        isOffCourse = True

    elif (ir1_read == 1 and ir2_read == 0):
        isOffCourse = True

    else:
        isOffCourse = False

def adjust_angle():
    global isOffCourse
    global direction

    if (not isOffCourse or not active):
        return

    set_gb(direction, turn_speed, direction, turn_speed)

# Utility
def stop():
    sensors.dd_mmotor(gb1_direction, 0, gb1_speed, 0)
    sensors.dd_mmotor(gb2_direction, 0, gb2_speed, 0)

def set_gb(gb1_dir, gb1_spd, gb2_dir, gb2_spd):
    sensors.dd_mmotor(gb1_direction, gb1_dir, gb1_speed, gb1_spd)
    sensors.dd_mmotor(gb2_direction, gb2_dir, gb2_speed, gb2_spd)

# Pins
force = DigitalPin.P20

ir1 = DigitalPin.P1
ir2 = DigitalPin.P8

gb1_speed = AnalogPin.P14
gb1_direction = AnalogPin.P13

gb2_speed = AnalogPin.P16
gb2_direction = AnalogPin.P15

# Pin values
force_read = 0
ir1_read = 0
ir2_read = 0

# Directions for turning and moving
direction = 0
turn_direction = 0

# Speeds and offsets incase one side is faster then the other (they are)
speed = 100
speed_offset1 = 0
speed_offset2 = 0

turn_speed = 250
turn_speed_offset1 = 0
turn_speed_offset2 = 0

active = False

# Keep track of how many intersections the car has passed
intersectionCount = 0

# Flags for callback functions
atIntersection = False
isMoving = True
isTurning = False
isOffCourse = False

turn_counter1 = 0
turn_counter2 = 0

basic.forever(read_sensors)
basic.forever(main)
basic.forever(check_angle)
basic.forever(adjust_angle)
basic.forever(turn)