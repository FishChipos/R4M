# NOTES:
# 1 is left, 0 is right
# 1 is back, 0 is front
# 1 is IR sees black or any sufficiently dark color, 
# 0 is IR sees white or any sufficiently light color

# Black magic don't touch
pins.set_pull(DigitalPin.P20, PinPullMode.PULL_UP)

# MODIFIES: NONE
def move():
    global state
    global direction, speed

    # Only when moving
    if (state == 0):
        set_gb(direction, speed, 1 - direction, speed)

# MODIFIES: adjusting, turn_direction
def adjust():
    global ir1_read, ir2_read
    global state
    global turn_direction, turn_speed

    # If not adjusting then don't do anything
    if (state != 1):
        return

    # If one of the sensors sense black
    elif (ir1_read == 0 ^ ir2_read == 0):
        # If the left sensor doesn't sense black then turn right
        if (ir1_read == 1):
            turn_direction = 0

        # Otherwise turn left
        elif (ir2_read == 1):
            turn_direction = 1

        set_gb(turn_direction, turn_speed, turn_direction, turn_speed)

# MODIFIES: ir1_read, ir2_read, force_read
def read_pins():
    global ir1_read, ir2_read, force_read

    ir1_read = pins.digital_read_pin(ir1)
    ir2_read = pins.digital_read_pin(ir2)
    force_read = pins.digital_read_pin(force)

def set_gb(dir1, spd1, dir2, spd2):
    sensors.dd_mmotor(gb1_direction, dir1, gb1_speed, spd1)
    sensors.dd_mmotor(gb2_direction, dir2, gb2_speed, spd2)

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
speed = 100
speed_offset1 = 0
speed_offset2 = 0

turn_speed = 150
turn_speed_offset1 = 0
turn_speed_offset2 = 0

# Flags (0 -> false, 1 -> true)
active = 0

# State (0 -> moving, 1 -> adjusting, 2 -> turning)
state = 0

# Array containing flags for each intersection passed
# E.G. 
# when passing the first intersection the first element will be set to one
# when passing the second intersection the second element will be set to one
# and so on
intersections = [0, 0, 0, 0]

# Run these functions in the background
basic.forever(read_pins)
basic.forever(move)
basic.forever(adjust)

# Main loop
while True:
    # Once the button is pressed activate
    if (force_read == 0 and active == 0):
        active = 1

    elif (force_read == 0 and active == 1):
        # Reset
        active = 0
        intersections = [0, 0, 0, 0]
        state = 0

    if (active):
        # At intersection
        if (ir1_read == 0 and ir2_read == 0):
            pass

        # Off course
        elif (ir1_read == 0 ^ ir2_read == 0):
            state = 1

        # Otherwise by default move forward
        elif (ir1_read == 1 and ir2_read == 1):
            state = 0