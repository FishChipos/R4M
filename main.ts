//  NOTES:
//  1 is left, 0 is right
//  1 is back, 0 is front
//  1 is IR sees black or any sufficiently dark color, 
//  0 is IR sees white or any sufficiently light color
//  Black magic don't touch
pins.setPull(DigitalPin.P20, PinPullMode.PullUp)
//  MODIFIES: state
function move() {
    
    
    
    state = 0
    set_gb(direction, speed, 1 - direction, speed)
    /** 
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
    
 */
}

//  MODIFIES: state
function turn() {
    
    
    
    state = 1
    let ir1_read_last = ir1_read
    let ir2_read_last = ir2_read
    let counter1 = 0
    let counter2 = 0
    let counter = 0
    while (counter != count) {
        basic.pause(40)
        stop()
        //  Don't delete this
        basic.showNumber(counter1 + counter2)
        if (counter1 + counter2 >= 4 && counter >= 10) {
            stop()
            return
        }
        
        if (ir1_read != ir1_read_last) {
            ir1_read_last = ir1_read
            if (counter1 == 0) {
                counter1 = 1
            } else if (counter1 == 1) {
                counter1 = 2
            }
            
        }
        
        if (ir2_read != ir2_read_last) {
            ir2_read_last = ir2_read
            if (counter2 == 0) {
                counter2 = 1
            } else if (counter2 == 1) {
                counter2 = 2
            }
            
        }
        
        set_gb(turn_direction, turn_speed, turn_direction, turn_speed)
        counter += 1
    }
    stop()
}

//  MODIFIES: state
function stop() {
    
    basic.pause(10)
    state = 2
    set_gb(0, 0, 0, 0)
}

//  MODIFIES: turn_direction
//  For use with adjusting
function check_angle(): number {
    
    //  Time for sensors to update
    basic.pause(10)
    if (ir1_read == 0 && ir2_read == 0) {
        return 0
    } else if (ir1_read == 0 || ir2_read == 0) {
        return 1
    }
    
    return 0
}

//  MODIFIES: ir1_read, ir2_read, ir3_read, ir4_read, force_read
//  MODIFIES: curr_time
function update_time() {
    
    curr_time = control.millis()
}

//  Utility function to set both gearboxes at the same time
function set_gb(dir1: number, spd1: number, dir2: number, spd2: number) {
    sensors.DDMmotor(gb1_direction, dir1, gb1_speed, spd1)
    sensors.DDMmotor(gb2_direction, dir2, gb2_speed, spd2)
}

//  Check if its at intersection
function check_inter(): boolean {
    
    if (ir1_read == 1 && ir2_read == 1) {
        music.playTone(Note.C, 50)
        return true
    }
    
    return false
}

function check_food(): number {
    
    if (ir3_read == 0) {
        return 1
    } else if (ir4_read == 0) {
        return 1
    } else {
        return 0
    }
    
}

//  --- PINS ---
let force = DigitalPin.P20
//  2 follow line sensors
let ir1 = DigitalPin.P1
let ir2 = DigitalPin.P8
//  Front sensor
let ir3 = DigitalPin.P12
let ir5 = DigitalPin.P0
//  Back sensor
let ir4 = DigitalPin.P2
let ir6 = DigitalPin.P0
//  Right gearbox
let gb1_speed = AnalogPin.P14
let gb1_direction = AnalogPin.P13
//  Left gearbox
let gb2_speed = AnalogPin.P16
let gb2_direction = AnalogPin.P15
//  ---------
//  Pin values
let force_read = 0
let ir1_read = 0
let ir2_read = 0
let ir3_read = 0
let ir4_read = 0
let ir5_read = 0
let ir6_read = 0
//  Directions for turning and moving (0 is right, 1 is left)
let direction = 0
let turn_direction = 0
//  Speeds
let speed = 78
let turn_speed = 220
let adjust_speed = 110
//  Flags (0 -> false, 1 -> true)
let active = 0
let adjust_ac = 1
let intersection_seen = 0
//  State (0 -> moving, 1 -> turning, 2 -> still, 3 -> special)
let state = 0
//  Intersection count
let intersection_count = 0
//  Current and last time for counting time elapsed
let curr_time = control.millis()
let last_time = control.millis()
//  Time it took for robot to finish one move or adjust operation
let move_elapsed = 0
let adjust_elapsed = 0
let last_move_time = 0
let last_adjust_time = 0
let count = 0
//  Run these functions in the background
basic.forever(function read_pins() {
    
    ir1_read = pins.digitalReadPin(ir1)
    ir2_read = pins.digitalReadPin(ir2)
    ir3_read = pins.digitalReadPin(ir3)
    ir4_read = pins.digitalReadPin(ir4)
    force_read = pins.digitalReadPin(force)
})
//  basic.forever(update_time)
basic.forever(function adjust() {
    
    
    
    
    
    
    if (active != 1) {
        return
    }
    
    if (adjust_ac != 1) {
        return
    }
    
    if (state != 0) {
        return
    }
    
    if (check_inter()) {
        intersection_seen = 1
        return
    } else if (check_angle()) {
        stop()
        //  last_adjust_time = control.millis()
        if (ir1_read == 0 && ir2_read == 1) {
            set_gb(0, adjust_speed, 0, adjust_speed)
            state = 0
        }
        
        if (ir1_read == 1 && ir2_read == 0) {
            set_gb(1, adjust_speed, 1, adjust_speed)
            state = 0
        }
        
        basic.pause(100)
        move()
    } else {
        //  adjust_elapsed += curr_time - last_adjust_time
        move()
    }
    
})
function reset_var() {
    
    adjust_ac = 1
    intersection_seen = 0
}

function main() {
    
    
    
    basic.showNumber(state)
    first()
}

basic.forever(function start() {
    
    
    //  Once the button is pressed activate
    if (force_read == 0 && active == 0) {
        active = 1
        basic.pause(500)
        first()
    } else if (force_read == 0 && active == 1) {
        //  Reset
        control.reset()
    }
    
})
//  Algorithms for each section
function first() {
    
    
    
    adjust_ac = 0
    direction = 0
    move()
    basic.pause(500)
    basic.showNumber(9)
    adjust_ac = 1
    direction = 0
    move()
    intersection_seen = 0
    while (true) {
        move()
        basic.pause(20)
        if (check_inter() || intersection_seen) {
            intersection_seen = 0
            adjust_ac = 0
            //  Move forward a little
            direction = 0
            move()
            basic.pause(1200)
            stop()
            //  Left food
            count = 10
            turn_direction = 1
            turn()
            adjust_ac = 1
            direction = 0
            move()
            basic.pause(600)
            while (!check_food()) {
                basic.pause(10)
            }
            stop()
            adjust_ac = 0
            direction = 0
            move()
            basic.pause(1000)
            stop()
            //  Right food
            direction = 1
            move()
            basic.pause(1000)
            while (!check_food()) {
                basic.pause(10)
            }
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
        }
        
    }
    second()
}

function second() {
    
    
    
    reset_var()
    basic.showNumber(8)
    stop()
    direction = 0
    move()
    while (true) {
        move()
        basic.pause(20)
        if (check_inter() || intersection_seen) {
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
            while (!check_food()) {
                basic.pause(20)
            }
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
        }
        
    }
    third()
}

function third() {
    
    
    
    reset_var()
    basic.showNumber(7)
    stop()
    direction = 0
    move()
    while (true) {
        move()
        basic.pause(20)
        if (check_inter() || intersection_seen) {
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
            while (!check_food()) {
                basic.pause(20)
            }
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
        }
        
    }
    fourth()
}

function fourth() {
    
    
    
    reset_var()
    basic.showNumber(6)
    stop()
    direction = 1
    move()
    basic.pause(1000)
    stop()
    direction = 0
    move()
    while (true) {
        move()
        basic.pause(20)
        if (check_inter() || intersection_seen) {
            stop()
            direction = 0
            move()
            basic.pause(1500)
            turn_direction = 1
            turn()
            stop()
            direction = 0
            move()
            while (!check_food()) {
                basic.pause(20)
            }
            direction = 0
            move()
            basic.pause(1500)
            stop()
            direction = 1
            move()
            while (!check_food()) {
                basic.pause(10)
            }
            basic.pause(1500)
            stop()
            direction = 0
            move()
            while (!(check_inter() || intersection_seen)) {
                basic.pause(20)
            }
            basic.pause(1400)
            stop()
            turn_direction = 0
            turn()
        }
        
    }
    last()
}

function last() {
    
    
    
    reset_var()
    basic.showNumber(5)
    stop()
    direction = 0
    move()
    while (true) {
        move()
        basic.pause(20)
        if (check_inter() || intersection_seen) {
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
            while (!(check_inter() || intersection_seen)) {
                basic.pause(20)
            }
            basic.pause(1500)
            stop()
        }
        
    }
    let active = 0
    return
}

