'''
  Bosen Qu (20768684)
  August 18, 2019
  Fraction class that supports fraction calculations
'''

def gcd(a, b):
    # gcd(a, b) computes the greatest common divisor of a and b
    # gcd: Int Int -> Int
        if a % b == 0:
            return b
        return gcd(b, a % b)
   
def scm(a, b):
    # scm(a, b) computes the smallest common multiplier of a and b
    # scm: Int Int -> Int
    return a * b // gcd(a, b)
    
def cast_str(str):
    # cast_str(str) casts a string str to a fraction
    # cast_str: Str -> Fraction
        if '/' in str:
            nums = list(map(float, str.split('/')))
            return Fraction(nums[0], nums[1])
        else:
            return Fraction(float(str), 1)

class Fraction:
    def __init__(self, nume, deno = 1, neg = False):
        self.nume, self.deno = abs(nume), abs(deno)
        self.neg = neg if nume > 0 and deno > 0 or\
                          nume < 0 and deno < 0\
                       else not neg
        self.reduce()
    
    def reduce(self):
        while int(self.nume) != self.nume or int(self.deno) != self.deno:
            self.nume = self.nume * 10
            self.deno = self.deno * 10
        self.nume = int(self.nume)
        self.deno = int(self.deno)
        n = gcd(self.nume, self.deno)
        self.nume = self.nume // n
        self.deno = self.deno // n
    
    def __repr__(self):
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
    
    def sum_scalar(self, other, sign):
        sum_deno = scm(self.deno, other.deno)
        sum_nume = self.nume * (sum_deno // self.deno) + other.nume * (sum_deno // other.deno)
        return Fraction(sum_nume, sum_deno, sign)
    
    def diff_scalar(self, other, sign):
        diff_deno = scm(self.deno, other.deno)
        diff_nume = self.nume * (diff_deno // self.deno) - other.nume * (diff_deno // other.deno)
        return Fraction(abs(diff_nume), diff_deno, sign)
    
    def __abs__(self):
        return Fraction(self.nume, self.deno, False)
    
    def __neg__(self):
        return Fraction(self.nume, self.deno, not self.neg)
    
    def __eq__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        if self.nume == 0 and other.nume == 0 and self.deno != 0 and other.deno != 0:
            return True
        return self.neg == other.neg and self.nume == other.nume and self.deno == other.deno
    
    def __lt__(self, other):
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
        if type(other) != Fraction:
            other = Fraction(other)
        return (not self < other) and (not self == other)
            
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

    __rmul___ = __mul__
    
    def recip(self):
        return Fraction(self.deno, self.nume, self.neg)
    
    def __truediv__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        return self * other.recip()
        