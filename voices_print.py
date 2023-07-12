import pyttsx3

# Initialize the Text-to-Speech engine
engine = pyttsx3.init()

# Retrieve the available voices
voices = engine.getProperty('voices')

# Print voice names and IDs
for voice in voices:
    print("Voice Name:", voice.name)
    print(" - ID:", voice.id)
    print()
