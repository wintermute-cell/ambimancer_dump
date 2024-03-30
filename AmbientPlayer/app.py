from flask import Flask, request
import json
import os
import pygame
import threading
import time
import random

import socket
app = Flask(__name__)

GUN_IP = os.environ['GUN_IP']
GUN_PORT = os.environ['GUN_PORT']
AMBIENCES_DIR = './ambiences/'

# GLOBALS
PygameMixer = pygame.mixer
PygameMixer.init()
Ambiences = []

class Sound:
    def __init__(self, name, source_type, source, volume, pause_ms, overlap_ms, meander):
        self.name = name
        self.source_type = source_type
        self.sources = source
        self.static_volume = volume
        self.dynamic_volume_mult = 1
        self.overlap_ms = overlap_ms
        self.pause_ms = pause_ms
        self.meander = meander
        self.is_playing = False
        self.active_channels = []

    def __str__(self) -> str:
        return f'Sound: \"{self.name}\" from {self.sources} at volume {self.static_volume}'

    def get_random_pause_ms(self):
        return random.randint(self.pause_ms[0], self.pause_ms[1])

    def loop(self):
        self.is_playing = True
        global PygameMixer
        sounds: list[PygameMixer.Sound] = []
        for source in self.sources:
            sounds.append(PygameMixer.Sound(source))
        channel_idx = 0
        while self.is_playing:
            sound = random.choice(sounds)
            c = PygameMixer.find_channel()
            channel_idx = ((channel_idx + 1) % 8) + 0
            if self.active_channels:
                c.set_volume(self.active_channels[-1].get_volume())
            c.play(sound)
            print(f'Playing {self.name} on channel {channel_idx}...')
            self.active_channels.append(c)
            still_active_channels = [channel for channel in self.active_channels if channel.get_busy()]
            self.active_channels = still_active_channels
            if self.overlap_ms > 0:
                slen = sound.get_length() - self.overlap_ms/1000
            else:
                slen = sound.get_length() + self.get_random_pause_ms()/1000
            time.sleep(slen)

    def set_static_volume(self, volume):
        self.static_volume = min(max(volume, 0), 1)
        for channel in self.active_channels:
            channel.set_volume(self.static_volume * self.dynamic_volume_mult)

    def set_dynamic_volume_mult(self, volume_mult):
        self.dynamic_volume_mult = volume_mult
        for channel in self.active_channels:
            channel.set_volume(self.static_volume * volume_mult)

    def play(self):
        t = threading.Thread(target=self.loop)
        t.daemon = True
        t.start()

    def stop(self):
        self.is_playing = False
        for c in self.active_channels:
            c.fadeout(1000)


class Options:
    def __init__(self, volume):
        self.volume = volume

    def __str__(self) -> str:
        return f'Options:\n\tVolume: {self.volume}'


class Ambience:
    def __init__(self, name: str, options: Options, sounds: list[Sound], file_path):
        self.name = name
        self.options = options
        self.sounds = sounds
        self.file_path = file_path

    def __str__(self) -> str:
        output: str = f'Ambience \"{self.name}\"\n{self.options}\nSounds:\n'
        for sound in self.sounds:
            output += f'\t{sound}\n'
        return output

    def meander_sounds(self, meander_mult):
        for sound in self.sounds:
            if sound.meander:
                sound.set_dynamic_volume_mult(meander_mult)

    def play(self):
        for sound in self.sounds:
            sound.play()

    def stop(self):
        for sound in self.sounds:
            sound.stop()


class AmbienceManager:
    def __init__(self):
        self.active_ambiences = []
        self.meander_mult = 1

        mt = threading.Thread(target=self.modulate_meander)
        mt.daemon = True
        mt.start()

    def add_ambience(self, ambience_name: str):
        global Ambiences
        for ambience in Ambiences:
            if ambience.name == ambience_name:
                self.active_ambiences.append(ambience)
                ambience.play()
                print(f'Playing {ambience.name}')
                return

    def remove_ambience(self, ambience_name: str):
        remaining_ambiences = []
        for ambience in self.active_ambiences:
            if ambience.name == ambience_name:
                ambience.stop()
                print(f'Stopping {ambience.name}')
            else:
                remaining_ambiences.append(ambience)
        self.active_ambiences = remaining_ambiences

    def modulate_meander(self):
        floor = 0.35
        is_rising = -1
        while True:
            if self.meander_mult <= floor:
                self.meander_mult = floor
                is_rising = 1
            elif self.meander_mult >= 1:
                self.meander_mult = 1
                is_rising = -1
            self.meander_mult += 0.01 * is_rising
            for ambience in self.active_ambiences:
                ambience.meander_sounds(self.meander_mult)
            time.sleep(0.8)


def load_single_ambience(path_to_amb_file: str) -> Ambience:
    ambience = None
    with open(path_to_amb_file) as f:
        json_data = json.load(f)
        options_data = json_data['options']
        sounds_data = json_data['sounds']
        options = Options(options_data['volume'])
        sounds: list[Sound] = []
        for sound_name, sound_data in sounds_data.items():
            sounds.append(Sound(
                sound_name,
                sound_data['source_type'],
                sound_data['sources'],
                sound_data['volume'],
                sound_data['pause_ms'],
                sound_data['overlap_ms'],
                sound_data['meander']
            ))
    ambience = Ambience(json_data['name'], options, sounds, path_to_amb_file)
    return ambience

def load_ambiences() -> list[Ambience]:
    ambiences: list[Ambience] = []
    for file in os.listdir(AMBIENCES_DIR):
        if file.endswith('.json'):
            ambience = load_single_ambience(AMBIENCES_DIR + file)
            ambiences.append(ambience)
    return ambiences


def init():
    global Ambiences
    Ambiences = load_ambiences()
    print('\n\nLoaded Ambiences:\n')
    for a in Ambiences:
        print(f'{a}\n')

hostname = socket.gethostname()
#IPAddr = socket.gethostbyname(hostname)

CurrentAmbienceManager = AmbienceManager()
init()

intro = '\n\n\n--------------------------------------\n'
intro += f'AmbientPlayer running on device {hostname}\n'
intro += f'Connect to the client at the address:\n {GUN_IP}:{GUN_PORT}\n'
print(intro)

# ------
# ROUTES
# ------
@app.route('/')
def health():
    return 'Alive!', 200


@app.route('/play')
def play():
    amb_name = request.args.get('name')
    if amb_name:
        CurrentAmbienceManager.add_ambience(amb_name)
        return '', 200
    else:
        return 'Invalid ambience name', 400


@app.route('/stop')
def stop():
    amb_name = request.args.get('name')
    if amb_name:
        CurrentAmbienceManager.remove_ambience(amb_name)
        return '', 200
    else:
        return 'Invalid ambience name', 400


@app.route('/stop_all')
def stop_all():
    return '', 200


@app.route('/get_all')
def get_all():
    return '', 200


@app.route('/get_playing')
def get_playing():
    return '', 200


@app.route('/reload')
def reload():
    amb_name = request.args.get('name')
    if amb_name:
        global Ambiences
        good_ambiences = []
        stale_ambience = None
        for ambience in Ambiences:
            if ambience.name == amb_name:
                stale_ambience = ambience    
            else:
                good_ambiences.append(ambience)
        if stale_ambience == None:
            return 'Invalid ambience name', 400
        fresh_ambience = load_single_ambience(stale_ambience.file_path)
        Ambiences = good_ambiences
        Ambiences.append(fresh_ambience)
        if stale_ambience in CurrentAmbienceManager.active_ambiences:
            CurrentAmbienceManager.remove_ambience(amb_name)
            CurrentAmbienceManager.add_ambience(amb_name)
        return '', 200
    else:
        return 'Invalid ambience name', 400
