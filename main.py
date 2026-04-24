from voice import take_command, speak, stop_speaking
from youtube_control import play_youtube
import threading
from gui import start_gui_thread
import gui
import webbrowser
import os
from gtts import gTTS
import pygame
import time
import pyautogui
import datetime
import json
import requests
import pygetwindow as gw
import psutil
import platform
import socket
import subprocess
import requests
#import os


pygame.mixer.init()

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False

# 🔊 SPEAK CONTROL
is_speaking = False
#is_playing_music = False  # Naya variable


def speak(text):
    global is_speaking
    try:
        print("nova:", text)

        tts = gTTS(text=text, lang='en')
        tts.save("voice.mp3")

        pygame.mixer.music.load("voice.mp3")
        pygame.mixer.music.play()

        is_speaking = True

        # 🔥 interruptable speaking
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            if not is_speaking:
                pygame.mixer.music.stop()
                break

        is_speaking = False
        pygame.mixer.music.unload()
        os.remove("voice.mp3")

    except:
        is_speaking = False


def stop_speaking():
    global is_speaking
    is_speaking = False
    pygame.mixer.music.stop()


# 🧠 MEMORY
def load_memory():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except:
        return {}


def save_memory(data):
    with open("memory.json", "w") as f:
        json.dump(data, f)


memory = load_memory()


# 🔁 SAFE INPUT
def get_input(prompt):
    for _ in range(3):
        speak(prompt)
        ans = take_command()

        if ans != "":
            return ans.lower()

        speak("I didn't catch that")

    return ""


# 🧠 ASK QUESTIONS
def ask_questions():
    global memory

    speak("I will ask you some questions")

    memory["name"] = get_input("What is your name?")
    memory["city"] = get_input("Which city do you live in?")
    memory["age"] = get_input("What is your age?")
    memory["color"] = get_input("What is your favorite color?")

    save_memory(memory)
    speak("Your information has been saved")


# 🤖 AI CHAT
def ai_chat(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        # ✅ SAFE HANDLE
        if isinstance(data, dict):
            return data.get("response", "No response")
        else:
            return str(data)

    except Exception as e:
        print("AI Error:", e)
        return "AI error"


# 😎 EMOTION
def detect_emotion(text):
    text = text.lower()

    if any(w in text for w in ["happy", "good", "great"]):
        return "happy"
    elif any(w in text for w in ["sad", "bad"]):
        return "sad"
    elif "angry" in text:
        return "angry"
    return "normal"


def emotional_reply(cmd, res):
    try:
        emo = detect_emotion(cmd)

        if emo == "happy":
            return "That's great! " + str(res)
        elif emo == "sad":
            return "I am here for you. " + str(res)
        elif emo == "angry":
            return "Stay calm. " + str(res)

        return str(res)
    except:
        return str(res)
    
#import psutil
import screen_brightness_control as sbc

def system_stats():
    try:
        battery = psutil.sensors_battery()
        percent = battery.percent
        plugged = "Plugged In" if battery.power_plugged else "Not Plugged In"
        report = f"Sir, your system has {percent} percent battery and it is currently {plugged}."
        speak(report)
    except Exception as e:
        speak("Sir, I am unable to access system statistics at the moment.")



# 🔥 SMART PC CONTROL (NEW ADD - NO REMOVAL)
def smart_pc_control(command):
    try:
        print("PC CONTROL:", command)

        command = command.lower()

        # WIFI
        if "wifi" in command:
            speak("Opening Wifi settings")
            os.system("start ms-settings:network-wifi")
            return True

        # SETTINGS
        if "settings" in command:
            speak("Opening settings")
            os.system("start ms-settings:")
            return True
        
        # 🖥️ MINIMIZE (PRO)
        if "minimize" in command or "minimise" in command:
            try:
                win = gw.getActiveWindow()
                if win:
                    win.minimize()
                    speak("Window minimized")
                return True
            except Exception as e:
                print("Minimize Error:", e)
                return True


        # 🖥️ MAXIMIZE (PRO)
        if "maximize" in command:
            try:
                win = gw.getActiveWindow()
                if win:
                    win.maximize()
                    speak("Window maximized")
                return True
            except Exception as e:
                print("Maximize Error:", e)
                return True
            
        # ❌ CLOSE WINDOW
        if "close" in command or "exit app" in command:
            speak("Closing window")
            pyautogui.hotkey("alt", "f4")
            return True

        # ❌ CLOSE SPECIFIC APP
        if "close" in command:

            if "chrome" in command:
                os.system("taskkill /f /im chrome.exe")
                speak("Closing Chrome")
                return True

            elif "notepad" in command:
                os.system("taskkill /f /im notepad.exe")
                speak("Closing Notepad")
                return True

            else:
                # fallback
                pyautogui.hotkey("alt", "f4")
                speak("Closing window")
                return True

        # 🖱️ MOUSE CONTROL (FINAL FIX)

        step = 200  # speed adjust kar sakta hai

        # 👉 MOVE (no need "mouse" word)
        if "move" in command or "cursor" in command:

            if "left" in command:
                pyautogui.moveRel(-step, 0, duration=0.2)
                speak("Moving left")
                return True

            elif "right" in command:
                pyautogui.moveRel(step, 0, duration=0.2)
                speak("Moving right")
                return True

            elif "up" in command:
                pyautogui.moveRel(0, -step, duration=0.2)
                speak("Moving up")
                return True

            elif "down" in command:
                pyautogui.moveRel(0, step, duration=0.2)
                speak("Moving down")
                return True
            
        # 🔋 BATTERY STATUS
        if "battery" in command or "system status" in command:
            system_stats()
            return True

        # ☀️ BRIGHTNESS CONTROL
        if "brightness" in command:
            if "increase" in command or "up" in command:
                curr = sbc.get_brightness()[0]
                sbc.set_brightness(min(100, curr + 20))
                speak("Brightness increased")
            elif "decrease" in command or "down" in command:
                curr = sbc.get_brightness()[0]
                sbc.set_brightness(max(0, curr - 20))
                speak("Brightness decreased")
            return True

        # 📸 SCREENSHOT
        if "screenshot" in command:
            speak("Taking screenshot, sir")
            ss = pyautogui.screenshot()
            name = f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"
            ss.save(name)
            speak(f"Screenshot saved as {name}")
            return True

        # 🔍 SEARCH ON YOUTUBE DIRECTLY
        if "search on youtube" in command:
            topic = command.replace("search on youtube", "").strip()
            speak(f"Searching for {topic} on YouTube")
            webbrowser.open(f"https://www.youtube.com/results?search_query={topic}")
            return True

        # 👉 CLICK
        if "click" in command:

            if "right" in command:
                pyautogui.rightClick()
                speak("Right click")
                return True

            elif "double" in command:
                pyautogui.doubleClick()
                speak("Double click")
                return True

            else:
                pyautogui.click()
                speak("Click")
                return True


        # 👉 SCROLL
        if "scroll" in command:

            if "up" in command:
                pyautogui.scroll(300)
                speak("Scrolling up")
                return True

            elif "down" in command:
                pyautogui.scroll(-300)
                speak("Scrolling down")
                return True


        # ⌨️ TYPING AI (FAST & WITH ENTER)
        if command.startswith("type"):
            text = command.replace("type", "").strip()

            if text != "":
                if "enter" in text:
                    clean_text = text.replace("enter", "").strip()
                    pyautogui.write(clean_text, interval=0.01) # Speed fast kar di
                    pyautogui.press("enter")
                else:
                    pyautogui.write(text, interval=0.01)
                
                speak("Done") # Pehle type hoga, fir nova bolega
            return True


        # 🔥 DELETE / REMOVE TEXT (YAHAN ADD KARNA HAI)
        if "delete all" in command or "clear text" in command:
            pyautogui.hotkey("ctrl", "a")
            pyautogui.press("backspace")
            speak("Cleared text")
            return True

        if "delete word" in command:
            pyautogui.hotkey("ctrl", "backspace")
            speak("Deleted word")
            return True

        if "delete" in command or "backspace" in command:
            pyautogui.press("backspace")
            speak("Deleted")
            return True
        



        # ⌨️ SHORTCUTS
        if "select all" in command:
            pyautogui.hotkey("ctrl", "a")
            speak("Selected all")
            return True

        if "copy" in command:
            pyautogui.hotkey("ctrl", "c")
            speak("Copied")
            return True

        if "paste" in command:
            pyautogui.hotkey("ctrl", "v")
            speak("Pasted")
            return True
        

        return False

    except Exception as e:
        print("PC CONTROL ERROR:", e)
        return False

# 🤖 MAIN LOOP
def run_nova():

    global memory
    nova_active = False
    permission_taken = False
    talk_mode = False

    while True:
        try:
            # 🔹 WAKE MODE
            if not nova_active:
                command = take_command()

                if command == "":
                    continue

                if "nova" in command:
                    nova_active = True
                    speak("Hello, I am nova. How can I help you?")

                    if not permission_taken:
                        permission_taken = True   # 🔥 FIX

                        speak("Can I ask you some personal questions? Say yes or no")
                        reply = take_command()

                        if "yes" in reply:
                            ask_questions()
                        else:
                            speak("Okay, I will not ask now. You can say ask some questions later")
                continue

            # 🔹 ACTIVE MODE
            command = take_command().lower()

            # 🔥 BICH MEIN ROKNE KA COMMAND
            

        # 🔥 INSTANT INTERRUPT
            if "stop" in command or "chup" in command:
                stop_speaking()
                talk_mode = False
                speak("Okay, I am quiet now.")
                continue

            command = command.replace("nova", "").strip()

            if command == "":
                continue

            print("Command:", command)

            # 🛑 STOP SPEAKING
            if "stop talking" in command:
                talk_mode = False
                stop_speaking()
                speak("Talk mode stopped")
                continue
            elif  command == "stop":
                stop_speaking()
                speak("Stopped")
                continue

            # ❌ EXIT
            elif "exit" in command or "goodbye" in command:
                speak("Goodbye sir, have a nice day!")
                #import os
                # Yeh poore process ko (GUI + Voice) turant kill kar dega
                os._exit(0)

            # 3. NETWORKING FEATURE: IP Scanner
            elif "scan network" in command or "network scan" in command:
                speak("Scanning local network for active devices, sir.")
                try:
                    # ARP command se active devices ki list milti hai
                    output = subprocess.check_output("arp -a", shell=True).decode()
                    print(output)
                    speak("Network scan complete. Active IP addresses are displayed on your terminal.")
                except:
                    speak("I encountered an error while scanning the network.")

            # 4. CYBER FEATURE: WiFi Password Recovery
            elif "show wifi" in command or "wi-fi passwords" in command:
                speak("Fetching saved Wi-Fi profiles and passwords.")
                try:
                    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
                    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
                    for name in profiles:
                        results = subprocess.check_output(['netsh', 'wlan', 'profile', name, 'key=clear']).decode('utf-8').split('\n')
                        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                        print(f"WiFi: {name} | Password: {results[0] if results else 'No Password'}")
                    speak("I have listed all saved passwords for you.")
                except:
                    speak("Security protocols restricted my access to WiFi profiles.")

            # 5. CYBER FEATURE: Website Security Check
            elif "check security of" in command:
                domain = command.replace("check security of", "").strip()
                if domain:
                    speak(f"Analyzing security headers for {domain}")
                    try:
                        url = f"https://{domain}" if not domain.startswith("http") else domain
                        res = requests.get(url, timeout=5)
                        speak(f"Website is active. Status code is {res.status_code}.")
                    except:
                        speak("Could not establish a secure connection with the domain.")

            # 6. SYSTEM HEALTH (M.Sc IT standard)
            elif "system status" in command or "health" in command:
                cpu = psutil.cpu_percent()
                ram = psutil.virtual_memory().percent
                speak(f"Sir, CPU usage is at {cpu} percent and RAM is at {ram} percent.")

            # 💤 SLEEP
            elif "sleep" in command:
                speak("Going to sleep")
                nova_active = False
                continue

            # 💬 TALK MODE
            elif "need some talk" in command:
                talk_mode = True
                speak("Sure, let's talk. Say stop talking to exit")

            elif "stop talking" in command or "stop talk" in command:
                talk_mode = False
                stop_speaking()
                speak("Talk mode stopped")

            # ... (need some talk wala logic yahan hai)

            # 💬 3rd POINT: BASIC TALK FIX (Instant Replies)
            elif "hello" in command:
                speak("Hello Arpit! How can I help you?")
                continue

            elif "how are you" in command or "how r u" in command:
                speak("I am doing great, sir! Thank you for asking. How are you?")
                continue
            
            elif "who are you" in command:
                speak("I am nova, your personal AI assistant, ready to help you with your tasks.")
                continue

            # ... (Iske niche PC Control aur baki logic rehne de)

            #PC CONTROL 
            elif smart_pc_control(command):
                continue

            elif talk_mode:
                res = ai_chat(command)

                # 🔥 SAFE FIX
                if not isinstance(res, str):
                    res = str(res)

                final_res = emotional_reply(command, res)

                if not isinstance(final_res, str):
                    final_res = str(final_res)

                speak(final_res)
                continue

            # 🧠 MEMORY
            elif command.startswith("my name is"):
                memory["name"] = command.replace("my name is", "").strip()
                save_memory(memory)
                speak("Name saved")

            elif command.startswith("my city is"):
                memory["city"] = command.replace("my city is", "").strip()
                save_memory(memory)
                speak("City saved")

            elif command.startswith("my age is"):
                memory["age"] = command.replace("my age is", "").strip()
                save_memory(memory)
                speak("Age saved")

            elif "what is my name" in command:
                speak(memory.get("name", "unknown"))

            elif "what is my city" in command:
                speak(memory.get("city", "unknown"))

            # 🧠 ASK
            elif "ask some question" in command or "ask some questions" in command:
                ask_questions()

            # 🎯 TYPE + ENTER FIX
            elif command.startswith("type"):
                text = command.replace("type", "").strip()

                if "enter" in text:
                    pyautogui.press("enter")
                else:
                    pyautogui.write(text)

            elif "press enter" in command:
                pyautogui.press("enter")

            # 🖱️ CLICK
            elif "click" in command:
                pyautogui.click()

            # ⬇️ SCROLL
            elif "scroll down" in command:
                pyautogui.scroll(-500)

            elif "scroll up" in command:
                pyautogui.scroll(500)

            # 🔙 NAVIGATION
            elif "back" in command:
                pyautogui.hotkey("alt", "left")

            elif "forward" in command:
                pyautogui.hotkey("alt", "right")

            # 🔊 VOLUME CONTROL 🔥 NEW
            elif "volume up" in command:
                pyautogui.press("volumeup")
                speak("Volume increased")

            elif "volume down" in command:
                pyautogui.press("volumedown")
                speak("Volume decreased")

            elif "mute" in command:
                pyautogui.press("volumemute")
                speak("Muted")

            # 🎵 YOUTUBE (Advanced Control)
            # 🎵 YOUTUBE (Advanced Control)
            elif "play" in command:
                song = command.replace("play", "").strip()
                speak(f"Playing {song} on YouTube")
                
                # 1. Gaana alag thread mein shuru karo
                threading.Thread(target=play_youtube, args=(song,), daemon=True).start()
                
                # 2. Nova ko turant Sleep mode mein daal do
                # Isse Nova tab tak kuch nahi sunegi jab tak aap "Nova" nahi bolte
                nova_active = False 
                
                print("System: Nova is now in Sleep Mode to avoid music feedback.")
                continue

            # 💻 APPS
            elif "open notepad" in command:
                os.system("start notepad")

            elif "open calculator" in command:
                os.system("start calc")

            elif "open chrome" in command:
                os.system("start chrome")

            # 🚀 NEW: SYSTEM HEALTH CHECK (Yahan add karo)
            elif "system health" in command or "system status" in command:
            
                cpu_usage = psutil.cpu_percent()
                ram_usage = psutil.virtual_memory().percent
                
                status_msg = f"Sir, the system is stable. CPU usage is at {cpu_usage} percent, and RAM usage is at {ram_usage} percent."
                speak(status_msg)
                
                if cpu_usage > 80:
                    speak("Warning Sir, CPU usage is very high.")

            # 🔍 1. NETWORK SCANNER (Internship Based Feature)
            elif "scan network" in command or "check connected devices" in command:
                speak("Scanning the network, sir. Please wait.")
                # Basic IP discovery using ARP
                devices = os.popen("arp -a").read()
                # Sirf connected IP addresses nikalne ke liye filter
                print(devices) 
                speak("Sir, I have retrieved the list of devices currently on your network. You can check the details on the console.")

            # 🛠️ 2. SYSTEM DIAGNOSTIC (Heavy Report)
            elif "system diagnostic" in command or "run diagnostic" in command:
                speak("Running full system diagnostics.")
                
                # OS & Processor Info
                sys_info = platform.uname()
                processor = sys_info.processor
                os_name = sys_info.system + " " + sys_info.release
                
                # Battery & Storage
                battery = psutil.sensors_battery()
                battery_per = battery.percent if battery else "N/A"
                disk = psutil.disk_usage('/')
                disk_free = round(disk.free / (1024**3), 2)
                
                report = f"Diagnostic complete. You are running {os_name}. Pr ocessor is {processor}. "
                report += f"Battery is at {battery_per} percent, and you have {disk_free} GB free space on your main drive."
                
                speak(report)
                print(f"--- FULL DIAGNOSTIC REPORT ---\nOS: {os_name}\nRAM: {psutil.virtual_memory().percent}%\nDisk Free: {disk_free}GB")

            # 💬 BASIC TALK FIX
            elif "hello" in command:
                speak("Hello")

            elif "how are you" in command or "how r u" in command or "how r you" in command:
                speak("I am doing great")

            # ⏰ TIME
            elif "time" in command:
                speak(datetime.datetime.now().strftime("The time is %H:%M"))

            # SMART PC CONTROL CALL (NEW ADD)
            elif smart_pc_control(command):
                continue

            # 🌐 GOOGLE SAFE
            else:
                if len(command) > 3:
                    speak("Searching on Google")
                    webbrowser.open(f"https://www.google.com/search?q={command}")
                else:
                    speak("I did not understand")

        except Exception as e:
            print("Error:", e)
            continue

# run_nova() call karne se PEHLE ise likho
if __name__ == "__main__":
    # 1. Pehle GUI start hogi (Alag thread mein)
    start_gui_thread() 
    
    # 2. Phir Nova ka main loop shuru hoga
    print(">>> Nova is standby. Say 'Nova activate' to start.")
    run_nova()

threading.Thread(target=run_nova, daemon=True).start()
gui.root.withdraw()
gui.root.mainloop()