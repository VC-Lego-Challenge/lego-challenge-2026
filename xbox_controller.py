from pybricks.hubs import PrimeHub
from pybricks.iodevices import XboxController
from pybricks.parameters import Button, Direction, Port
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Set up all devices.
prime_hub = PrimeHub()
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.A, Direction.CLOCKWISE)
drive_base = DriveBase(left_motor, right_motor, 56, 114)  # wheel_diameter, axle_track (mm)
attachment_c = Motor(Port.C, Direction.CLOCKWISE)
attachment_e = Motor(Port.E, Direction.CLOCKWISE)
light_sensor = ColorSensor(Port.D)

# Pairs with the first available Xbox controller. Put the controller in
# pairing mode (press and hold the connect button) if this doesn't connect.
xbox = XboxController()

MAX_SPEED = 500  # mm/s
MAX_TURN_RATE = 200  # deg/s
ATTACHMENT_DC = 70  # percent

# Flip to True if forward on the left stick drives the robot backward.
INVERT_DRIVE = True


def main():
    print('Xbox controller connected:', xbox.name())

    while True:
        pressed = xbox.buttons.pressed()

        # Left stick drives, right stick turns.
        _, left_y = xbox.joystick_left()
        right_x, _ = xbox.joystick_right()
        if INVERT_DRIVE:
            left_y = -left_y
        drive_base.drive(left_y / 100 * MAX_SPEED, right_x / 100 * MAX_TURN_RATE)

        # Triggers (pressure sensitive) run the attachment motor on Port C.
        left_trigger, right_trigger = xbox.triggers()
        attachment_c.dc((right_trigger - left_trigger) / 100 * ATTACHMENT_DC)

        # Bumpers (LB/RB, above the triggers) run the attachment motor on Port E.
        if Button.RB in pressed:
            attachment_e.dc(ATTACHMENT_DC)
        elif Button.LB in pressed:
            attachment_e.dc(-ATTACHMENT_DC)
        else:
            attachment_e.stop()

        # Show the detected color on the hub's RGB status light.
        prime_hub.light.on(light_sensor.color())

        # A reports the light sensor reading.
        if Button.A in pressed:
            print('light:', light_sensor.ambient())

        wait(20)


try:
    main()
finally:
    drive_base.stop()
    attachment_c.stop()
    attachment_e.stop()