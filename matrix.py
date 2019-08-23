##=======================================================
## Bosen Qu (20768684)
## August 23, 2019
## Matrix class that supports Matirx calculations
##=======================================================

import fraction

def empty_val(row, col):
    '''
    returns initialized value for a row * col matrix
    
    empty_val: Nat Nat -> (listof (listof "undefined"))
    
    Examples:
        empty_val(2, 3) => [["undefined", "undefined", "undefined"]
                           ["undefined", "undefined", "undefined"]]
    '''
    lst = []
    for i in range(row):
        lst.append([])
        for j in range(col):
            lst[i].append("undefined")
    return lst
    
def leading_one_index(row):
    '''
    returns the index of leading one in a row, assuming the
        row is in a RREF matirx, or returns the column size
        if there is no leading one
        
    leading_one_index: (listof (anyof Int Float Fraction)) -> Nat
    
    Examples:
        leading_one_index([0, 1, 2, 3]) => 1
        leading_one_index([1, 2, 3, 4]) => 4
    '''
    rv = 0
    for n in row:
        if n == 1:
            break
        rv += 1
    return rv
    
def std_matrix_val(n):
    '''
    returns the value of a n * n standard matrix
    
    std_matrix_val: Nat -> (listof (listof Fraction))
    
    Examples: std_matrix_val(3): [[Fraction(1), Fraction(0), Fraction(0)]
                                  [Fraction(0), Fraction(1), Fraction(0)]
                                  [Fraction(0), Fraction(0), Fraction(1)]]
    '''
    lst = empty_val(n, n)
    for i in range(n):
        for j in range(n):
            lst[i][j] = fraction.Fraction(1) if i == j\
                        else fraction.Fraction(0)
    return lst        

class Matrix:
    '''
    Fields: row(Nat), col(Nat), val(listof (listof Fraction))
    '''
    
    def __init__(self, row, col, val = []):
        '''
        Constructor: Creates a Matrix object by calling Matrix(row, col, val)
        
        __init__: Nat Nat (anyof (listof (listof Fraction)) None) -> None
        ''' 
        self.row = row
        self.col = col
        if val == []:
            self.val = empty_val(self.row, self.col)
            self.input()
            Matrix.print(self)
        else:
            self.val = val
    
    def input(self):
        '''
        coverts user input to the value of matrix
        
        input: Matrix -> None
        
        Effects: asks user for input
        '''
        for i in range(self.row):
            for j in range(self.col):
                print(f"input M({i + 1}, {j + 1}): ", end = "")
                self.val[i][j] = fraction.cast_str(input())
    
    def print(self):
        '''
        prints the matrix
        
        print: Matrix -> None
        
        Effects: prints out the matrix
        '''
        for i in range(self.row):
            for num in self.val[i]:
                print(num, end = " ")
            print()
            
    def deep_copy(self, only_val = False):
        '''
        returns a copy of self or only its value
        
        deep_copy: Matrix (anyof Bool None) -> (anyof Matrix (listof (listof Fraction))
        '''
        new_val = []
        for i in range(self.row):
            new_val.append([])
            new_val[i] = [j for j in self.val[i]]
        return new_val if only_val else Matrix(self.row, self.col, new_val)
        
            
    def __add__(self, other):
        '''
        returns the result of self + other
        
        __add__: Matrix Matrix -> Matrix
        requires: self.row == other.row
                  self.col == other.col
        '''
        if self.row != other.row or self.col != other.col:
            return "undefined"
        val = empty_val(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                val[i][j] = self.val[i][j] + other.val[i][j]
        return Matrix(self.row, self.col, val)
    
    __radd__ = __add__
        
    def __sub__(self, other):
        '''
        returns the result of self - other
        
        __sub__: Matrix Matrix -> Matrix
        requires: self.row == other.row
                  self.col == other.col
        '''
        if self.row != other.row or self.col != other.col:
            return "undefined"
        val = empty_val(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                val[i][j] = self.val[i][j] - other.val[i][j]
        return Matrix(self.row, self.col, val)
    
    def __mul__(self, other):
        '''
        returns the result of self * other
        
        __mul__: Matrix (anyof Fraction Int Float) -> Matrix
        requires: if type(other) == matrix, then self.row == other.col
        '''
        if type(other) == Matrix:
            if self.col != other.row:
                return "undefined"
            val = empty_val(self.row, other.col)
            for i in range(self.row):
                for j in range(other.col):
                    temp = 0
                    for k in range(self.col):
                        temp += self.val[i][k] * other.val[k][j]
                    val[i][j] = temp
            return Matrix(self.row, other.col, val)
        else:
            val = empty_val(self.row, self.col)
            mult = other if type(other) == fraction.Fraction \
                   else fraction.Fraction(other)
            for i in range(self.row):
                for j in range(self.col):
                    val[i][j] = self.val[i][j] * mult
            return Matrix(self.row, self.col, val)
        
    def __rmul__(self, other):
        '''
        returns the result of other * self
        
        __rmul__: Matrix (anyof Fraction, Int, Float) -> Matrix
        '''
        return self * other
    
    def is_non_zero_row(self, row):
        '''
        returns True if self.val[row] is a non zero row, returns False otherwise
        
        is_non_zero_row: Matrix, Nat -> Bool
        '''
        i = 0
        for n in self.val[row]:
            if n != 0:
                return (n, i)
            i += 1
        return False
    
    def is_RREF(self):
        '''
        returns True if self is in RREF form, returns False otherwise
        
        is_RREF: Fraction -> Bool
        '''
        prev_leading_one_index = -1
        #check zero row
        for i in range(self.row):
            r = self.is_non_zero_row(i)
            #find a zero row
            if r == False:
                #check if rows below are zero row
                for j in range(i + 1, self.row):
                    if self.is_non_zero_row(j):
                        return False
                return True
            #not a zero row, check leading one, and its position
            if r[0] != 1:
                return False
            if r[1] <= prev_leading_one_index:
                return False
            #check if the leading one is the only non zero entry in its column
            for j in range(self.row):
                if j != i and self.val[j][r[1]] != 0:
                    return False
            prev_leading_one_index = r[1]
        return True
    
    def row_mult(self, row_num, mult):
        self.val[row_num] = list(map(lambda x: x * mult, self.val[row_num]))
    
    def row_swap(self, row_num_1, row_num_2):
        for i in range(self.col):
            self.val[row_num_1][i], self.val[row_num_2][i] =\
            self.val[row_num_2][i], self.val[row_num_1][i]
    
    def row_add_mult(self, row_num_1, row_num_2, mult):
        for i in range(self.col):
            self.val[row_num_1][i] += self.val[row_num_2][i] * mult
                    
    def row_reduce(self, n):
        #if first is zero, find a non-zero row
        have_non_zero_row = False
        for i in range(n, self.row):
            #find a non zero row, swap with first row
            if self.val[i][n] != 0:
                self.row_swap(n, i)
                have_non_zero_row = True
                break;
        #reduce first entry of each row
        if have_non_zero_row:
            self.row_mult(n, self.val[n][n].recip())
            for i in range(n + 1, self.row):
                self.row_add_mult(i, n, -self.val[i][n])             
        #if 1 * n or n * 1 matrix, exit
        if n == self.row - 1 or n == self.col - 1:
            return      
        #keep reducing
        self.row_reduce(n + 1)
        #reduce each entry of the n-th row
        for i in range(n + 1, min(self.col, self.row)):
            self.row_add_mult(n, i, -self.val[n][i])
            
    def rearrange_leading_one(self):
        self.val.sort(key = lambda x: leading_one_index(x))
            
    def RREF(self):
        m = self.deep_copy()
        m.row_reduce(0)
        m.rearrange_leading_one()
        return m
    
    def rank(self):
        RREF = self.RREF()
        r = 0
        for i in range(RREF.row):
            if not RREF.is_non_zero_row(i):
                return r
            r += 1
        del RREF
        return r
    
    def invertible(self):
        return self.row == self.col == self.rank()
    
    def inverse(self):
        if not self.invertible():
            return "undefined"
        aug_self = Aug_Matrix(self.row, self.col, self.row,
                              self.deep_copy(True), std_matrix_val(self.row))
        return Matrix(self.row, self.col, aug_self.RREF().aug)
    
    def transpose(self):
        val = empty_val(self.col, self.row)
        for i in range(self.row):
            for j in range(self.col):
                val[j][i] = self.val[i][j]
        return Matrix(self.col, self.row, val)
    
    def remove_row_col(self, row, col):
        rv = self.deep_copy()
        rv.val.pop(row)
        for row in rv.val:
            row.pop(col)
        rv.row -= 1
        rv.col -= 1
        return rv
        
    def det(self):
        if self.row != self.col:
            return "undefined"
        if self.row == 1:
            return self.val[0][0]
        if self.row == 2:
            return self.val[0][0] * self.val[1][1] -\
                   self.val[0][1] * self.val[1][0]
        det = fraction.Fraction(0)
        for i in range(self.col):
            det += ((-1) ** i) * self.val[0][i] * self.remove_row_col(0, i).det()
        return det
    
    def is_upper_triangular(self):
        for j in range(self.col):
            for i in range(j + 1, self.row):
                if self.val[i][j] != 0:
                    return False
        return True
    
    def is_lower_triangular(self):
        for j in range(self.col):
            for i in range(0, j - 1):
                if self.val[i][j] != 0:
                    return False
        return True
    
    def is_triangluar(self):
        return is_upper_triangular or is_lower_triangular
        
class Aug_Matrix(Matrix):
    def __init__(self, row, col, aug_col, val = [], aug = []):     
        Matrix.__init__(self, row, col, val)
        self.col += aug_col
        self.aug_col = aug_col
        if aug == []:
            self.input_aug()
            self.print()
        else:
            self.aug = aug
    
    def input_aug(self):
        for i in range(self.aug_col):
            for j in range(self.row):
                print(f"input aug({j + 1}, {i + 1}): ", end = "")
                self.val[j].append(fraction.cast_str(input()))
    
    def print(self):
        for i in range(self.row):
            for j in range(self.col):
                if j == self.col - self.aug_col:
                    print("|", end = " ")
                print(self.val[i][j], end = " ")
            print()
               
    def deep_copy(self):
        rv = Matrix.deep_copy(self)
        rv.aug_col = self.aug_col
        rv.__class__ = Aug_Matrix
        return rv
    
    def __add__(self, other):
        return "undefined"
    
    def __radd__(self, other):
        return "undefined"
    
    def __sub__(self, other):
        return "undefined"
    
    def __mul__(self, other):
        return "undefined"
        
    def __truediv__(self, other):
        return "undefined"