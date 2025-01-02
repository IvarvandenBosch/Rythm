import os
import librosa
import pygame
import soundfile as sf

class MusicPlayer:
    def __init__(self):
      self.source = None
      self.bpm = 120
      self.tempo = 120
      self.beat_times = []
      self.x = None
      self.sr = None

    def loadSong(self, path):
      self.source = path
      self.bpm = bpmArray.get(path, 120)
      self.x, self.sr = librosa.load(path)
      self.tempo, self.beat_times = librosa.beat.beat_track(y=self.x, sr=self.sr, start_bpm=self.bpm, units='time')

    def updateBpm(self, new_bpm):
      self.tempo, self.beat_times = librosa.beat.beat_track(y=self.x, sr=self.sr, start_bpm=new_bpm, units='time')

    def change_playback_bpm(self, target_bpm):
      stretch_factor = target_bpm / self.tempo
      stretched_audio = librosa.effects.time_stretch(self.x, rate=stretch_factor)
      sf.write('temp_audio.wav', stretched_audio, self.sr)
      pygame.mixer.music.load('temp_audio.wav')
      pygame.mixer.music.play(0)

    def playMusic(self):
      pygame.mixer.music.load(self.source)
      pygame.mixer.music.set_volume(0.4)
      pygame.mixer.music.play(0)

    def pauseMusic(self):
      pygame.mixer.music.pause()

    def resumeMusic(self):
      pygame.mixer.music.unpause()

pygame.mixer.init()

bpmArray = {
    'nummers/notlikeus.mp3': 101,
    'nummers/uptowngirl.mp3': 129,
    'nummers/doemaar.mp3': 133,
    'nummers/tsugaru-burst.mp3': 172,
    'nummers/endofcentury.mp3': 175,
}

player = MusicPlayer()
player.loadSong('nummers/notlikeus.mp3')
