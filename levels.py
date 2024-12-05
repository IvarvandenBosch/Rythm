import librosa
import pygame

source = 'nummers/apt.mp3'

x, sr = librosa.load(source)

tempo, beat_times = librosa.beat.beat_track(y=x, sr=sr, start_bpm=149, units='time')

def playMusic() :
  pygame.mixer.music.load(source)
  pygame.mixer.music.set_volume(0.7)
  pygame.mixer.music.play(-1) 
