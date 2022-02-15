import random,sys
d={'tl':0,'tm':2,'tr':4,'ml':6,'mm':8,'mr':10,'bl':12,'bm':14,'br':16}
board='-|-|-\n-|-|-\n-|-|-'  

def t():
    if len(sys.argv)>1:
        x=sys.argv[1]
    else:
        x=input('1 or 2 players: ')
    if x == '2':
        print(board)
        for i in range(100):
            if i%2==0:
                try:
                    y=input("X's turn: ")
                    if y=='fail':
                        return
                    p1(y)
                    if ((board[0]==board[2]==board[4]=='X')or(board[6]==board[8]==board[10]=='X')or(board[12]==board[14]==board[16]=='X')or(board[0]==board[6]==board[12]=='X')or(board[2]==board[8]==board[14]=='X')or(board[4]==board[10]==board[16]=='X')or(board[0]==board[8]==board[16]=='X')or(board[12]==board[8]==board[4]=='X')):
                        print('Player 1(X) WON!!!!')
                        resetboard()
                        return
                    elif '-' not in board:
                        print('DRAW!!i Am ThE bEsT aT tIC TaC tOe')
                        resetboard()
                        return
                except:
                    continue
            else:
                try:
                    y=input("O's turn: ")
                    p2(y)
                    if ((board[0]==board[2]==board[4]=='O')or(board[6]==board[8]==board[10]=='O')or(board[12]==board[14]==board[16]=='O')or(board[0]==board[6]==board[12]=='O')or(board[2]==board[8]==board[14]=='O')or(board[4]==board[10]==board[16]=='O')or(board[0]==board[8]==board[16]=='O')or(board[12]==board[8]==board[4]=='O')):
                        print('Player 2(O) WON!!!')
                        resetboard()
                        return
                    elif '-' not in board:
                        print('DRAW!!i Am ThE bEsT aT tIC TaC tOe')
                        resetboard()
                        return
                except:
                    continue
    elif x=='1':
        print(board)
        for i in range(100):
            if i%2==0:
                try:
                    y=input("X's turn: ")
                    p1(y)
                    if ((board[0]==board[2]==board[4]=='X')or(board[6]==board[8]==board[10]=='X')or(board[12]==board[14]==board[16]=='X')or(board[0]==board[6]==board[12]=='X')or(board[2]==board[8]==board[14]=='X')or(board[4]==board[10]==board[16]=='X')or(board[0]==board[8]==board[16]=='X')or(board[12]==board[8]==board[4]=='X')):
                        print('Player 1(X) WON!!!!')
                        resetboard()
                        return
                    elif '-' not in board:
                        print('DRAW!!i Am ThE bEsT aT tIC TaC tOe')
                        resetboard()
                        return
                except:
                    continue
            else:
                try:
                    bot()
                    if ((board[0]==board[2]==board[4]=='O')or(board[6]==board[8]==board[10]=='O')or(board[12]==board[14]==board[16]=='O')or(board[0]==board[6]==board[12]=='O')or(board[2]==board[8]==board[14]=='O')or(board[4]==board[10]==board[16]=='O')or(board[0]==board[8]==board[16]=='O')or(board[12]==board[8]==board[4]=='O')):
                        print('Player 2(O) WON!!!  HAHAHAH YOU LOST to a BOT')
                        resetboard()
                        return
                    elif '-' not in board:
                        print('DRAW!!i Am ThE bEsT aT tIC TaC tOe')
                        resetboard()
                        return
                except:
                    continue

def p1(p):
    global board
    b=list(board)
    ind=d[p]
    if b[ind]=='-':
        del b[ind]
        b.insert(ind,'X')
    board=''.join(b)
    print(board+'\n')
    return board
def p2(p):
    global board
    b=list(board)
    ind=d[p]
    if b[ind]=='-':
        del b[ind]
        b.insert(ind,'O')
    board=''.join(b)
    print(board+'\n')
    return board
def bot():
    global board
    y=random.randrange(0,17,2)
    b=list(board)
    if b[y]=='-':
        del b[y]
        b.insert(y,'O')
    elif '-' in board:
        while b[y]!='-':
            y=random.randrange(0,17,2)
    del b[y]
    b.insert(y,'O')
    board=''.join(b)
    print(board+'\n')
    return board
def resetboard():
    global board
    board='-|-|-\n-|-|-\n-|-|-'
    return board
print()
t()
    
