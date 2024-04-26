import RPi.GPIO as GPIO
import time
import socket

# Configuration initiale des GPIO
def setup_gpio():
    GPIO.setwarnings(False)  # Désactive les avertissements
    GPIO.cleanup()  # Nettoie les configurations précédentes des GPIO
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

# Définition des broches GPIO
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

# Gestion du nettoyage des GPIO
try:
    # Placez ici votre boucle ou logique principale
    pass
finally:
    # Assurez-vous que le nettoyage est fait correctement à la fin
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()

# Votre code serveur ou autres fonctions ici
