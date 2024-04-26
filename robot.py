import RPi.GPIO as GPIO
import time
import socket
import speech_recognition as sr

# Définition des broches GPIO
ENA = 17  # PWM pour la vitesse du moteur A
IN1 = 27  # Contrôle de direction du moteur A
IN2 = 22  # Contrôle de direction du moteur A (utiliser pour reculer)
ENB = 18  # PWM pour la vitesse du moteur B
IN3 = 23  # Contrôle de direction du moteur B
IN4 = 24  # Contrôle de direction du moteur B (utiliser pour reculer)

# Configuration des broches GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

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

def drive_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(100)
    pwm_b.ChangeDutyCycle(100)

def stop():
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

# Initialiser le recognizer
recognizer = sr.Recognizer()
microphone = sr.Microphone()

try:
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("En attente de commandes vocales...")
        while True:
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio, language='fr-FR').lower()
                print("Commande reçue:", command)
                
                if 'avance' in command:
                    drive_forward()
                elif 'recule' in command:
                    drive_backward()
                elif 'arrête' in command:
                    stop()
                else:
                    print("Commande non reconnue")
            except sr.UnknownValueError:
                print("Je n'ai pas compris la commande.")
            except sr.RequestError:
                print("Erreur de service; vérifiez votre connexion Internet.")
except KeyboardInterrupt:
    print("Arrêt du programme")
finally:
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    print("GPIO nettoyé")
