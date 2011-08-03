
import colorama
from colorama import Fore, Back, Style

class Display(object):
    
    """ A terminal display for a GridSequencer object. """
    
    def __init__(self, seq, pos):
        """ Initialise the display. seq is a GridSequencer object, and pos
        should be a pair giving the terminal coordinates of the top-left of the
        sequencer grid. """
        
        self.seq = seq
        self.x0, self.y0 = pos
        self.pos_code = lambda x, y: '\x1b[%d;%dH' % (y, x)
        colorama.init()
        self.clear_screen()
        self.clear_grid()
    
    def clear_screen(self):
        """ Clear the display. """
        
        w, h = 90, 41
        
        for y in xrange(1,h):
            print '%s%s%s' % (Back.BLACK, self.pos_code(1,y), ' '*w),
    
    def clear_grid(self):
        """ Back to default white grid. """
        
        for y in xrange(self.y0,self.seq.size+self.y0):
            print '%s%s%s' % (Back.WHITE, self.pos_code(self.x0,y), ' '*self.seq.size),
        print '%s\n' % Back.BLACK
    
    def update(self):
        """ Update the display. """
        
        for j in xrange(self.seq.size):
            print '%s%s' % (self.pos_code(self.x0,self.y0+j), Back.WHITE)
            for i in xrange(self.seq.size):
                x = self.x0 + i
                y = self.y0 + j
                block = self.seq.grid[j,i]
                char = Back.WHITE
                if isinstance(block, int):
                    char += Fore.BLACK
                    if block == self.seq.UP:
                        char += '^'
                    elif block == self.seq.DOWN:
                        char += 'v'
                    elif block == self.seq.LEFT:
                        char += '<'
                    elif block == self.seq.RIGHT:
                        char += '>'
                    elif block == self.seq.EMPTY:
                        char = Back.WHITE + ' '
                elif isinstance(block, list):
                    char += Fore.RED + 'o'
                print '%s%s' % (self.pos_code(x,y), char),
            print '%s%s ' % (self.pos_code(x+1,y), Back.BLACK),


class TextDisplay(object):
    
    """ An basic ASCII display of a GridSequencer object. """
    
    def __init__(self, seq):
        self.seq = seq
    
    def __str__(self):
        string = '-' * (self.seq.size + 2) + '\n'
        for i in xrange(self.seq.size):
            string += '|'
            for j in xrange(self.seq.size):
                block = self.seq.grid[i,j]
                if type(block) == int:
                    if block == self.seq.EMPTY:
                        string += ' '
                    elif block == self.seq.UP:
                        string += '^'
                    elif block == self.seq.DOWN:
                        string += 'v'
                    elif block == self.seq.LEFT:
                        string += '<'
                    elif block == self.seq.RIGHT:
                        string += '>'
                elif type(block) == list:
                    string += 'o'
            string += '|\n'
        string += '-' * (self.seq.size + 2) + '\n'
        return string