# NOTES:
# 1 is left, 0 is right
# 1 is back, 0 is front
# 1 is IR sees black or any sufficiently dark color, 
# 0 is IR sees white or any sufficiently light color

# Black magic don't touch
pins.set_pull(DigitalPin.P20, PinPullMode.PULL_UP)

# MODIFIES: state
def move():
    global active, state
    global direction, speed

    state = 0
    
    set_gb(direction, speed, 1 - direction, speed)

# MODIFIES: state
def turn():
    global active, state
    global turn_direction, turn_speed
    global ir1_read, ir2_read

    state = 1

    counter1 = 0
    counter2 = 0

    while True:
        set_gb(turn_direction, turn_speed, turn_direction, turn_speed)

        basic.pause(80)

        stop()

        basic.show_number(counter1 + counter2)

        if (counter1 + counter2 >= 4):
            stop()
            return

        if (counter1 == 0 and ir1_read == 0):
            counter1 = 1

        if (counter1 == 1 and ir1_read == 1):
            counter1 = 2

        if (counter2 == 0 and ir2_read == 0):
            counter2 = 1

        if (counter2 == 1 and ir2_read == 1):
            counter2 = 2

# MODIFIES: state
def stop():
    global active, state
    
    state = 2

    set_gb(0, 0, 0, 0)
    

# MODIFIES: turn_direction
def adjust():
    global ir1_read, ir2_read
    global adjust_ac
    global intersection_seen
    global active, state
    global adjust_speed

    if active != 1:
        return

    if adjust_ac != 1:
        return

    if state != 0:
        return

    if (check_angle() == 2):
        intersection_seen = 1
        return

    elif (check_angle()):
        stop()

        if (ir1_read == 0 and ir2_read == 1):
            set_gb(0, adjust_speed, 0, adjust_speed)
            state = 0

        if (ir1_read == 1 and ir2_read == 0):
            set_gb(1, adjust_speed, 1, adjust_speed)
            state = 0

    else:
        move()

# For use with adjusting
def check_angle():
    global ir1_read, ir2_read

    if (ir1_read == 1 and ir2_read == 1):
        return 2

    elif (ir1_read == 0 and ir2_read == 0):
        return 0

    elif (ir1_read == 0 or ir2_read == 0):
        return 1

    return 0

# MODIFIES: ir1_read, ir2_read, force_read
def read_pins():
    global ir1_read, ir2_read, force_read

    ir1_read = pins.digital_read_pin(ir1)
    ir2_read = pins.digital_read_pin(ir2)
    force_read = pins.digital_read_pin(force)

# Utility function to set both gearboxes at the same time
def set_gb(dir1, spd1, dir2, spd2):
    sensors.dd_mmotor(gb1_direction, dir1, gb1_speed, spd1)
    sensors.dd_mmotor(gb2_direction, dir2, gb2_speed, spd2)

# Check if its at intersection
def check_inter():
    global ir1_read, ir2_read
      
    if (ir1_read == 1 and ir2_read == 1):
        return True

    return False

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

# Directions for turning and moving (0 is right, 1 is left)
direction = 0
turn_direction = 0

# Speeds and offsets incase one side is faster then the other (they are)
speed = 75
turn_speed = 180
adjust_speed = 120

# Flags (0 -> false, 1 -> true)
active = 0
main_ac = 1
adjust_ac = 1
intersection_seen = 0

# State (0 -> moving, 1 -> turning, 2 -> still, 3 -> special)
state = 0

# Intersection count
intersectionCount = 0

# Run these functions in the background
basic.forever(read_pins)
basic.forever(adjust)

def start():
    global force_read
    global active

    # Once the button is pressed activate
    if (force_read == 0 and active == 0):
        active = 1
        basic.pause(500)
        first()

    elif (force_read == 0 and active == 1):
        # Reset
        control.reset()

def main():
    global ir1_read, ir2_read, force_read
    global active, state
    global intersectionCount

    basic.show_number(state)

    first()

basic.forever(start)

# Algorithms for each section
def first():
    global main_ac, adjust_ac, intersection_seen
    global direction, turn_direction
    global intersectionCount

    basic.show_number(9)

    main_ac = 0

    stop()

    direction = 0
    move()

    while True:
        if (check_inter() or intersection_seen):
            intersection_seen = 0
            stop()

            # Move forward a little
            move()
            basic.pause(800)

            stop()

            # Turn left
            turn_direction = 1
            turn()

            move()
            basic.pause(4000)

            stop()

            direction = 1
            move()
            basic.pause(8000)

            stop()

            adjust_ac = 0

            direction = 0
            move()
            basic.pause(4000)

            stop()

            turn_direction = 0
            turn()

            intersectionCount += 1

            second()

        basic.pause(20)

def second():
    global main_ac, adjust_ac, intersection_seen
    global direction, turn_direction
    global intersectionCount

    basic.show_number(8)

    stop()

    direction = 0

    move()

    while True:
        if (check_inter() or intersection_seen):
            intersection_seen = 0
            stop()

            move()
            basic.pause(800)

            stop()

            turn_direction = 1
            turn()

            move()
            basic.pause(4000)

            stop()

            direction = 1
            move()
            basic.pause(4000)

            stop()

            turn_direction = 0
            turn()

            intersectionCount += 1

            third()

def third():
    pass