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
}

//  MODIFIES: state
function turn() {
    
    
    
    state = 1
    let counter1 = 0
    let counter2 = 0
    while (true) {
        set_gb(turn_direction, turn_speed, turn_direction, turn_speed)
        basic.pause(80)
        stop()
        basic.showNumber(counter1 + counter2)
        if (counter1 + counter2 >= 4) {
            stop()
            return
        }
        
        if (counter1 == 0 && ir1_read == 0) {
            counter1 = 1
        }
        
        if (counter1 == 1 && ir1_read == 1) {
            counter1 = 2
        }
        
        if (counter2 == 0 && ir2_read == 0) {
            counter2 = 1
        }
        
        if (counter2 == 1 && ir2_read == 1) {
            counter2 = 2
        }
        
    }
}

//  MODIFIES: state
function stop() {
    
    state = 2
    set_gb(0, 0, 0, 0)
}

//  MODIFIES: turn_direction
//  For use with adjusting
function check_angle(): number {
    
    if (ir1_read == 1 && ir2_read == 1) {
        return 2
    } else if (ir1_read == 0 && ir2_read == 0) {
        return 0
    } else if (ir1_read == 0 || ir2_read == 0) {
        return 1
    }
    
    return 0
}

//  MODIFIES: ir1_read, ir2_read, force_read
//  Utility function to set both gearboxes at the same time
function set_gb(dir1: number, spd1: number, dir2: number, spd2: number) {
    sensors.DDMmotor(gb1_direction, dir1, gb1_speed, spd1)
    sensors.DDMmotor(gb2_direction, dir2, gb2_speed, spd2)
}

//  Check if its at intersection
function check_inter(): boolean {
    
    if (ir1_read == 1 && ir2_read == 1) {
        return true
    }
    
    return false
}

//  Pins
let force = DigitalPin.P20
let ir1 = DigitalPin.P1
let ir2 = DigitalPin.P8
let gb1_speed = AnalogPin.P14
let gb1_direction = AnalogPin.P13
let gb2_speed = AnalogPin.P16
let gb2_direction = AnalogPin.P15
//  Pin values
let force_read = 0
let ir1_read = 0
let ir2_read = 0
//  Directions for turning and moving (0 is right, 1 is left)
let direction = 0
let turn_direction = 0
//  Speeds and offsets incase one side is faster then the other (they are)
let speed = 75
let turn_speed = 180
let adjust_speed = 120
//  Flags (0 -> false, 1 -> true)
let active = 0
let main_ac = 1
let adjust_ac = 1
let intersection_seen = 0
//  State (0 -> moving, 1 -> turning, 2 -> still, 3 -> special)
let state = 0
//  Intersection count
let intersectionCount = 0
//  Run these functions in the background
basic.forever(function read_pins() {
    
    ir1_read = pins.digitalReadPin(ir1)
    ir2_read = pins.digitalReadPin(ir2)
    force_read = pins.digitalReadPin(force)
})
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
    
    if (check_angle() == 2) {
        intersection_seen = 1
        return
    } else if (check_angle()) {
        stop()
        if (ir1_read == 0 && ir2_read == 1) {
            set_gb(0, adjust_speed, 0, adjust_speed)
            state = 0
        }
        
        if (ir1_read == 1 && ir2_read == 0) {
            set_gb(1, adjust_speed, 1, adjust_speed)
            state = 0
        }
        
    } else {
        move()
    }
    
})
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
    
    
    
    basic.showNumber(9)
    main_ac = 0
    stop()
    direction = 0
    move()
    while (true) {
        if (check_inter() || intersection_seen) {
            intersection_seen = 0
            stop()
            //  Move forward a little
            move()
            basic.pause(800)
            stop()
            //  Turn left
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
        }
        
        basic.pause(20)
    }
}

function second() {
    
    
    
    basic.showNumber(8)
    stop()
    direction = 0
    move()
    while (true) {
        if (check_inter() || intersection_seen) {
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
        }
        
    }
}

function third() {
    
}

