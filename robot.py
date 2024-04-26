import RPi.GPIO as GPIO
import time
import speech_recognition as sr

# Définition des broches GPIO pour les moteurs
ENA = 17  # PWM pour la vitesse du moteur A
IN1 = 27  # Contrôle de direction du moteur A
IN2 = 22  # Contrôle de direction du moteur A
ENB = 18  # PWM pour la vitesse du moteur B
IN3 = 23  # Contrôle de direction du moteur B
IN4 = 24  # Contrôle de direction du moteur B

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

def drive_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.start(100)
    pwm_b.start(100)

def drive_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.start(100)
    pwm_b.start(100)

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.stop()
    pwm_b.stop()

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
                elif 'arrête-toi' in command:
                    stop()
                else:
                    print("Commande non reconnue")
            except sr.UnknownValueError:
                print("Je n'ai pas compris la commande.")
            except sr.RequestError:
                print("Erreur de service; vérifiez votre connexion Internet.")
except KeyboardInterrupt:
    pass

# Nettoyage des broches GPIO
GPIO.cleanup()
