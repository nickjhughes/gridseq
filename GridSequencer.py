

class Matrix(object):
    
    """ A 2D matrix. """
    
    def __init__(self, size, value=None):
        """ Create a new matrix of the given size, filled with the given value.
        Size should be a pair. """
        
        self.height, self.width = size
        self.array = [[value for i in xrange(self.width)] for j in xrange(self.height)]
    
    def __getitem__(self, index):
        """ Return the specified element from the matrix. Index should be a
        pair. """
        
        return self.array[index[0]][index[1]]
    
    def __setitem__(self, index, value):
        """ Set the specified element in the matrix. Index should be a pair. """
        
        self.array[index[0]][index[1]] = value
    
    def __str__(self):
        return '\n'.join([' '.join([str(e) for e in r]) for r in self.array])


class GridSequencer(object):
    
    """ A grid generative sequencer. """
    
    EMPTY, UP, RIGHT, DOWN, LEFT = range(5)
    
    def __init__(self, size=9):
        """ Create a new Seq object, a square grid of side length size. """
        
        self.size = size
        self.grid = Matrix([size,size], self.EMPTY)
        self.hit_list = []
    
    def update(self):
        """ Update the positions of blocks in the grid. """
        
        copy = Matrix([self.size,self.size], self.EMPTY)
        for i in xrange(self.size):
            for j in xrange(self.size):
                block = self.grid[i,j]
                if block != self.EMPTY and isinstance(block, int):
                    # Move the single block
                    pos, value = self._move([i,j], block)
                    if type(copy[pos]) == list:
                        copy[pos].append(value)
                    elif type(copy[pos]) == int and copy[pos] != self.EMPTY:
                        copy[pos] = [copy[pos], value]
                    else:
                        copy[pos] = value
                elif isinstance(block, list):
                    # Move blocks on top of each other
                    for dir in block:
                        pos, value = self._move([i,j], dir)
                        if type(copy[pos]) == list:
                            copy[pos].append(value)
                        elif type(copy[pos]) == int and copy[pos] != self.EMPTY:
                            copy[pos] = [copy[pos], value]
                        else:
                            copy[pos] = value
        
        # Rotate collided blocks
        for i in xrange(self.size):
            for j in xrange(self.size):
                if isinstance(copy[i,j], list):
                    copy[i,j] = [self._rotate(dir, len(copy[i,j])-1) for dir in copy[i,j]]
        
        self.grid = copy
    
    def _rotate(self, direction, multiplier=1):
        """ Rotate the given direction clockwise 90 degrees, times the multipler
        parameter given (which is 1 by default), and return. """
        
        dir = direction + multiplier
        if dir >= 5:
            dir -= 4
        return dir
    
    def _move(self, position, direction, record=True):
        """ If the given block is in the given position, where should it go
        next? Return the position and direction as pair.
        
        Also adds to the hit_list, which records when and where blocks hit the
        walls. To avoid this behaviour, pass false as a third argument. """
        
        i, j = position
        
        if direction == self.UP:
            if i == 0:
                # Hit wall
                pos = [i+1,j]
                dir = self.DOWN
            elif self.grid[i-1,j] != self.EMPTY:
                # Hit block
                pos = [i,j]
                dir = self.DOWN
            else:
                pos = [i-1,j]
                dir = self.UP
        elif direction == self.DOWN:
            if i == self.size-1:
                # Hit wall
                pos = [i-1,j]
                dir = self.UP
            elif self.grid[i+1,j] != self.EMPTY:
                # Hit block
                pos = [i,j]
                dir = self.UP
            else:
                pos = [i+1,j]
                dir = self.DOWN
        elif direction == self.LEFT:
            if j == 0:
                # Hit wall
                pos = [i,j+1]
                dir = self.RIGHT
            elif self.grid[i,j-1] != self.EMPTY:
                # Hit block
                pos = [i,j]
                dir = self.RIGHT
            else:
                pos = [i,j-1]
                dir = self.LEFT
        elif direction == self.RIGHT:
            if j == self.size-1:
                # Hit wall
                pos = [i,j-1]
                dir = self.LEFT
            elif self.grid[i,j+1] != self.EMPTY:
                # Hit block
                pos = [i,j]
                dir = self.LEFT
            else:
                pos = [i,j+1]
                dir = self.RIGHT
        
        # Add to hit_list
        if record:
            p, q = pos
            if p == 0 and dir == self.UP:
                self.hit_list.append(q)
            elif p == self.size-1 and dir == self.DOWN:
                self.hit_list.append(q)
            elif q == 0 and dir == self.LEFT:
                self.hit_list.append(p)
            elif q == self.size-1 and dir == self.RIGHT:
                self.hit_list.append(p)
        
        return (pos, dir)
    
    def add(self, position, direction):
        """ Add a new block to the grid, in the given position and facing the
        given direction. Position should be a pair. Will silently fail if a
        block already exists in that position. """
        
        if self.grid[position] == self.EMPTY:
            self.grid[position] = direction
    
    def edit(self, position, direction):
        """ Change the direction of the block in the given position. Position
        should be a tuple. Will silently fail if no block exists in the given
        position. """
        
        if self.grid[position] != self.EMPTY:
            self.grid[position] = direction


class TextDisplay(object):
    
    """ An ASCII display of a GridSequencer object. """
    
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


if __name__ == '__main__':
    from time import sleep
    seq = GridSequencer()
    view = TextDisplay(seq)
    #seq.add([0,1], seq.DOWN)
    #seq.add([8,1], seq.UP)
    seq.add([1,8], seq.UP)
    seq.add([3,8], seq.UP)
    #seq.add([8,7], seq.UP)
    seq.add([5,8], seq.UP)
    seq.add([7,8], seq.UP)
    while True:
        sleep(0.5)
        print view
        print list(set(seq.hit_list))
        seq.hit_list = []
        seq.update()
