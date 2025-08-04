## IMPORT LIBRARIES ##

from moviepy import VideoFileClip
from pynput import keyboard
from pynput import mouse
import random
import winsound
import time
import os



## DECLARE VARIABLES ##

cooldown = 0
current_ability = 'NONE'
script_running = True
tick_start_time = 0
deltatime = 0
key_events = []
skip_listen = False
clip_path = r'D:/Replay Videos/Desktop/'
output_path = r'C:/Users/xela_/Desktop/SkinwalkerClips/'
clip_index = 0
sessionID = random.randint(100,999)


## KEY LISTENER ##

## MOUSE ##

def on_click(x, y, button, pressed):
    if pressed:
        if button == mouse.Button.left:
            key_events.append('Left_Button')
        if button == mouse.Button.right:
            key_events.append('Right_Button')

mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()

## KEYBOARD ##

key_controller = keyboard.Controller()

def on_press(key):
    if not skip_listen:
        try:
            key_events.append(key.char)
            print('Key {0} added to event list.'.format(key.char))
        except AttributeError:
            try:
                key_events.append(key)
                print('Special key {0} added to event list.'.format(key))
            except AttributeError as e:
                print(e)
                

def on_release(key):
    # if not skip_listen:
    #     if key == keyboard.Key.esc:
    #         # Stop listener
    #         return False
    pass

keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()



## SCRIPT FUNCTIONS ##

def set_tick_start_time():
    global tick_start_time
    tick_start_time = time.monotonic_ns() / 10**9

def get_delta_time():
    delta_time = time.monotonic_ns() / 10**9 - tick_start_time
    print('Tick Time:', delta_time)
    return delta_time

def print_keys():
    global key_events
    if key_events:
        print('Key Events:', key_events)
    else:
        print("Empty List")

def clear_keys():
    global key_events
    key_events = []

def is_listener_alive():
    if not keyboard_listener.is_alive() or not mouse_listener.is_alive:
        print('Listener not alive')
        winsound.PlaySound(r'C:\Users\xela_\Desktop\Desktop\PythonScripts\MageArena\ListenerFault.wav', winsound.SND_FILENAME)

def hotkey_activate(char):
    global skip_listen
    skip_listen = True
    key_controller.press(keyboard.Key.alt)
    key_controller.press(keyboard.Key.shift)
    key_controller.press(char)
    key_controller.release(char)
    key_controller.release(keyboard.Key.shift)
    key_controller.release(keyboard.Key.alt)
    skip_listen = False

def activate_main_ability(current_ability):
    match current_ability:
        case "FireBall":
            print('### Activated FireBall ###')
            hotkey_activate('y')
        case "Freeze":
            print('### Activated Freeze ###')
            hotkey_activate('u')
        case "WormHole":
            print('### Activated Main WormHole ###')
            hotkey_activate('i')
        case "MagicMissile":
            print('### Activated MagicMissile ###')
            hotkey_activate('p')
        case _:
            print("### No Ability Active ###")

def activate_secondary_ability(current_ability):
    match current_ability:
        case "WormHole":
            print('### Activated Secondary WormHole ###')
            hotkey_activate('o')
        case _:
            print("### No Ability Active ###")

def convert_mp4_to_wav(input_mp4_path, output_wav_path):
    try:
        video_clip = VideoFileClip(input_mp4_path)
        video_clip = video_clip.subclipped(video_clip.duration - 3, video_clip.duration)
        video_clip.audio.write_audiofile(output_wav_path, codec='pcm_s16le')
        video_clip.close()
        print(f"Successfully converted '{input_mp4_path}' to '{output_wav_path}'")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")



## MAIN SCRIPT LOOP ##

while script_running:
    is_listener_alive()
    set_tick_start_time()
    time.sleep(0.5)
    
    for key in key_events:

        if key == '1' or key == '!':
            current_ability = "FireBall"
        if key == '2' or key == '@':
            current_ability = "Freeze"
        if key == '3' or key == "#":
            current_ability = "WormHole"
        if key == '4' or key == '$':
            current_ability = "MagicMissile"
        if key == '5' or key == '%':
            current_ability = 'NONE'
        if key == '6' or key == '^':
            current_ability = 'NONE'
        if key == keyboard.Key.esc:
            current_ability = 'NONE'
        if key == 'Left_Button':
            if cooldown == 0:
                activate_main_ability(current_ability)
                cooldown += 1
            else:
                print('### COOLDOWN ACTIVE ###')
        if key == 'Right_Button':
            if cooldown == 0:
                activate_secondary_ability(current_ability)
                cooldown += 1
            else:
                print('### COOLDOWN ACTIVE ###')

    print('Current ability:', current_ability)
    cooldown  -= get_delta_time()
    if cooldown < 0:
        cooldown = 0
    print('Cooldown:', cooldown)
    print_keys()

    clip_names = os.listdir(clip_path)
    if len(clip_names):
        print('### Converting files ###')
        for clip in clip_names:
            full_clip_path = clip_path + clip
            convert_mp4_to_wav(full_clip_path, output_path + 'mimic' + str(clip_index) + '_' + str(sessionID) + '.wav')
            try:
                os.remove(full_clip_path)
            except Exception as e:
                print(f"An error occurred during deletion: {e}")
            clip_index += 1
    else:
        print('No files to convert.')

    print()
    clear_keys()