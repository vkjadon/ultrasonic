import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def setup_pins(trigger_pin, echo_pin):
    GPIO.setup(trigger_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

def get_distance(trigger_pin, echo_pin):
    # Ensure trigger is low
    GPIO.output(trigger_pin, False)
    time.sleep(0.1)

    # Send a 10µs pulse to trigger the measurement
    GPIO.output(trigger_pin, True)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)

    # Measure the time it takes for the echo to be received
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    # Calculate distance based on the time and speed of sound
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound = 34300 cm/s, so distance = (time/2) * speed of sound
    distance = round(distance, 2)

    return distance

def cleanup():
    GPIO.cleanup()

def main():
    try:
        trigger_pin = 23  # Replace with your actual trigger pin
        echo_pin = 24     # Replace with your actual echo pin
        setup_pins(trigger_pin, echo_pin)

        while True:
            distance = get_distance(trigger_pin, echo_pin)
            print(f'Distance: {distance} cm')
            time.sleep(1)  # Wait for 1 second before measuring again

    except KeyboardInterrupt:
        print("Test interrupted by user. Exiting...")

    finally:
        cleanup()

if __name__ == "__main__":
    main()
