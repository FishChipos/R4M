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
    global curr_time, move_elapsed, adjust_elapsed

    state = 0
    
    set_gb(direction, speed, 1 - direction, speed)

    '''
    else:
        move_elapsed = 0

        last_move_time = control.millis()

        while move_elapsed <= time:
            set_gb(direction, speed, 1 - direction, speed)

            move_elapsed += curr_time - last_move_time

            if (adjust_elapsed != 0):
                move_elapsed -= adjust_elapsed
                adjust_elapsed = 0

        stop()
    '''

# MODIFIES: state
def turn():
    global active, state, count 
    global turn_direction, turn_speed
    global ir1_read, ir2_read

    state = 1

    ir1_read_last = ir1_read
    ir2_read_last = ir2_read

    counter1 = 0
    counter2 = 0

    counter = 0

    while counter != count :
        basic.pause(40)

        stop()

        # Don't delete this
        basic.show_number(counter1 + counter2)

        if (counter1 + counter2 >= 4 and counter >= 10):
            stop()
            return

        if (ir1_read != ir1_read_last):
            ir1_read_last = ir1_read

            if (counter1 == 0):
                counter1 = 1

            elif (counter1 == 1):
                counter1 = 2

        if (ir2_read != ir2_read_last):
            ir2_read_last = ir2_read

            if (counter2 == 0):
                counter2 = 1

            elif (counter2 == 1):
                counter2 = 2

        set_gb(turn_direction, turn_speed, turn_direction, turn_speed)

        counter += 1
        
    stop()

# MODIFIES: state
def stop():
    global active, state

    basic.pause(10)
    
    state = 2

    set_gb(0, 0, 0, 0)
    

# MODIFIES: turn_direction
def adjust():
    global ir1_read, ir2_read
    global adjust_ac
    global intersection_seen
    global active, state
    global adjust_speed
    global last_adjust_time, curr_time, adjust_elapsed

    if active != 1:
        return

    if adjust_ac != 1:
        return

    if state != 0:
        return

    if (check_inter()):
        intersection_seen = 1
        return

    elif (check_angle()):
        stop()

        # last_adjust_time = control.millis()

        if (ir1_read == 0 and ir2_read == 1):
            set_gb(0, adjust_speed, 0, adjust_speed)
            state = 0

        if (ir1_read == 1 and ir2_read == 0):
            set_gb(1, adjust_speed, 1, adjust_speed)
            state = 0

        basic.pause(100)

        move()

        # adjust_elapsed += curr_time - last_adjust_time

    else:
        move()

# For use with adjusting
def check_angle():
    global ir1_read, ir2_read

    # Time for sensors to update
    basic.pause(10)

    if (ir1_read == 0 and ir2_read == 0):
        return 0

    elif (ir1_read == 0 or ir2_read == 0):
        return 1

    return 0

# MODIFIES: ir1_read, ir2_read, ir3_read, ir4_read, force_read
def read_pins():
    global ir1_read, ir2_read, ir3_read, ir4_read, force_read

    ir1_read = pins.digital_read_pin(ir1)
    ir2_read = pins.digital_read_pin(ir2)
    ir3_read = pins.digital_read_pin(ir3)
    ir4_read = pins.digital_read_pin(ir4)

    force_read = pins.digital_read_pin(force)

# MODIFIES: curr_time
def update_time():
    global curr_time, last_time

    curr_time = control.millis()

# Utility function to set both gearboxes at the same time
def set_gb(dir1, spd1, dir2, spd2):
    sensors.dd_mmotor(gb1_direction, dir1, gb1_speed, spd1)
    sensors.dd_mmotor(gb2_direction, dir2, gb2_speed, spd2)

# Check if its at intersection
def check_inter():
    global ir1_read, ir2_read
      
    if (ir1_read == 1 and ir2_read == 1):
        music.play_tone(Note.C, 50)
        return True

    return False

def check_food():
    global ir3_read, ir4_read

    if (ir3_read == 0):
        return 1

    elif (ir4_read == 0):
        return 1

    else:
        return 0

# --- PINS ---
force = DigitalPin.P20

# 2 follow line sensors
ir1 = DigitalPin.P1
ir2 = DigitalPin.P8

# Front sensor
ir3 = DigitalPin.P12
ir5 = DigitalPin.P0

# Back sensor
ir4 = DigitalPin.P2
ir6 = DigitalPin.P0

# Right gearbox
gb1_speed = AnalogPin.P14
gb1_direction = AnalogPin.P13

# Left gearbox
gb2_speed = AnalogPin.P16
gb2_direction = AnalogPin.P15
# ---------

# Pin values
force_read = 0
ir1_read = 0
ir2_read = 0
ir3_read = 0
ir4_read = 0
ir5_read = 0
ir6_read = 0

# Directions for turning and moving (0 is right, 1 is left)
direction = 0
turn_direction = 0

# Speeds
speed = 78
turn_speed = 220
adjust_speed = 110

# Flags (0 -> false, 1 -> true)
active = 0
adjust_ac = 1
intersection_seen = 0

# State (0 -> moving, 1 -> turning, 2 -> still, 3 -> special)
state = 0

# Intersection count
intersection_count = 0

# Current and last time for counting time elapsed
curr_time = control.millis()
last_time = control.millis()

# Time it took for robot to finish one move or adjust operation
move_elapsed = 0
adjust_elapsed = 0

last_move_time = 0
last_adjust_time = 0

count = 0 

# Run these functions in the background
basic.forever(read_pins)
# basic.forever(update_time)
basic.forever(adjust)

def reset_var():
    global adjust_ac, intersection_seen

    adjust_ac = 1
    intersection_seen = 0

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
    global intersection_count

    basic.show_number(state)

    first()

basic.forever(start)

# Algorithms for each section
def first():
    global adjust_ac, intersection_seen, count 
    global direction, turn_direction
    global intersection_count

    adjust_ac = 0

    direction = 0
    move()
    
    basic.pause(500)

    basic.show_number(9)

    adjust_ac = 1

    direction = 0
    move()

    intersection_seen = 0

    while True:
        move()
        basic.pause(20)
        if (check_inter() or intersection_seen):
            intersection_seen = 0

            adjust_ac = 0

            # Move forward a little
            direction = 0
            move()
            basic.pause(1200)

            stop()

            # Left food
            count = 10 
            turn_direction = 1
            turn()

            adjust_ac = 1

            direction = 0
            move()

            basic.pause(600)
            
            while not check_food():
                basic.pause(10)

            stop()

            adjust_ac = 0

            direction = 0
            move()
            basic.pause(1000)

            stop()

            # Right food

            direction = 1
            move()
            
            basic.pause(1000)

            while not check_food():
                basic.pause(10)

            stop()

            direction = 1
            move()
            basic.pause(900)

            stop()

            direction = 0
            move()
            basic.pause(700)

            adjust_ac = 0

            direction = 0
            move()
            basic.pause(1300)

            stop()

            count = 11 

            turn_direction = 0
            turn()

            intersection_count += 1

            break

    second()

def second():
    global adjust_ac, intersection_seen
    global direction, turn_direction
    global intersection_count, count 

    reset_var()

    basic.show_number(8)

    stop()

    direction = 0
    move()

    while True:
        move()
        basic.pause(20)
        if (check_inter() or intersection_seen):
            intersection_seen = 0

            adjust_ac = 0

            direction = 0
            move()
            basic.pause(1400)

            stop()
            count = 12
            turn_direction = 1
            turn()

            adjust_ac = 1

            direction = 0
            move()

            while not check_food():
                basic.pause(20)

            adjust_ac = 0

            direction = 0
            move()
            basic.pause(2000)

            stop()

            direction = 1
            move()
            
            basic.pause(3000)

            direction = 0
            move()
            basic.pause(1300)

            stop()

            turn_direction = 0
            turn()

            intersection_count += 1

    third()
        
def third():
    global adjust_ac, intersection_seen
    global direction, turn_direction
    global intersection_count, count 

    reset_var()

    basic.show_number(7)

    stop()

    direction = 0
    move()

    while True:
        move()
        basic.pause(20)
        if (check_inter() or intersection_seen):
            intersection_seen = 0

            adjust_ac = 0

            direction = 0
            move()
            basic.pause(1600)

            stop()

            count = 12

            turn_direction = 1
            turn()

            adjust_ac = 1

            direction = 0
            move()

            while not check_food():
                basic.pause(20)

            adjust_ac = 0

            direction = 0
            move()
            basic.pause(1500)

            stop()

            direction = 1
            move()
            basic.pause(3000)

            direction = 0
            move()
            basic.pause(1500)

            stop()

            turn_direction = 0
            turn()

            intersection_count += 1

    fourth()

def fourth():
    global adjust_ac, intersection_seen
    global direction, turn_direction
    global intersection_count, count 

    reset_var()

    basic.show_number(6)

    stop()

    direction = 1
    move()  
    basic.pause(1000)

    stop()

    direction = 0
    move()
   
    while True:
        move()
        basic.pause(20)
        if (check_inter() or intersection_seen):
            stop()

            direction = 0
            move()
            basic.pause(1500)
            
            turn_direction = 1
            turn()

            stop()

            direction = 0
            move()

            while not check_food():
                basic.pause(20)

            direction = 0
            move()
            basic.pause(1500)

            stop()

            direction = 1
            move()

            while not check_food():
                basic.pause(10) 

            basic.pause(1500)
            stop() 

            direction = 0
            move()

            while not (check_inter() or intersection_seen):
                basic.pause(20)

            basic.pause(1400)

            stop()

            turn_direction = 0 
            turn()

    last()

def last():
    global adjust_ac, intersection_seen
    global direction, turn_direction
    global intersection_count, count

    reset_var()

    basic.show_number(5)

    stop()

    direction = 0
    move()
    
    while True:
        move()
        basic.pause(20)
        if check_inter() or intersection_seen:
            stop()

            direction = 0
            move()
            basic.pause(1500)
            
            turn_direction = 1
            turn()

            stop()

            direction = 0
            move()

            intersection_seen = 0
            while not (check_inter() or intersection_seen):
                basic.pause(20)

            basic.pause(1500)

            stop()

    active = 0
    return