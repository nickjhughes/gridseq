
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