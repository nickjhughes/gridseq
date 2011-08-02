
from time import sleep
import pygame
import pygame.midi
from pygame.locals import *

pygame.midi.init()

class midiGenerator(object):
    
    """ Generates MIDI signals. """
    
    def __init__(self, device_id=None, instrument=0):
        """ Initialise pyGame and MIDI and such. """
        
        if device_id is None:
            port = pygame.midi.get_default_output_id()
        else:
            port = device_id
        
        self.midi_out = pygame.midi.Output(port, 0)
        self.midi_out.set_instrument(instrument)
    
    def _convert_note(self, note):
        """ Convert the given note, a string like 'C4' or 'Ab2' into its
        corresponding MIDI number. """
        
        letters = {'C':0, 'D':2, 'E':4, 'F':5, 'G':7, 'A':9, 'B':11,
                   'C#':1, 'Db':1, 'D#':3, 'Eb':3, 'F#':6, 'Gb':6,
                   'G#':8, 'Ab':8, 'G#':10, 'Bb':10}
        
        if len(note) == 2:
            letter, octave = note
        else:
            letter, accidental, octave = note
            letter = letter + accidental
        return 12*(int(octave)+1) + letters[letter]
    
    def play_notes(self, notes, duration):
        """ Play the given notes for the given duration. notes should be a
        list. """
        
        for note in notes:
            self.midi_out.note_on(self._convert_note(note), 100)
        sleep(duration)
        for note in notes:
            self.midi_out.note_off(self._convert_note(note))
    
    def cleanup(self):
        """ Clean up. """
        
        del self.midi_out
        pygame.midi.quit()
    
    @staticmethod
    def get_devices():
        """ Return a list of MIDI devices. """
        
        devices = []
        for i in range(pygame.midi.get_count()):
            interface, name, input, output, opened = pygame.midi.get_device_info(i)
            devices.append({'port': i, 'interface': interface, 'name': name,
                            'input': input, 'output': output, 'opened': opened})
        return devices
    
    @staticmethod
    def print_device_info():
        """ Print MIDI device info. """
        
        for i in range(pygame.midi.get_count()):
            r = pygame.midi.get_device_info(i)
            interf, name, input, output, opened = r
            in_out = ""
            if input:
                in_out = "(input)"
            if output:
                in_out = "(output)"
            print ("%2i: Interface %s, Name %s, Opened %s, %s" %
                   (i, interf, name, opened, in_out))

