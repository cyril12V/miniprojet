import socket
import speech_recognition as sr

def listen_for_commands():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for commands...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError:
        print("Could not request results; check your internet connection")
        return None

def send_command(command, host='10.38.165.207', port=48151):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(command.encode('utf-8'))
    except socket.error as e:
        print(f"Failed to connect to {host}:{port}, error: {e}")

if __name__ == "__main__":
    while True:
        command = listen_for_commands()
        if command:
            send_command(command)
