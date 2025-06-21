import speech_recognition as sr
from cryptography.fernet import Fernet
import os

# File paths
KEY_FILE = "voice_secret.key"
DIARY_FILE = "voice_diary.encrypted"
PASSWORD = "open"  # Your spoken password

# Generate or load encryption key
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, 'rb') as f:
        return f.read()

# Encrypt and decrypt functions
def encrypt_data(text, key):
    return Fernet(key).encrypt(text.encode())

def decrypt_data(token, key):
    return Fernet(key).decrypt(token).decode()

# Voice recognition for password
def listen_for_password():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak your password...")
        audio = recognizer.listen(source)

    try:
        spoken = recognizer.recognize_google(audio)
        print(f"You said: {spoken}")
        return spoken.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError:
        print("Speech service unavailable.")
    return None

# Diary actions
def add_entry(key):
    entry = input("Write your diary entry:\n")
    encrypted = encrypt_data(entry, key)
    with open(DIARY_FILE, 'ab') as f:
        f.write(encrypted + b'\n')
    print("Entry securely added.")

def view_entries(key):
    if not os.path.exists(DIARY_FILE):
        print("No diary entries found.")
        return
    with open(DIARY_FILE, 'rb') as f:
        for line in f:
            try:
                print("📝", decrypt_data(line.strip(), key))
            except:
                print("❌ Could not decrypt entry.")

# Main function
def main():
    spoken_password = listen_for_password()
    if spoken_password != PASSWORD:
        print("❌ Access Denied.")
        return

    key = load_key()
    print("\n🔐 Welcome to your Encrypted Voice Diary")
    print("1. View Entries")
    print("2. Add Entry")
    choice = input("Choose an option: ")

    if choice == '1':
        view_entries(key)
    elif choice == '2':
        add_entry(key)
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()