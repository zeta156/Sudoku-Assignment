#Michael Cervantes
#Sudoku Assignment
#Python algorithm to solve a sudoku puzzle
#zeta156@csu.fullerton.edu
#cProfile used to test performance
import cProfile

# Board class represents my game board, it contains
# the "master list" of elements, which represent each cell in the matrix of the game
# it also contains objects that represent the rows,columns and subboards of the game
class Board:
  def __init__(self,boardString):
    self.elements = []
    self.rows = []
    self.columns = []
    self.subBoards = []
    #self.solved = False
    
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
      
        
  
# Element class represents each "cell" of the game board
# Each element knows which row/col/subBoard it is a member of, 
# as well as its value and index in the element list
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
    
    
# Row class represents a single row of the board
# Contains a list of its members, and can check itself for membership
# of a given value, as well as check itself for number of empty locations
class Row:
  def __init__(self,l,rowNum):
  #Get a list l of Elements
    self.rowValues = l
    for i in range(len(self.rowValues)):
      self.rowValues[i].rowNum = rowNum

    self.valueSet = set()
    for i in range(len(self.rowValues)):
      #print("ith time I added a value to set is",i)
      self.valueSet.add(self.rowValues[i].value)
    print('len of rowValues is:',len(self.rowValues))
    print('row internal value set is:',self.valueSet)  
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
  def numberOfChoices(self):
    self.valueSet.clear()
    for i in range(len(self.rowValues)):
      self.valueSet.add(self.rowValues[i].value)
    return (9 - len(self.valueSet))

  def hasNumber(self,n):
    self.valueSet.clear()
    for i in range(len(self.rowValues)):
      self.valueSet.add(self.rowValues[i].value)
    if n in self.valueSet:
      return True
    else:
      return False
    
  
  
# Column class represents a single column of the board
# Contains a list of its members, and can check itself for membership
# of a given value, as well as check itself for number of empty locations        
class Column:
  def __init__(self,l,colNum):
    self.colValues = l
    self.valueSet = set()
    for i in range(len(self.colValues)):
      self.colValues[i].colNum = colNum
      
    self.valueSet = set()
    for i in range(len(self.colValues)):
      self.valueSet.add(self.colValues[i].value)
    

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
    
  def numberOfChoices(self):
    self.valueSet.clear()
    for i in range(len(self.colValues)):
      self.valueSet.add(self.colValues[i].value)
    return (9 - len(self.valueSet))
  
  def hasNumber(self,n):
    self.valueSet.clear()
    for i in range(len(self.colValues)):
      self.valueSet.add(self.colValues[i].value)
    if n in self.valueSet:
      return True
    else:
      return False
  
          
  
# SubBoard class represents a single sub board of the board
# Contains a list of its members, and can check itself for membership
# of a given value, as well as check itself for number of empty locations
class SubBoard:
  def __init__(self,row1,row2,row3,sbNum):
    self.subBoardValues = row1 + row2 + row3
    self.valueSet = set()
    for i in range(len(self.subBoardValues)):
      self.subBoardValues[i].subBoardNum = sbNum
  
    self.valueSet = set()
    for i in range(len(self.subBoardValues)):
      self.valueSet.add(self.subBoardValues[i].value)

  def numberOfChoices(self):
    self.valueSet.clear()
    for i in range(len(self.subBoardValues)):
      self.valueSet.add(self.subBoardValues[i].value)
    return (9 - len(self.valueSet))

  def hasNumber(self,n):
    self.valueSet.clear()
    for i in range(len(self.subBoardValues)):
      self.valueSet.add(self.subBoardValues[i].value)
    if n in self.valueSet:
      return True
    else:
      return False
  
  
  
      
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
          
  
# Finds and returns an empty element, which would be filled by solve sudoku
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

# An attempt to find the "best" empty element, i.e., an element that is in a row/col/SB
# that has the least number of choices, this does work but is much slower than 
# naive findEmptyElement

def findBestEmptyElement(board,eleNum):
  emptyLocationList = []
  bestLocation = None
  leastNumberOfChoices = 9
  
  for i in range(len(board.elements)):
    #print(type(board.elements[i]),i)
    if board.elements[i].value == -1:
      emptyLocationList.append(board.elements[i])
    
        
  #Empty loc list has all empty elements, have to find
  #which is best candidate, i.e.
  #which is in a row/col/subB with the least choices
  
  if not emptyLocationList:
    return False #No empty elements found
  else:
    for i in range(len(emptyLocationList)):
    
    #Check for a best location among rows
      x = board.rows[emptyLocationList[i].rowNum].numberOfChoices()
      if x < leastNumberOfChoices:
        bestLocation = emptyLocationList[i]

    #Check for a best location among columns

    for i in range(len(emptyLocationList)):
      x = board.columns[emptyLocationList[i].colNum].numberOfChoices()
      if x < leastNumberOfChoices:
        bestLocation = emptyLocationList[i]

    #Check for a best location among subBoards
    for i in range(len(emptyLocationList)):
      x = board.subBoards[emptyLocationList[i].subBoardNum].numberOfChoices()
      if x < leastNumberOfChoices:
        bestLocation = emptyLocationList[i]

    #Return best location on the eleNum list
    eleNum.append(bestLocation.eleNum)
    #Return true, a empty element was found
    return True
    
  
  #if(location):
  #  eleNum.append(location.eleNum)
  #  #print("findEE about to return True")
  #  return True
  #else:
  #  #print("findEE about to return False")
  #  return False

# This function checks if the "number" that will attempt insertion in an element
# has no conflicts with the row/col/subboard of that element, i.e. this checks against
# insertion of duplicate values which violate sudoku rules

def noConflicts(board,element,num):
#Must check for row, column, and subBoard conflicts(duplicates)
  #get list of numbers in elements row, check for duplicates with num
  #rowNumbers = board.rows[element.rowNum].intList()
  #if num in rowNumbers:
  
  
  if(board.rows[element.rowNum].hasNumber(num)):
    return False #conflict found in row
  #if num in board.rows[element.rowNum].valueSet:
  #  print('row value set',board.rows[element.rowNum].valueSet)
  #  return False
  
  #colNumbers = board.columns[element.colNum].intList()
  #if num in colNumbers:
  
  #elif num in board.columns[element.colNum].valueSet:
  #  print('col value set',board.columns[element.colNum].valueSet)
  elif board.columns[element.colNum].hasNumber(num):
    return False #conflict found in column
    
  #sbNumbers = board.subBoards[element.subBoardNum].intList()
  #if num in sbNumbers:
  #elif num in board.subBoards[element.subBoardNum].valueSet:
  elif board.subBoards[element.subBoardNum].hasNumber(num):
    return False #Conflict found in sub board
  else:
    
    return True #No conflict found  
      
      
# Function to recursively solve the sudoku puzzle, essentially a brute force algorithm
# that just fills in each element with a non conflicted number and moves on to the next
# back tracking when a dead end is met
def solveSudoku(board):
  x,y = [],[]
  eleNum = []
  #print("Entered solveSudoku")
  
  if(not findEmptyElement(board,eleNum)):
  #  #print("Entered first if")
    return True
  
  # Works but much slower
  #if(not findBestEmptyElement(board,eleNum)):
  #  return True
   
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
  
  #input takes ~370 seconds to solve
  input = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
  
  #input2 takes ~27 seconds to solve
  input2 = '.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...'
  
  #z = Board(input)
  z = Board(input2)  
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
    
        