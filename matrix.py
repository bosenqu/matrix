import fraction

def empty_val(row, col):
        lst = []
        for i in range(row):
            lst.append([])
            for j in range(col):
                lst[i].append("undefined")
        return lst
    
def is_zero_row(row):
    for n in row:
        if n != 0:
            return False
    return True

def std_matrix_val(n):
    lst = empty_val(n, n)
    for i in range(n):
        for j in range(n):
            lst[i][j] = fraction.Fraction(1) if i == j\
                        else fraction.Fraction(0)
    return lst        

class Matrix:
    def __init__(self, row, col, val = []):
        self.row = row
        self.col = col
        if val == []:
            self.val = empty_val(self.row, self.col)
            self.input()
            Matrix.print(self)
        else:
            self.val = val
    
    def input(self):
        for i in range(self.row):
            for j in range(self.col):
                print(f"input M({i + 1}, {j + 1}): ", end = "")
                self.val[i][j] = fraction.cast_str(input())
    
    def print(self):
        for i in range(self.row):
            for num in self.val[i]:
                print(num, end = " ")
            print()
            
    def deep_copy(self, only_val = False):
        new_val = []
        for i in range(self.row):
            new_val.append([])
            new_val[i] = [j for j in self.val[i]]
        return new_val if only_val else Matrix(self.row, self.col, new_val)
        
            
    def __add__(self, other):
        if self.row != other.row or self.col != other.col:
            return "undefined"
        val = empty_val(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                val[i][j] = self.val[i][j] + other.val[i][j]
        return Matrix(self.row, self.col, val)
        
    def __sub__(self, other):
        if self.row != other.row or self.col != other.col:
            return "undefined"
        val = empty_val(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                val[i][j] = self.val[i][j] - other.val[i][j]
        return Matrix(self.row, self.col, val)
    
    def __mul__(self, other):
        if type(other) == Matrix:
            if self.col != other.row:
                return "undefined"
            val = empty_val(self.row, other.col)
            for i in range(self.row):
                for j in range(other.col):
                    temp = Fraction(0)
                    for k in range(self.col):
                        temp += self.val[i][k] * other.val[k][j]
                    val[i][j] = temp
            return Matrix(self.row, other.col, val)
        else:
            val = empty_val(self.row, self.col)
            mult = other if type(other) == Fraction else Fraction.cast_num(other)
            for i in range(self.row):
                for j in range(self.col):
                    val[i][j] = self.val[i][j] * mult
            return Matrix(self.row, self.col, val)
        
    def is_non_zero_row(self, row):
        i = 0
        for n in self.val[row]:
            if n != 0:
                return (n, i)
            i += 1
        return False
    
    def is_RREF(self):
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
            
    def rearrange_zero_rows(self):
        self.val.sort(key = lambda x: 1 if is_zero_row(x) else 0)
            
    def RREF(self):
        m = self.deep_copy()
        m.row_reduce(0)
        m.rearrange_zero_rows()
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
        
        
class Aug_Matrix(Matrix):
    def __init__(self, row, col, aug_col, val = [], aug = []):
        Matrix.__init__(self, row, col, val)
        self.aug_col = aug_col
        if aug == []:
            self.aug = empty_val(self.row, self.aug_col)
            self.input_aug()
            self.print()
        else:
            self.aug = aug
    
    def input_aug(self):
        for i in range(self.aug_col):
            for j in range(self.row):
                print(f"input aug({j + 1}, {i + 1}): ", end = "")
                self.aug[j][i] = Fraction.cast_str(input())
    
    def print(self):
        for i in range(self.row):
            for num in self.val[i]:
                print(num, end = " ")
            print("|", end = " ")
            for num in self.aug[i]:
                print(num, end = " ")
            print()
               
    def deep_copy(self):
        new_val = []
        new_aug = []
        for i in range(self.row):
            new_val.append([])
            new_val[i] = [j for j in self.val[i]]
            new_aug.append([])
            new_aug[i] = [j for j in self.aug[i]]
        return Aug_Matrix(self.row, self.col, self.aug_col, new_val, new_aug)
    
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
    
    def row_mult(self, row_num, mult):
        Matrix.row_mult(self, row_num, mult)
        self.aug[row_num] = list(map(lambda x: x * mult, self.aug[row_num]))
    
    def row_swap(self, row_num_1, row_num_2):
        Matrix.row_swap(self, row_num_1, row_num_2)
        for i in range(self.aug_col):
            self.aug[row_num_1][i], self.aug[row_num_2][i] =\
            self.aug[row_num_2][i], self.aug[row_num_1][i]
    
    def row_add_mult(self, row_num_1, row_num_2, mult):
        Matrix.row_add_mult(self, row_num_1, row_num_2, mult)
        for i in range(self.aug_col):
            self.aug[row_num_1][i] += self.aug[row_num_2][i] * mult
    
        
m1 = Matrix(3, 3)
print(m1.invertible())