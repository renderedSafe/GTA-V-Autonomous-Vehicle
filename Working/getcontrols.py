import pygame


def get_controls(joystick):
    """
    :return: steering_angle, throttle --both rounded to 6 digits
    """

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            pass

    # both values get rounded to we keep things simpler
    steering_angle = round(joystick.get_axis(0), 6)
    #print(steering_angle)
    # reversing the sign of the throttle value because controller spits out -1 for full forward and 1 for full reverse
    throttle = -(round(joystick.get_axis(2), 6))

    return steering_angle, throttle

