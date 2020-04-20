import simpleaudio as sa


filename = 'musicvideo.wav'
wave_obj = sa.WaveObject.from_wave_file(filename)
play_obj = wave_obj.play()
  # Wait until sound has finished playing
for i in range (100000):
    print(i)
play_obj.stop()