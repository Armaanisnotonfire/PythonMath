''' Display the doc of all the defined classes
for i in [("\n".join(c)) for c in [[i for i in p.__doc__.split("\n")] for p in defined_class]]: print(i.encode('utf-8').decode('unicode-escape'))
'''

defined_class = [Matrix, Complex, Ratio] # Completed/functional classes
""" MATRIX CLASS"""
class Matrix():
    '''
    Class name : Matrix
    Class type : Math class
    Matrix implementation with methods :
        * initialisation
        * representation
        * addition
        * substraction
        * negation
        * multiplication
        * transmutation (__invert__)
        * contain (python "in" funtion)
        * setitem (via matrix[(i,j)]=value)
        * len (return a tuple (i,j))
    '''
    def __init__(self, component):
        assert type(component) is list, str(type(component))+" type isn't supported by <class 'Matrix'>, must be <class 'list'>"

        h = len(component)
        assert h>0, "Empty matrix"

        l = max([len(i) for i in component]) # Search the max row size
        assert l>0, "Empty matrix"

        for i in range(len(component)): # Look in the entire matrix
            component[i]=component[i]+[0]*(l-len(component[i])) # Add missing 0

        self.comp = component # Correctly shaped matrix (fill w missing 0)
        self.l = l # Usefull because its often called in the Matrix class
        self.h = h # Same

    def __repr__(self):
        return "\n".join(["\t".join([str(n) for n in i]) for i in self.comp])

    ## magic methods
    #  Main magic methods
    def __add__(self, other):
        assert self.h==other.h and self.l==other.l, "Size error"
        return Matrix([[self.comp[i][j]+other.comp[i][j] for j in range(self.l)] for i in range(self.h)])

    def __sub__(self, other):
        return self+(-other)

    def __neg__(self):
        return self.scal(-1)

    def __mul__(self, other):
        assert self.l==other.h and self.h==other.l, "Size error"
        return Matrix([[sum([self.comp[rowN][i]*other.comp[i][colN] for i in range(self.l)]) for colN in range(other.l)] for rowN in range(self.h)])
        '''
        The line above is a little bit too long so i split it here just for reader

        for rowN in range(self.h):
            for colN in range(other.l): #Change the name just for readability (cuz it's same as self.h)
                for i in range(self.l)  #or range(other.h)
                    self.comp[rowN][i]*other.comp[i][colN]
        '''

    def __invert__(self):
        return Matrix([[self.comp[j][i] for j in range(self.h)] for i in range(self.l)])

    # Additional methods
    transpose = __invert__ #Create an alias of ~self

    def __contains__(self, item):
        checklist = set()
        for i in self.comp:  # Create a set with one occurence of each item in the matrix
            checklist = checklist | set(i)
        return (item in checklist) #Check item is in the set (python know this)

    def __setitem__(self, key, value): #use to redifine a value
        assert type(key) is tuple and len(key)==2, "The key is badly set please use mat[(i,j)]"
        self.comp[key[0]][key[1]] = value
        return self
    set = __setitem__
    ## Other methods
    def len(self):
        return (self.h,self.l)

    def scal(self, scal):
        return Matrix([[scal*self.comp[i][j] for j in range(self.l)] for i in range(self.h)])
## Actually there are too many assertions here ! (do not see that py in Pyzo, it's ugly)

""" COMPLEX CLASS """
class Complex():
    '''
    Class name : Complex
    Class type : Math class
    Complex implementation with methods :
        * initialisation
        * representation
        * real part
        * imaginary part
        * negation
        * equality
        * addition
        * multiplication
        * division
    '''
    def __init__(self, real, imag):
        self.r = real
        self.i = imag

    def __repr__(self):
        if self.r == 0:
            return str(self.i) + 'i'
        else:
            if self.i==0:
                return str(self.r)
            else:
                return str(self.r) + '+' + str(self.i) + 'i'

    def real(self):return self.r
    def imag(self):return self.i

    def __neg__(self):
        return Complex(self.r, -self.i)

    def __eq__(self,other):
        return self.r == other.r and self.i == other.i

    def __add__(self, other):
        return Complex(self.r+other.r, self.i+other.i)

    def __mul__(self, other):
        return Complex(self.r*other.r - self.i*other.i, self.r*other.i + other.r*self.i)

    def __truediv__(self, other):
        return Complex((-other*self).real()/(-other*other).real(),(-other*self).imag()/(-other*other).real())

""" RATIONAL CLASS"""
class Ratio():
    '''
    Class name : Rational
    Class type : Math class
    Rational implementation with methods :
        * initialisation
        * representation
        * equality (__eq__)
        * hash (for set purposes)
        * invert
        * negation
        * addition
        * multiplication
        * substraction
        * division
    '''
    from fractions import gcd

    def __init__(self, num, den):
        assert den != 0, 'Rationnel indéfini : den = 0'
        self.den = den
        self.num = num

    def __repr__(self):
        gc = gcd(self.num, self.den)
        return str(self.num//gc) +'/' + str(self.den//gc)

    def __hash__(self):
        return hash(self.num)^hash(self.den)

    def inv(self):
        return Ratio(self.den, self.num)

    #Classic ops
    def __eq__(self, other):
        return self.num * other.den == other.num * self.den

    def __neg__(self):
        return Ratio(-self.num, self.den)

    def __add__(self, other):
        return Ratio(self.num*other.den + other.num*self.den, other.den*self.den)

    def __mul__(self, other):
        return Ratio(self.num*other.num, self.den*other.den)

    def __sub__(self, other):
        return self + -other

    def __truediv__(self, other):
        return self * other.inv()
