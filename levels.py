import librosa
import pygame

source = 'nummers/apt.mp3'
bpmArray = {'nummers/notlikeus.mp3': 101, 'nummers/apt.mp3': 149, 'nummers/prayer.mp3': 123, 'nummers/testSong.mp3': 97,'nummers/100bpm.mp3': 100}
bpm = bpmArray[source]





x, sr = librosa.load(source)

tempo, beat_times = librosa.beat.beat_track(y=x, sr=sr, start_bpm=bpm, units='time')

def playMusic() :
  bpm = bpmArray[source]
  pygame.mixer.music.load(source)
  pygame.mixer.music.set_volume(0.4)
  pygame.mixer.music.play(0) 

def pauseMusic():
  pygame.mixer.music.pause()

def resumeMusic():
  pygame.mixer.music.unpause()