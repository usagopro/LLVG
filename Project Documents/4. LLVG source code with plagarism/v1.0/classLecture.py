import speech_recognition as sr

lecture = []
recognized = ''
listening = False
recognizer = None
stop_listening = None


def callback(recognizer, source):

    try:
        global recognized
        recognized = recognizer.recognize_google(source)
        global lecture
        lecture.append(recognized)
        print("you said ", lecture)

    except sr.RequestError as exc:
        print(exc)

    except sr.UnknownValueError:
        print("unable to recognize")


def toggle_listening(txt_field, mic_label):
    global listening
    global recognizer
    global stop_listening

    if listening:
        mic_label.config(bg='#0066CC')
        txt_field.config(state='normal')
        stop_listening()  # Stop the listening loop
        listening = False
        print("Microphone listening stopped")
    else:
        mic_label.config(bg='#4B0082')
        txt_field.config(state='disabled')
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.1)
        print('Talk')
        stop_listening = recognizer.listen_in_background(mic, callback)
        listening = True
        print("Microphone listening started")


def reset_lecture():
    global lecture
    lecture = []
