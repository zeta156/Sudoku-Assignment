
import cProfile
class Board:
  def __init__(self,boardString):
    self.elements = []
    self.rows = []
    self.columns = []
    self.subBoards = []
    self.solved = False
    
    n = 0
    for e in boardString:
      self.elements.append(Element(e,n))
      n += 1
      
    n = 0  
    for i in range(0,81,9):
      l = self.elements[i:i+9]
      self.rows.append(Row(l,n))
      n += 1
      
    n = 0  
    for i in range(9):
      l = self.elements[i:81:9]
      self.columns.append(Column(l,n))
      n += 1
    
    n = 0  
    for i in range(0,81,27):
      for j in range(0,9,3):
        r1 = self.elements[i+j:i+j+3]
        r2 = self.elements[i+j+9:i+j+12]
        r3 = self.elements[i+j+18:i+j+21]
        self.subBoards.append(SubBoard(r1,r2,r3,n))
        n += 1
      
        
  
      
class Element:
  def __init__(self,e,n):
    self.eleNum = n
    if(e=='.'):
      self.value = -1
    else:
      self.value = int(e)
    self.colNum = None
    self.rowNum = None
    self.subBoardNum = None
    
class Row:
  def __init__(self,l,rowNum):
  #Get a list l of Elements
    self.rowValues = l
    self.valueSet = set()
    for i in range(len(self.rowValues)):
      self.rowValues[i].rowNum = rowNum
  def display(self):
    print("Values of this row are:",end='')
    for i in range(len(self.rowValues)):
      print(self.rowValues[i].value,end='')
    print('')       
  def intList(self):
    x = set()
    for i in range(len(self.rowValues)):
      x.add(self.rowValues[i].value)
    return x
  def hasNumber(self,n):
    self.valueSet.clear()
    for i in range(len(self.rowValues)):
      self.valueSet.add(self.rowValues[i].value)
    if n in self.valueSet:
      return True
    else:
      return False
    
  
          
class Column:
  def __init__(self,l,colNum):
    self.colValues = l
    for i in range(len(self.colValues)):
      self.colValues[i].colNum = colNum
  def display(self):
    print("Values of this column are:",end='')
    for i in range(len(self.colValues)):
      print(self.colValues[i].value,end='')
    print('')    
       
  def intList(self):
    x = set()
    for i in range(len(self.colValues)):
      x.add(self.colValues[i].value)
    return x
          
  
class SubBoard:
  def __init__(self,row1,row2,row3,sbNum):
    self.subBoardValues = row1 + row2 + row3
    
    for i in range(len(self.subBoardValues)):
      self.subBoardValues[i].subBoardNum = sbNum
      
  def printHello(self):
    print("hello")  
  def display(self):
    print("Values of this sub board are:",end='')
    for i in range(len(self.subBoardValues)):
      print(self.subBoardValues[i].value,end='')
    print('')
       
  def intList(self):
    x = set()
    for i in range(len(self.subBoardValues)):
      x.add(self.subBoardValues[i].value)
    return x
          
  
def findEmptyElement(board,eleNum):
  location = None
  for i in range(len(board.elements)):
      #print(type(board.elements[i]),i)
      if board.elements[i].value == -1:
        location = board.elements[i]
  if(location):
    eleNum.append(location.eleNum)
    #print("findEE about to return True")
    return True
  else:
    #print("findEE about to return False")
    return False

def noConflicts(board,element,num):
#Must check for row, column, and subBoard conflicts(duplicates)
  #get list of numbers in elements row, check for duplicates with num
  #rowNumbers = board.rows[element.rowNum].intList()
  #if num in rowNumbers:
  if(board.rows[element.rowNum].hasNumber(num)):
    return False #conflict found in row
  colNumbers = board.columns[element.colNum].intList()
  if num in colNumbers:
    return False #conflict found in column
  sbNumbers = board.subBoards[element.subBoardNum].intList()
  if num in sbNumbers:
    return False #Conflict found in sub board
  return True #No conflict found  
      
def solveSudoku(board):
  x,y = [],[]
  eleNum = []
  #print("Entered solveSudoku")
  if(not findEmptyElement(board,eleNum)):
    #print("Entered first if")
    return True
   
  for num in range(1,10):
    #print("Entered first For")
    if(noConflicts(board,board.elements[eleNum[0]],num)):
      board.elements[eleNum[0]].value = num
      if(solveSudoku(board)):
        return True
      board.elements[eleNum[0]].value = -1
  return False    
  
    
def main():
  
  print('Hi, Sudoku assignment')
  inputMissingOne = '4173698256321589479587243168254371.9791586432346912758289643571573291684164875293' #Missing 6
  inputMissingThree = '4173698256.21589479587243168254371.9791586432346912758289643571.73291684164875293' #Missing 3,6

  solvedInput = '417369825632158947958724316825437169791586432346912758289643571573291684164875293'
  input = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
  z = Board(input)
  #z = Board(input)
  
  #for i in range(81):
  #  print(z.elements[i].value,end='')
  #print('')
  #print(z.rows)
  
  #Print out each row
  
  
  for i in range(len(z.rows)):
    for j in range(len(z.rows[i].rowValues)):
      print(z.rows[i].rowValues[j].value,end="")
    print('')
    
  #z.rows[0].display()
  #z.columns[0].display()
  #for i in range(9):
  #  print('sub board number',i)
  #  z.subBoards[i].display()
  #  #print(i)
  #print("There are this many sub boards",len(z.subBoards))
  
  #solveSudoku(z)
  #t = z.rows[0].intList()
  #print(t)
  #print(z.elements[72].value)
  #print('row:',z.elements[72].rowNum)
  #print('col:',z.elements[72].colNum)
  #print('sub board number',z.elements[72].subBoardNum)
  #z.subBoards[6].display()
  #print("in main")
  #for i in range(len(z.elements)):
  #  print(type(z.elements[i]),i)
  solveSudoku(z)
  print("Called solve Sudoku")
  for i in range(len(z.rows)):
    for j in range(len(z.rows[i].rowValues)):
      print(z.rows[i].rowValues[j].value,end="")
    print('')

if __name__ == "__main__":
    
  cProfile.run('main()')
    
        