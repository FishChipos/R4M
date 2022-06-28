//  NOTES:
//  1 is left and back, 0 is right and front
//  Black magic don't touch
pins.setPull(DigitalPin.P20, PinPullMode.PullUp)
//  Main logic and callback functions
function move() {
    
    if (!isMoving || isTurning || !active) {
        return
    }
    
    set_gb(direction, speed, 1 - direction, speed)
}

//  Utility
function stop() {
    sensors.DDMmotor(gb1_direction, 0, gb1_speed, 0)
    sensors.DDMmotor(gb2_direction, 0, gb2_speed, 0)
}

function set_gb(gb1_dir: number, gb1_spd: number, gb2_dir: number, gb2_spd: number) {
    sensors.DDMmotor(gb1_direction, gb1_dir, gb1_speed, gb1_spd)
    sensors.DDMmotor(gb2_direction, gb2_dir, gb2_speed, gb2_spd)
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
//  Directions for turning and moving
let direction = 0
let turn_direction = 0
//  Speeds and offsets incase one side is faster then the other (they are)
let speed = 100
let speed_offset1 = 0
let speed_offset2 = 0
let turn_speed = 250
let turn_speed_offset1 = 0
let turn_speed_offset2 = 0
let active = false
//  Keep track of how many intersections the car has passed
let intersectionCount = 0
//  Flags for callback functions
let atIntersection = false
let isMoving = true
let isTurning = false
let isOffCourse = false
let turn_counter1 = 0
let turn_counter2 = 0
basic.forever(function read_sensors() {
    
    ir1_read = pins.digitalReadPin(ir1)
    ir2_read = pins.digitalReadPin(ir2)
    force_read = pins.digitalReadPin(force)
})
basic.forever(function main() {
    let turn_direction: number;
    
    
    
    if (force_read == 0 && !active) {
        active = true
    } else if (force_read == 0 && active) {
        active = false
    }
    
    if (!active) {
        return
    }
    
    if (ir1_read == 0 && ir2_read == 0) {
        atIntersection = true
    }
    
    if (!atIntersection) {
        isMoving = true
    }
    
    if (atIntersection && !isTurning) {
        isTurning = true
        intersectionCount += 1
        atIntersection = false
        if (intersectionCount == 1) {
            turn_direction = 1
            
        } else if (intersectionCount == 2) {
            
        } else if (intersectionCount == 3) {
            
        } else if (intersectionCount == 4) {
            
        }
        
    }
    
})
basic.forever(function check_angle() {
    let isOffCourse: boolean;
    if (isTurning || !active) {
        return
    }
    
    if (ir1_read == 0 && ir2_read == 1) {
        isOffCourse = true
    } else if (ir1_read == 1 && ir2_read == 0) {
        isOffCourse = true
    } else {
        isOffCourse = false
    }
    
})
basic.forever(function adjust_angle() {
    
    
    if (!isOffCourse || !active) {
        return
    }
    
    set_gb(direction, turn_speed, direction, turn_speed)
})
basic.forever(function turn() {
    
    
    
    if (!isTurning || !active) {
        return
    }
    
    set_gb(turn_direction, turn_speed, turn_direction, turn_speed)
    if (turn_counter1 + turn_counter2 >= 4) {
        isTurning = false
        turn_counter1 = 0
        turn_counter2 = 0
        return
    }
    
    if (ir1_read == 0 && turn_counter1 == 0) {
        turn_counter1 = 1
    } else if (ir1_read == 1 && turn_counter1 == 1) {
        turn_counter1 = 2
    }
    
    if (ir2_read == 0 && turn_counter2 == 0) {
        turn_counter2 = 1
    } else if (ir2_read == 1 && turn_counter2 == 1) {
        turn_counter2 = 2
    }
    
})
