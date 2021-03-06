__author__ = 'srinath'

import tracemalloc
tracemalloc.start()

board_loc_dict = {}
board_loc_dict_reverse = {}
path_list = []
states = {"final_proper": 0, "final_improper": 1, "not_final": 2}
global no_of_nodes_expanded


def getInput():
    board = []
    index = 0
    for i in range(0, 7, 1):
        temp = []
        for j in range(0, 7, 1):
            if (i < 2 and (j < 2 or j > 4)) or (i > 4 and (j < 2 or j > 4)):
                temp.append(None)
            else:
                temp.append(0)
                board_loc_dict[(i, j)] = index;
                index += 1
        board.append(temp)

    string = "--XXX--,--XXX--,XXXXXXX,XXX0XXX,XXXXXXX,--XXX--,--XXX--"
    string = "--0XX--,--X0X--,0000X00,00XX0X0,0000000,--0XX--,--XX0--"
    #string = "--000--,--000--,0000000,0000XX0,0000000,--000--,--000--"
    print("Enter Board State:")
    string = input()
    l = string.split(',')
    #print(l)
    for i in range(0, 7, 1):
        for j in range(0, 7, 1):
            board[i][j] = l[i][j]
    return board

def checkFinalState(board_state):
    noOfX = 0;
    for i in board_state:
        noOfX += i.count('X')
    if noOfX == 1:
        if board_state[3][3] == 'X':
            return states["final_proper"]
        else:
            return states["final_improper"]
    else:
        return states["not_final"]

def isValidLeftMove(board_state, i, j):
    if ((i >= 2 and i <= 4 and j >= 2) or (j == 4)) and (
                board_state[i][j - 2] == '0' and board_state[i][j - 1] == 'X' and board_state[i][j] == 'X'):
        return True
    return False

def moveLeft(board_state, i, j):
    board_state[i][j - 2] = 'X'
    board_state[i][j - 1] = '0'
    board_state[i][j] = '0'


def isValidRightMove(board_state, i, j):
    if ((i >= 2 and i <= 4 and j <= 4) or (j == 2)) and (
                board_state[i][j + 2] == '0' and board_state[i][j + 1] == 'X' and board_state[i][j] == 'X'):
        return True
    return False

def moveRight(board_state, i, j):
    board_state[i][j + 2] = 'X'
    board_state[i][j + 1] = '0'
    board_state[i][j] = '0'
    #printBoard(board_state)

def isValidBottomMove(board_state, i, j):
    if ((j >= 2 and j <= 4 and i <= 4) or (i == 2)) and (
                board_state[i + 2][j] == '0' and board_state[i + 1][j] == 'X' and board_state[i][j] == 'X'):
        return True
    return False

def moveBottom(board_state, i, j):
    board_state[i + 2][j] = 'X'
    board_state[i + 1][j] = '0'
    board_state[i][j] = '0'

def isValidTopMove(board_state, i, j):
    if ((j >= 2 and j <= 4 and i >= 2) or (i == 4)) and (
                board_state[i - 2][j] == '0' and board_state[i - 1][j] == 'X' and board_state[i][j] == 'X'):
        return True
    return False

def moveTop(board_state, i, j):
    board_state[i - 2][j] = 'X'
    board_state[i - 1][j] = '0'
    board_state[i][j] = '0'

def testCases():
    # string = "--000--,--0X0--,00XXX00,000X000,000X000,--000--,--000--"
    string = "--000--,--000--,0000000,0000XX0,000X000,--000--,--000--"
    #string = input()
    board = []
    l = string.split(',')
    #print(l)
    for i in range(0, 7, 1):
        for j in range(0, 7, 1):
            board[i][j] = l[i][j]
    for i in board:
        print(i)

    print(isValidBottomMove(board, 3, 3))
    print(isValidBottomMove(board, 4, 3))
    print(isValidTopMove(board, 4, 3))
    print(isValidTopMove(board, 3, 3))
    print(isValidLeftMove(board, 3, 2))
    print(isValidLeftMove(board, 3, 3))
    print(isValidRightMove(board, 3, 3))
    print(isValidRightMove(board, 3, 2))


def findFirstPeg(board_state):
    for (i, j) in board_loc_dict.keys():
        if board_state[i][j] == 'X':
            return (i, j)
    return None

def getBestPegH2(board_state,move):
    if move == "left":
        isValidMove = isValidLeftMove
        movePeg = moveLeft
    elif move == "right":
        isValidMove = isValidRightMove
        movePeg = moveRight
    elif move == "top":
        isValidMove = isValidTopMove
        movePeg = moveTop
    elif move == "bottom":
        isValidMove = isValidBottomMove
        movePeg = moveBottom
    pegCountList = []
    for i in range(0,7,1):
        for j in range(0,7,1):
            if board_state[i][j]=='X':
                if isValidMove(board_state,i,j):
                    board_state_copy = unshared_copy(board_state)
                    movePeg(board_state_copy,i,j)
                    pegCountList.append((getIsolatedPegCount(board_state_copy),(i,j)))

    #sorted(pegCountList,key=lambda elem:elem[0])
    pegCountList.sort(key=lambda tup:tup[0])
    #for i in pegCountList:
    #    print(i)
    for i in pegCountList:
        yield i[1]


def getBestPegInitial(board_state):
    #sides = [0,1,2,12,19,26,32,31,30,20,13,6,3,4,5,11,18,25,29,28,27,21,14,7]
    sides_tuples = [(0, 2),(0, 3),(0, 4),(2, 6),(3, 6),(4, 6),(6, 4),(6, 3),(6, 2),(4, 0),(3, 0),(2, 0),(1, 2),(1, 3),(1, 4),(2, 5),(3, 5),(4, 5),(5, 4),(5, 3),(5, 2),(4, 1),(3, 1),(2, 1)]
    #center = [8,9,10,17,24,23,22,15,16]
    center_tuples = [(2, 2),(2, 3),(2, 4),(3, 4),(4, 4),(4, 3),(4, 2),(3, 2),(3, 3)]
    for (i,j) in sides_tuples:
        if board_state[i][j] == 'X':
            yield (i,j)
    for (i,j) in center_tuples:
        if board_state[i][j] == 'X':
            yield (i,j)


def getIsolatedPegCount(board_state):
    count = 0
    for i in range(0,7,1):
        for j in range(0,7,1):
            if board_state[i][j]=='X' and checkIfIsolated(board_state,i,j):
                count+=1
    return count

def checkIfIsolated(board_state,i,j):
    #print("isolation",i,j)
    #printBoard(board_state)
    if i >= 1 and i <= 5:
        if j>=1 and j<= 5:
            if board_state[i-1][j] == 'X' or board_state[i][j-1] == 'X' or board_state[i][j+1] == 'X' or board_state[i+1][j] == 'X':
                return False
            else:
                return True
        elif j==0:
            if board_state[i-1][j] == 'X' or board_state[i][j+1] == 'X' or board_state[i+1][j] == 'X':
                return False
            else:
                return True
        elif j==6:
            if board_state[i-1][j] == 'X' or board_state[i][j-1] == 'X' or board_state[i+1][j] == 'X':
                return False
            else:
                return True
    elif i==0:
        if j>=1 and j<= 5:
            if board_state[i][j-1] == 'X' or board_state[i][j+1] == 'X' or board_state[i+1][j] == 'X':
                return False
            else:
                return True
        elif j==0:
            if board_state[i][j+1] == 'X' or board_state[i+1][j] == 'X':
                return False
            else:
                return True
        elif j==6:
            if board_state[i][j-1] == 'X' or board_state[i+1][j] == 'X':
                return False
            else:
                return True
    elif i==6:
        if j>=1 and j<= 5:
            if board_state[i][j-1] == 'X' or board_state[i][j+1] == 'X' or board_state[i-1][j] == 'X':
                return False
            else:
                return True
        elif j==0:
            if board_state[i][j+1] == 'X' or board_state[i-1][j] == 'X':
                return False
            else:
                return True
        elif j==6:
            if board_state[i][j-1] == 'X' or board_state[i-1][j] == 'X':
                return False
            else:
                return True

def unshared_copy(inList):
    if isinstance(inList, list):
        return list(map(unshared_copy, inList))
    return inList

def printBoard(board_state):
    print("\n")
    for i in board_state:
        print(i)
    print("\n")

def findPath(board_state):
    #printBoard(board_state)
    global no_of_nodes_expanded
    no_of_nodes_expanded+=1
    finalstate = checkFinalState(board_state)
    if finalstate == states["final_proper"]:
            path_list.append("")
            return len(path_list) - 1  # returning index so that new node in the path is prepended to existing string
    elif finalstate == states["final_improper"]:
            print("final invalid state")
            return None
    else:
        for (i,j) in getBestPegH2(board_state,"left"):
            board_state_copy = unshared_copy(board_state)
            moveLeft(board_state_copy,i,j)
            ret = findPath(board_state_copy)
            if ret!=None:
                path = '(' + str(board_loc_dict[(i, j)]) + ',' + str(board_loc_dict[(i, j - 2)]) + ')'
                temp = path + " " + path_list[ret]
                path_list[ret] = temp
                return ret

        for (i,j) in getBestPegH2(board_state,"right"):
            board_state_copy = unshared_copy(board_state)
            moveRight(board_state_copy,i,j)
            ret = findPath(board_state_copy)
            if ret!=None:
                path = '(' + str(board_loc_dict[(i, j)]) + ',' + str(board_loc_dict[(i, j + 2)]) + ')'
                temp = path + " " + path_list[ret]
                path_list[ret] = temp
                return ret

        for (i,j) in getBestPegH2(board_state,"top"):
            board_state_copy = unshared_copy(board_state)
            moveTop(board_state_copy,i,j)
            ret = findPath(board_state_copy)
            if ret!=None:
                path = '(' + str(board_loc_dict[(i, j)]) + ',' + str(board_loc_dict[(i-2, j)]) + ')'
                temp = path + " " + path_list[ret]
                path_list[ret] = temp
                return ret

        for (i,j) in getBestPegH2(board_state,"bottom"):
            board_state_copy = unshared_copy(board_state)
            moveBottom(board_state_copy,i,j)
            ret = findPath(board_state_copy)
            if ret!=None:
                path = '(' + str(board_loc_dict[(i, j)]) + ',' + str(board_loc_dict[(i+2, j)]) + ')'
                temp = path + " " + path_list[ret]
                path_list[ret] = temp
                return ret
    return None






if __name__ == "__main__":
    import time
    startTime = time.time()
    global no_of_nodes_expanded
    no_of_nodes_expanded = 0
    board = getInput()
    #printBoard(board)
    for (i,j) in getBestPegInitial(board):
        ret = findPath(board)
        if ret != None:
            print(path_list)
            print("Statistics:")
            print("No. of Nodes Expanded: "+str(no_of_nodes_expanded))
            elapsedTime = time.time() - startTime
            print("Elapsed Time: "+str(elapsedTime)+" secs")
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')
            print("[ Top 10 ]")
            for stat in top_stats[:10]:
                print(stat)
            import sys
            sys.exit(0)
    print("No path found")
    print("Statistics:")
    print("No. of Nodes Expanded: "+str(no_of_nodes_expanded))
    elapsedTime = time.time() - startTime
    print("Elapsed Time: "+str(elapsedTime)+" secs")
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)


