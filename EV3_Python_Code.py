# EV3 packages
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait
import _thread

# --- Initialize Brick and Motors ---
ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
claw_motor = Motor(Port.C)

# --- Initialize Sensors ---
us_left = UltrasonicSensor(Port.S1)
touch_right = TouchSensor(Port.S3)
color_sensor = ColorSensor(Port.S2)

# --- Motor Settings ---
forward_speed = 40
turn_speed = 20
manual_speed = 20
claw_speed = 15

# --- Ultrasonic Thresholds (in mm for MicroPython) ---
open_space_threshold = 700  # 70 cm
close_distance_threshold = 500  # 50 cm

# --- Manual Keys Dictionary ---
manual_keys = {
    'w': False, 'a': False, 's': False, 'd': False,
    'z': False, 'x': False
}

# --- Keyboard Input Thread ---
# Note: EV3 MicroPython doesn't support standard keyboard input
# This would need to be replaced with button controls or Bluetooth commands
# For now, this is a placeholder structure

def keyboard_thread():
    """
    Placeholder for keyboard/button input handling.
    In practice, you would use EV3 brick buttons or Bluetooth communication.
    Example: ev3.buttons.pressed() returns list of pressed buttons
    """
    while True:
        buttons = ev3.buttons.pressed()
        # Map EV3 buttons to manual keys if needed
        # Button.UP -> 'w', Button.DOWN -> 's', etc.
        wait(50)

# Start input thread (commented out since we can't use keyboard on EV3)
# _thread.start_new_thread(keyboard_thread, ())

ev3.speaker.beep()
print('🤖 Running robot...')

# --- Main Loop ---
try:
    while True:
        # Read color sensor
        color_check = color_sensor.color()
        
        # Manual mode (Blue, Green, Yellow)
        if color_check in [Color.BLUE, Color.GREEN, Color.YELLOW]:
            # Drive control
            if manual_keys['w']:
                left_motor.run(manual_speed * 10)  # MicroPython uses deg/s
                right_motor.run(manual_speed * 10)
            elif manual_keys['s']:
                left_motor.run(-manual_speed * 10)
                right_motor.run(-manual_speed * 10)
            elif manual_keys['a']:
                left_motor.run(-manual_speed * 10)
                right_motor.run(manual_speed * 10)
            elif manual_keys['d']:
                left_motor.run(manual_speed * 10)
                right_motor.run(-manual_speed * 10)
            else:
                left_motor.stop()
                right_motor.stop()
            
            # Claw control
            if manual_keys['z']:
                claw_motor.run(claw_speed * 10)
            elif manual_keys['x']:
                claw_motor.run(-claw_speed * 10)
            else:
                claw_motor.stop()
        
        else:
            # --- Autonomous Mode ---
            left_dist = us_left.distance()  # Returns distance in mm
            touch_pressed = touch_right.pressed()
            
            if touch_pressed:
                # Stop and back up
                left_motor.stop()
                right_motor.stop()
                wait(200)
                left_motor.run(-forward_speed * 10)
                right_motor.run(-forward_speed * 10)
                wait(1000)
                # Turn right
                left_motor.run(turn_speed * 10)
                right_motor.run(-turn_speed * 10)
                wait(1200)
                # Move forward
                left_motor.run(forward_speed * 10)
                right_motor.run(forward_speed * 10)
            
            elif left_dist > open_space_threshold:
                print('Open space detected on left! Turning left...')
                wait(700)
                left_motor.stop()
                right_motor.stop()
                wait(500)
                # Turn left
                left_motor.run((turn_speed - 20) * 10)
                right_motor.run((turn_speed + 20) * 10)
                wait(1500)
                # Move forward
                left_motor.run(forward_speed * 10)
                right_motor.run(forward_speed * 10)
                wait(2000)
            
            elif left_dist > close_distance_threshold:
                left_motor.run(forward_speed * 10)
                right_motor.run(forward_speed * 10)
                wait(500)
            
            else:
                # Slight right turn
                left_motor.run((forward_speed + 1) * 10)
                right_motor.run(forward_speed * 10)
        
        wait(50)

except KeyboardInterrupt:
    print('🛑 Stopping robot...')
    left_motor.stop()
    right_motor.stop()
    claw_motor.stop()
    ev3.speaker.beep()
