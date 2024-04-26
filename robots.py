import RPi.GPIO as GPIO
import time
import socket

def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.setup(ldr_pin, GPIO.IN)
    GPIO.setup(trigger_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

ENA = 17
IN1 = 27
IN2 = 22
ENB = 18
IN3 = 23
IN4 = 24
ldr_pin = 5
trigger_pin = 6
echo_pin = 13
light_threshold = 700
sonar_threshold = 200

setup_gpio()

pwm_a = GPIO.PWM(ENA, 100)
pwm_b = GPIO.PWM(ENB, 100)
pwm_a.start(0)
pwm_b.start(0)

def drive_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(100)
    pwm_b.ChangeDutyCycle(100)

def stop():
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

def main():
    setup_gpio()
    host = ''
    port = 48151
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(1)
        print("Waiting for a connection...")
        connection, client_address = sock.accept()
        with connection:
            print(f"Connected to {client_address}")
            while True:
                data = connection.recv(1024).decode('utf-8')
                print("Received command:", data)
                if data == 'avance':
                    drive_forward()
                elif data == 'recule':
                    drive_backward()
                elif data == 'arrete':
                    stop()
                if not data:
                    break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop()
        print("Arrêt du robot")
    finally:
        pwm_a.stop()
        pwm_b.stop()
        GPIO.cleanup()
        print("GPIO nettoyé")
