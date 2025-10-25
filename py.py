import os
from cerebras.cloud.sdk import Cerebras
import re
from datetime import datetime
import time

# Get API key from GitHub
API_KEY = os.getenv("CEREBRAS_API_KEY")
client = Cerebras(api_key=API_KEY)

USED_KEYWORDS_FILE = "used_keywords.txt"
OUTPUT_FOLDER = "_posts"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Your keyword list (keep all of them)
keywords = [
    "laptop won’t boot after update", "laptop screen stays black after logo", "laptop keeps crashing randomly", "laptop overheating in sleep mode", "laptop making buzzing sound", "laptop screen lines appearing", "laptop charging port loose", "laptop turns off without warning", "laptop stuck preparing automatic repair", "laptop battery not detected", "laptop fan running loud all the time", "laptop screen goes white", "laptop not connecting to bluetooth", "laptop not detecting mouse", "laptop takes forever to start", "laptop keeps shutting off when unplugged", "laptop freezes during gaming", "laptop won’t shut down completely", "laptop turns on but nothing on screen", "laptop battery percentage not accurate", "laptop keyboard repeating keys", "laptop screen brightness flickering", "laptop making beeping sound", "laptop screen blurry after sleep", "laptop power button not working", "laptop stuck on black screen with cursor", "laptop shows no boot device", "laptop not detecting ram", "laptop charging light blinking", "laptop plugged in but not charging windows 11", "laptop wifi keeps turning off", "laptop audio not syncing", "laptop microphone not detected", "laptop screen turns off but computer still on", "laptop overheating even on idle", "laptop fan not stopping", "laptop battery draining while charging", "laptop mouse pointer disappearing", "laptop lagging after login", "laptop slow to respond", "laptop freezes during video playback", "laptop usb device keeps disconnecting", "laptop can’t find wifi network", "laptop showing blue screen after update", "laptop not detecting external monitor hdmi", "laptop battery charging on and off", "laptop keyboard lights flashing", "laptop booting into bios every time", "laptop doesn’t detect ethernet cable", "laptop not reading sd card", "laptop stuck on diagnosing your pc", "laptop boots to recovery mode", "laptop overheating with charger plugged in", "laptop screen dimming automatically", "laptop cursor jumps around", "laptop display turns off randomly", "laptop won’t install windows update", "laptop won’t boot after bios update", "laptop stuck on restarting screen", "laptop won’t recognize second monitor", "laptop won’t detect wireless mouse", "laptop showing red light near charging port", "laptop won’t connect to mobile hotspot", "laptop fan making grinding noise", "laptop battery swelling symptoms", "laptop won’t enter bios", "laptop won’t boot from recovery usb", "laptop overheating while idle", "laptop not turning off completely", "laptop turns off after few minutes", "laptop keeps restarting after update", "laptop speaker crackling noise", "laptop no sound in headphones", "laptop showing battery not present", "laptop charging symbol not showing", "laptop screen backlight flashing", "laptop won’t detect usb drive", "laptop slow to charge battery", "laptop slow internet connection", "laptop wifi signal weak", "laptop shuts down at random times", "laptop mouse not moving but keyboard works", "laptop hard drive clicking", "laptop cpu usage 100 percent", "laptop overheating after windows update", "laptop freezes during zoom call", "laptop brightness not adjusting automatically", "laptop no display but power light on", "laptop battery discharging fast", "laptop won’t sleep when lid closed", "laptop trackpad lagging", "laptop makes popping sound", "laptop screen color distortion", "laptop touchpad right click not working", "laptop fan keeps revving up", "laptop turns off when battery low", "laptop turns on then off immediately", "laptop keeps asking for repair", "laptop freezes while watching youtube", "laptop cursor moving by itself", "laptop no power light", "laptop screen showing rainbow colors", "laptop not connecting to ethernet", "laptop mouse double clicking issue", "laptop brightness control not working", "laptop keyboard backlight turning off", "laptop overheats while charging overnight", "laptop slow after windows reset", "laptop hangs when opening chrome", "laptop not recognizing usb c hub", "laptop wifi adapter missing", "laptop external keyboard not detected", "laptop stuck in sleep mode", "laptop won’t wake from black screen", "laptop fan not turning on", "laptop not showing battery percentage", "laptop runs hot after bios update", "laptop performance drops when charging", "laptop battery percentage stuck", "laptop sound distortion problem", "laptop mic volume too low", "laptop no sound from speakers", "laptop battery blinking orange light", "laptop plugged in not charging dell", "laptop freezes when unplugged", "laptop won’t boot safe mode", "laptop turns off during update", "laptop power light blinking no display", "laptop fan starts then stops", "laptop usb ports short circuit", "laptop overheating after cleaning fan", "laptop stuck in windows logo", "laptop restarts during sleep mode", "laptop lagging during zoom meetings", "laptop keeps crashing after update", "laptop won’t connect to office wifi", "laptop fan noise after startup", "laptop showing critical battery error", "laptop not saving battery settings", "laptop flickering when brightness low", "laptop turns off when charger unplugged", "laptop freezes during file transfer", "laptop shows charging but not increasing", "laptop slow after installing update", "laptop overheating when playing video", "laptop taking too long to boot", "laptop screen resolution problem", "laptop cursor freezing after sleep", "laptop usb ports not detecting mouse", "laptop blue screen memory management", "laptop not connecting to tv via hdmi", "laptop overheating with cooling pad", "laptop shuts down when opening game", "laptop not charging to full capacity", "laptop power button blinking", "laptop no display after sleep", "laptop black screen with fan spinning", "laptop takes long time to shut down", "laptop screen turns pink", "laptop touchpad scroll not working", "laptop stuck in reboot loop", "laptop showing disk error", "laptop external mic not working", "laptop slow wifi connection fix", "laptop screen brightness locked", "laptop screen goes dark randomly", "laptop overheating even on standby", "laptop speaker not producing sound", "laptop keyboard keys sticking", "laptop makes high pitched noise", "laptop screen flickers when moving lid", "laptop overheating while charging fix", "laptop brightness too low", "laptop screen flashing white", "laptop won’t connect to home wifi", "laptop keeps logging off", "laptop showing battery error", "laptop booting into repair mode", "laptop brightness changes automatically", "laptop overheating due to dust", "laptop keeps restarting at login screen", "laptop mouse pointer missing", "laptop touchpad sensitivity issue", "laptop won’t recognize charger", "laptop won’t update drivers", "laptop overheating in bag", "laptop shuts off without warning", "laptop screen ghosting issue", "laptop wifi not turning on windows 11", "laptop booting very slowly", "laptop overheating with lid closed", "laptop screen goes black intermittently", "laptop audio cutting out", "laptop usb not transferring data", "laptop lagging when watching videos", "laptop hangs when copying files", "laptop battery drains when off", "laptop external display flickering", "laptop overheating when multitasking", "laptop screen shows artifacts", "laptop trackpad clicking sound", "laptop fans spin but no display", "laptop taking long time to charge", "laptop overheating while browsing", "laptop keyboard not detected in bios", "laptop sleep not working after update", "laptop battery percentage jumping", "laptop cursor shaking", "laptop screen tearing issue"
]

def load_used_keywords():
    used = set()
    if os.path.exists(USED_KEYWORDS_FILE):
        with open(USED_KEYWORDS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                used.add(line.strip())
    return used

def save_used_keyword(keyword):
    with open(USED_KEYWORDS_FILE, 'a', encoding='utf-8') as f:
        f.write(keyword + '\n')

def generate_blog_post(keyword):
    print(f"Generating: {keyword}")
    try:
        stream = client.chat.completions.create(
            messages=[{"role": "system", "content": f"Write a friendly, helpful blog post about '{keyword}'. 800-1200 words. Use stories, tips, active voice."}],
            model="llama3.1-8b",
            stream=True,
            max_completion_tokens=4000,
            temperature=0.7
        )
        content = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content += chunk.choices[0].delta.content
        return content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return ""

def format_filename(keyword):
    clean = re.sub(r'[^\w\s-]', '', keyword).strip().lower()
    clean = re.sub(r'\s+', '-', clean)
    date = datetime.now().strftime('%Y-%m-%d')
    return f"{date}-{clean}.md"

def save_post(keyword, content):
    filename = format_filename(keyword)
    path = os.path.join(OUTPUT_FOLDER, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"---\ntitle: \"{keyword.title()}\"\n---\n\n{content}")
    print(f"Saved: {filename}")

def main():
    print("Starting Daily Generator...")
    used = load_used_keywords()
    start = time.time()
    max_time = 3600  # 1 hour

    for i, kw in enumerate(keywords, 1):
        if time.time() - start > max_time:
            print("1 hour limit reached.")
            break
        if kw in used:
            print(f"[{i}] SKIP: {kw}")
            continue

        print(f"[{i}] Making: {kw}")
        content = generate_blog_post(kw)
        if content and len(content) > 500:
            save_post(kw, content)
            save_used_keyword(kw)
            print("Done")
        else:
            print("Failed or too short")
        time.sleep(1)

if __name__ == "__main__":
    main()


