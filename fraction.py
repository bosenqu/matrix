##=======================================================
## Bosen Qu (20768684)
## August 21, 2019
## Fraction class that supports fraction calculations
##=======================================================

def gcd(a, b):
    '''
    gcd(a, b) returns the greatest common divisor of a and b
    
    gcd: Nat Nat -> Nat 
    requires: b != 0
    
    Examples:
        gcd(5, 15) => 5
        gcd(14, 15) => 1
    '''
    if a % b == 0:
        return b
    return gcd(b, a % b)
   
def scm(a, b):
    '''
    scm(a, b) returns the smallest common multiplier of a and b
    
    scm: Nat Nat -> Nat 
    requires: b != 0
    
    Examples:
        scm(4, 6) => 12
        scm(5, 3) => 15
    '''
    return a * b // gcd(a, b)
    
def cast_str(str):
    '''
    cast_str(str) returns str casted as Fraction object
    
    cast_str: Str -> Fraction 
    requires: must be a proper fraction
    
    Examples:
        cast_str(“5/6”) => 5/6 stored as Fraction
        cast_str("-5/6") => -5/6 stored as Fraction
        cast_str("2/6") => 1/3 stored as Fraction
        cast_str("3") => 3 stroed as Fraction
    '''
    if '/' in str:
        nums = list(map(float, str.split('/')))
        return Fraction(nums[0], nums[1])
    else:
        return Fraction(float(str), 1)

class Fraction:
    '''
    Fields: nume(Int), deno(Nat), neg(Bool)
    requires: nume >= 0
    '''
    
    def __init__(self, nume, deno = 1, neg = False):
        '''
        Constructor: Creates a Fraction object by calling fraction(nume, deno, neg)
        
        __init__: Int (anyof Int, Float, None) (anyof Int, Float, None) Bool -> None
        requires: deno != 0
        '''
        self.nume, self.deno = abs(nume), abs(deno)
        self.neg = neg if nume > 0 and deno > 0 or\
                          nume < 0 and deno < 0\
                       else not neg
        self.reduce()
    
    def reduce(self):
        '''
        reduces self.nume and self.deno to simplist form of fraction
        
        reduce: None -> None
        
        Examples:
        if self is Fraction(3, 6, True), then self becomes -1/2 stored as Fraction
        if self is Fraction(-3, 6), then self becomes -1/2 stored as Fraction
        if self is Fraction(3, -6), then self becomes -1/2 stored as Fraction
        if self is Fraction(3, -6, True), then self becomes 1/2 stored as Fraction
        if self is Fraction(2.5, 3.5), then self becomes 5/7 stored as Fraction
        if self is Fraction(0.75), then self becomes 3/4 stored as Fraction
        '''
        while int(self.nume) != self.nume or int(self.deno) != self.deno:
            self.nume = self.nume * 10
            self.deno = self.deno * 10
        self.nume = int(self.nume)
        self.deno = int(self.deno)
        n = gcd(self.nume, self.deno)
        self.nume = self.nume // n
        self.deno = self.deno // n
    
    def __repr__(self):
        '''
        returns a string representation of self
        
        __repr__: Fraction -> Str
        '''
        if self.deno == 0:
            return "undenfined"
        if self.nume == 0:
            return "0"
        rv = ""
        if self.neg:
            rv += "-"
        rv = rv + str(self.nume)
        if self.deno != 1:
            rv += "/" + str(self.deno)
        return rv
    
    def __abs__(self):
        '''
        returns the absolute value of self
        
        __abs__: Fraction -> Fraction
        '''
        return Fraction(self.nume, self.deno, False)
    
    def __neg__(self):
        '''
        returns the negation of self
        
        __neg__: Fraction -> Fraction
        '''
        return Fraction(self.nume, self.deno, not self.neg)
    
    def __eq__(self, other):
        '''
        returns True if self and other are considered equal, False other-wise
        
        __eq__: Fraction, Any -> Bool
        '''
        if type(other) != Fraction:
            other = Fraction(other)
        if self.nume == 0 and other.nume == 0 and self.deno != 0 and other.deno != 0:
            return True
        return self.neg == other.neg and self.nume == other.nume and self.deno == other.deno
    
    def __lt__(self, other):
        '''
        returns True if self is less than other
        
        __lt__: Fraction, Any -> Bool
        '''
        if type(other) != Fraction:
            other = Fraction(other)
        if self == other:
            return False
        if self.neg == other.neg:
            comm_deno = scm(self.deno, other.deno)
            scalar_less = self.nume * (comm_deno // self.deno) <\
                          other.nume * (comm_deno // other.deno)
            return not scalar_less if self.neg else scalar_less
        else:
            return self.neg == True
    
    def __gt__(self, other):
        '''
        returns True if self is greater than other
        
        __gt__: Fraction, Any -> Bool
        '''
        if type(other) != Fraction:
            other = Fraction(other)
        return (not self < other) and (not self == other)
            
    def sum_scalar(self, other, sign):
        '''
        returns a Fraction object whose value is by abs(self) + abs(other),
          with neg = sign
        
        sum_scalar: Fraction Fraction Bool -> Fraction
        
        Examples:
        if a is Fraction(3, 5, True) and b is Fraction(4, 5, True), then
          a.sum_scalar(b, False) => Fraction(7, 5, False)
          a.sum_scalar(b, True) => Fraction(7, 5, True)
        '''
        sum_deno = scm(self.deno, other.deno)
        sum_nume = self.nume * (sum_deno // self.deno) + other.nume * (sum_deno // other.deno)
        return Fraction(sum_nume, sum_deno, sign)
    
    def diff_scalar(self, other, sign):
        '''
        returns a Fraction object whose value is the absolute value of abs(self) - abs(other),
          with neg = sign
          
        diff_scalar: Fraction Fraction Bool
        
        Examples:
        if a is Fraction(3, 5, True) and b is Fraction(4, 5, True), then
          a.diff_scalar(b, False) => Fraction(1, 5, False)
          a.diff_scalar(b, True) => Fraction(1, 5, True)
        '''
        diff_deno = scm(self.deno, other.deno)
        diff_nume = self.nume * (diff_deno // self.deno) - other.nume * (diff_deno // other.deno)
        return Fraction(abs(diff_nume), diff_deno, sign)
    
    def __add__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        if self.neg == other.neg:
            return Fraction.sum_scalar(self, other, self.neg)
        else:
            return Fraction.diff_scalar(self, other, not self.neg if abs(self) < abs(other) else self.neg)
    
    __radd__ = __add__
    
    def __sub__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        return self + (-other)
    
    def __rsub__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        return other + (-self)
    
    def __mul__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        return Fraction(self.nume * other.nume, self.deno * other.deno, not self.neg == other.neg)

    __rmul__ = __mul__
    
    def recip(self):
        return Fraction(self.deno, self.nume, self.neg)
    
    def __truediv__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        return self * other.recip()
        