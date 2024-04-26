import RPi.GPIO as GPIO
import time
import socket

def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    # Setup GPIO pins as before
    # Initialize PWM as before

# Setup and loop as before

def main():
    setup_gpio()
    host = ''
    port = 12345
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
        # Cleanup GPIO as before
