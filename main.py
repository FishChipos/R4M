# NOTES:
# 1 is left and back, 0 is right and front
# 1 is black, 0 is white

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
        # atIntersection = True
        pass

    if (not atIntersection and not isOffCourse):
        isMoving = True
        isTurning = False

def move():
    global isMoving, isTurning, direction

    if (not isMoving or isTurning or not active):
        return

    set_gb(direction, speed, 1 - direction, speed)

def turn():
    global isTurning, atIntersection, turn_direction
    global ir1_read, ir2_read 
    global turn_counter1, turn_counter2

    if (not isTurning or isMoving or not active):
        return

    set_gb(turn_direction, turn_speed, turn_direction, turn_speed)

    if (turn_counter1 + turn_counter2 >= 4):
        isTurning = False
        isMoving = True
        atIntersection = False
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
    global isMoving, isTurning, active, turn_direction, isOffCourse
    global ir1_read, ir2_read

    if isOffCourse:
        basic.show_number(1)

    else:
        basic.show_number(0)

    if (ir1_read == 1 and ir2_read == 0):
        turn_direction = 1
        isMoving = False
        isOffCourse = True

    elif (ir1_read == 0 and ir2_read == 1):
        turn_direction = 0
        isMoving = False
        isOffCourse = True

    if isOffCourse:
        adjust_angle()

def adjust_angle():
    global turn_direction, turn_speed, isOffCourse, ir1_read, ir2_read

    while isOffCourse:
        set_gb(turn_direction, turn_speed, turn_direction, turn_speed)

        if (ir1_read == 1 and ir2_read == 1):
            isOffCourse = False
            return

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
speed = 250
speed_offset1 = 0
speed_offset2 = 0

turn_speed = 150
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
basic.forever(move)