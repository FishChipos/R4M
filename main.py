# NOTES:
# 1 is left, 0 is right
# 1 is back, 0 is front
# 1 is IR sees black or any sufficiently dark color, 
# 0 is IR sees white or any sufficiently light color

# Black magic don't touch
pins.set_pull(DigitalPin.P20, PinPullMode.PULL_UP)

# MODIFIES: NONE
def move():
    global active, state
    global direction, speed

    if active != 1:
        return

    # Only when moving
    if state == 0:     
        set_gb(direction, speed, 1 - direction, speed)
    

# MODIFIES: adjusting, turn_direction, state
def adjust():
    global ir1_read, ir2_read
    global active, state
    global turn_direction, turn_speed

    if active != 1:
        return

    # If both sensors sense white then back on track (maybe)
    if (ir1_read == 1 and ir2_read == 1 and state == 1):
        state = 0

    elif ((ir1_read == 0 or ir2_read == 0) and not (ir1_read == 0 and ir2_read == 0) and state == 0):
        state = 1

    # If adjusting
    if (state == 1):
        # If the left sensor senses black then turn right
        if (ir1_read == 0 and ir2_read == 1):
            turn_direction = 0

        # Otherwise turn left
        elif (ir1_read == 1 and ir2_read == 0):
            turn_direction = 1

        basic.show_number(turn_direction)

        set_gb(turn_direction, turn_speed, turn_direction, turn_speed)

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
speed = 60
speed_offset1 = 0
speed_offset2 = 0

turn_speed = 120
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

def main():
    global ir1_read, ir2_read, force_read
    global active, state

    # Once the button is pressed activate
    if (force_read == 0 and active == 0):
        active = 1

    elif (force_read == 0 and active == 1):
        # Reset
        active = 0
        intersections = [0, 0, 0, 0]
        state = 0

    if (active):
        basic.show_number(state)

basic.forever(main)

    