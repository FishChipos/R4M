//  NOTES:
//  1 is left, 0 is right
//  1 is back, 0 is front
//  1 is IR sees black or any sufficiently dark color, 
//  0 is IR sees white or any sufficiently light color
//  Black magic don't touch
pins.setPull(DigitalPin.P20, PinPullMode.PullUp)
//  MODIFIES: NONE
//  MODIFIES: adjusting, turn_direction
//  MODIFIES: ir1_read, ir2_read, force_read
function set_gb(dir1: number, spd1: number, dir2: number, spd2: number) {
    sensors.DDMmotor(gb1_direction, dir1, gb1_speed, spd1)
    sensors.DDMmotor(gb2_direction, dir2, gb2_speed, spd2)
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
let speed = 100
let speed_offset1 = 0
let speed_offset2 = 0
let turn_speed = 150
let turn_speed_offset1 = 0
let turn_speed_offset2 = 0
//  Flags (0 -> false, 1 -> true)
let active = 0
//  State (0 -> moving, 1 -> adjusting, 2 -> turning)
let state = 0
//  Array containing flags for each intersection passed
//  E.G. 
//  when passing the first intersection the first element will be set to one
//  when passing the second intersection the second element will be set to one
//  and so on
let intersections = [0, 0, 0, 0]
//  Run these functions in the background
basic.forever(function read_pins() {
    
    ir1_read = pins.digitalReadPin(ir1)
    ir2_read = pins.digitalReadPin(ir2)
    force_read = pins.digitalReadPin(force)
})
basic.forever(function move() {
    
    
    //  Only when moving
    if (state == 0) {
        set_gb(direction, speed, 1 - direction, speed)
    }
    
})
basic.forever(function adjust() {
    
    
    
    //  If not adjusting then don't do anything
    if (state != 1) {
        return
    } else if (ir1_read == (0 ^ ir2_read) && (0 ^ ir2_read) == 0) {
        //  If one of the sensors sense black
        //  If the left sensor doesn't sense black then turn right
        if (ir1_read == 1) {
            turn_direction = 0
        } else if (ir2_read == 1) {
            //  Otherwise turn left
            turn_direction = 1
        }
        
        set_gb(turn_direction, turn_speed, turn_direction, turn_speed)
    }
    
})
//  Main loop
while (true) {
    //  Once the button is pressed activate
    if (force_read == 0 && active == 0) {
        active = 1
    } else if (force_read == 0 && active == 1) {
        //  Reset
        active = 0
        intersections = [0, 0, 0, 0]
        state = 0
    }
    
    if (active) {
        //  At intersection
        if (ir1_read == 0 && ir2_read == 0) {
            
        } else if (ir1_read == (0 ^ ir2_read) && (0 ^ ir2_read) == 0) {
            //  Off course
            state = 1
        } else if (ir1_read == 1 && ir2_read == 1) {
            //  Otherwise by default move forward
            state = 0
        }
        
    }
    
}
