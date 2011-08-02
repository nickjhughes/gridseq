
""" Functions as a Ghetto VST by using GridSequencer to generate MIDI with
pyGame, which is routed with LoopBe to Ableton Live. """


from GridSequencer import GridSequencer, TextDisplay
from midiGenerator import midiGenerator
from time import sleep, clock


scale = ['C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4']

seq = GridSequencer(len(scale))
view = TextDisplay(seq)

seq.add([0,0], seq.RIGHT)
seq.add([0,2], seq.RIGHT)
seq.add([2,7], seq.UP)
seq.add([4,7], seq.UP)
seq.add([6,0], seq.DOWN)
seq.add([6,2], seq.DOWN)
seq.add([6,4], seq.DOWN)
seq.add([8,6], seq.LEFT)
seq.add([8,8], seq.LEFT)
bpm = 150

sleep_time = 1/((bpm*2)/60.0)

# MIDI device
port = None
for device in midiGenerator.get_devices():
    if device['name'] == 'LoopBe Internal MIDI' and device['output']:
        port = device['port']
        print 'Using %s device.' % device['name']
if port is None:
    print 'Fatal Error: Could not find LoopBe MIDI device.'
    exit()

midi = midiGenerator(port)

t = clock()

while True:
    
    print view
    
    # Sounds
    notes = [scale[i] for i in list(set(seq.hit_list))]
    midi.play_notes(notes, sleep_time/2)
    
    seq.hit_list = []
    seq.update()
    
    while clock() - t < sleep_time:
        pass
    t = clock()

midi.cleanup()
