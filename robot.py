import RPi.GPIO as GPIO
import time
import socket

# Définition des broches GPIO
ENA = 17  # PWM pour la vitesse du moteur A
IN1 = 27  # Contrôle de direction du moteur A
IN2 = 22  # Contrôle de direction du moteur A
ENB = 18  # PWM pour la vitesse du moteur B
IN3 = 23  # Contrôle de direction du moteur B
IN4 = 24  # Contrôle de direction du moteur B
ldr_pin = 5
trigger_pin = 6
echo_pin = 13
light_threshold = 700
sonar_threshold = 200

# Configuration des broches GPIO
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

# Initialisation des PWM pour le contrôle de vitesse
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

def sonar_ping():
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)
    start_time = time.time()
    while GPIO.input(echo_pin) == 0:
        start_time = time.time()
    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # vitesse du son en cm/s
    return distance

# Socket setup
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(('10.38.165.207', 12345))
serveur.listen(5)

print("En attente de connexions...")
client, adresse = serveur.accept()
print(f"Connexion établie avec {adresse}")

try:
    while True:
        try:
            commande = client.recv(1024).decode()
            if not commande:
                break  # Break if client disconnects
            print("Commande reçue:", commande)
            
            if commande == "avancer":
                drive_forward()
            elif commande == "arrêter":
                stop()
            else:
                print("Commande non reconnue")

            ldr_reading = GPIO.input(ldr_pin)
            sonar_distance = sonar_ping()

            print("LDR Reading:", ldr_reading)
            print("Distance Reading:", sonar_distance)

            if ldr_reading < light_threshold:
                stop()
                print("Lights are off")
                break

            if sonar_distance < sonar_threshold:
                stop()
                print("Obstacle detected!")
                # Insert turn around logic here if necessary

        except socket.error as e:
            print("Socket error:", e)
            break
except KeyboardInterrupt:
    print("Program interrupted")

finally:
    print("Cleaning up GPIO and closing socket")
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    client.close()
    serveur.close()
import RPi.GPIO as GPIO
import time
import socket

# Définition des broches GPIO
ENA = 17  # PWM pour la vitesse du moteur A
IN1 = 27  # Contrôle de direction du moteur A
IN2 = 22  # Contrôle de direction du moteur A
ENB = 18  # PWM pour la vitesse du moteur B
IN3 = 23  # Contrôle de direction du moteur B
IN4 = 24  # Contrôle de direction du moteur B
ldr_pin = 5
trigger_pin = 6
echo_pin = 13
light_threshold = 700
sonar_threshold = 200

# Configuration des broches GPIO
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

# Initialisation des PWM pour le contrôle de vitesse
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

def sonar_ping():
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)
    start_time = time.time()
    while GPIO.input(echo_pin) == 0:
        start_time = time.time()
    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # vitesse du son en cm/s
    return distance

# Socket setup
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(('10.38.165.207', 12345))
serveur.listen(5)

print("En attente de connexions...")
client, adresse = serveur.accept()
print(f"Connexion établie avec {adresse}")

try:
    while True:
        try:
            commande = client.recv(1024).decode()
            if not commande:
                break  # Break if client disconnects
            print("Commande reçue:", commande)
            
            if commande == "avancer":
                drive_forward()
            elif commande == "arrêter":
                stop()
            else:
                print("Commande non reconnue")

            ldr_reading = GPIO.input(ldr_pin)
            sonar_distance = sonar_ping()

            print("LDR Reading:", ldr_reading)
            print("Distance Reading:", sonar_distance)

            if ldr_reading < light_threshold:
                stop()
                print("Lights are off")
                break

            if sonar_distance < sonar_threshold:
                stop()
                print("Obstacle detected!")
                # Insert turn around logic here if necessary

        except socket.error as e:
            print("Socket error:", e)
            break
except KeyboardInterrupt:
    print("Program interrupted")

finally:
    print("Cleaning up GPIO and closing socket")
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    client.close()
    serveur.close()
