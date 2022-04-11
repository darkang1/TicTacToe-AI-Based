class TicTacToe:
    def choosePlayerLetter(self):
        # Function to let the player choose which letter he wants to play
        letter=''
        while not(letter=='X' or letter=='O'):
            print("Do you want play as 'X' or 'O'?")
            letter = input('> ').upper()
            
        # Returns a list with the player's letter as the first item, and the computer's letter as the second
        if letter == 'X':
            return ['X','O']
        else:
            return ['O','X']

    def whoGoesFirst(self):
        # Function to let the player decide who goes first
        print("Do you want to go first? ('y' or 'n')")
        userInput = input('> ')
        
        if userInput.lower().startswith('y'):
            return 'player'
        elif userInput.lower().startswith('n'):
            return 'computer'
        else:
            print('Whatever')
            return 'computer'

    def drawBoard(self, board):
        # Function to print out the board that with passed arguments
        # 'board' is a list of 10 strings representing the board (ignoring index 0)
        print('\n| ' + board[1] + ' | ' + board[2] + ' | ' + board[3] + ' |')
        print('----+---+----')
        print('| ' + board[4] + ' | ' + board[5] + ' | ' + board[6] + ' |')
        print('----+---+----')
        print('| ' + board[7] + ' | ' + board[8] + ' | ' + board[9] + ' |\n')

    def getPlayerMove(self, board):
        # Function to get the player's move input
        move = '-1'
        while move not in '1 2 3 4 5 6 7 8 9'.split() or not self.isSpaceAvailable(board,int(move)):
            print('Input your next move [1-9]')
            move = input('> ')
            
            if move not in '1 2 3 4 5 6 7 8 9'.split():
                print('Invalid input! Try again.')
            elif not self.isSpaceAvailable(board,int(move)):
                print('Selected space is already taken! Try again.')
            
        return int(move)

    def findBestAIMove(self, board, computerLetter):
        # Function for AI to decide which empty space would be a best next move
        bestVal = -1000
        bestMove = -1
        
        for i in range(1,10):
            if self.isSpaceAvailable(board, i):
                board[i] = computerLetter
                moveVal = self.minmax(board, 0, False, -1000, 1000, computerLetter)
                board[i] = ' '

                if moveVal > bestVal:
                    bestMove = i
                    bestVal = moveVal

        return bestMove

    def minmax(self, board, depth, isMax, alpha, beta, computerLetter):
        # 2-in-1 function which performs either maximizing or minimizing
        # Verifying who playing which letter to properly fill the board from computer
        if computerLetter == 'X':
            playerLetter = 'O'
        else:
            playerLetter = 'X'
        
        # Verifying for winning conditions
        if self.isWinner(board, computerLetter):
            return 100
        if self.isWinner(board, playerLetter):
            return -100
        if self.isBoardFull(board):
            return 0
        
        # Checking if our function should work as maximizer or minimizer
        if isMax:
            bestVal = -1000

            for i in range(1,10):
                if self.isSpaceAvailable(board, i):
                    board[i] = computerLetter
                    bestVal = max(bestVal, self.minmax(board, depth+1, not isMax, alpha, beta, computerLetter) - depth)
                    alpha = max(alpha, bestVal)
                    board[i] = ' '

                    if alpha >= beta:
                        break

            return bestVal
        else:
            bestVal = 1000

            for i in range(1,10):
                if self.isSpaceAvailable(board, i):
                    board[i] = playerLetter
                    bestVal = min(bestVal, self.minmax(board, depth+1, not isMax, alpha, beta, computerLetter) + depth)
                    beta = min(beta, bestVal)
                    board[i] = ' '

                    if alpha >= beta:
                        break

            return bestVal

    def makeMove(self, board, letter, move):
        board[move] = letter

    def isSpaceAvailable(self, board, move):
        return board[move] == ' '

    def isWinner(self, board, letter):
        # Function to verify whether player with passed letter as argument has won or not. If yes, returns True
        return ((board[1]==letter and board[2]==letter and board[3]==letter) or
                (board[4]==letter and board[5]==letter and board[6]==letter) or
                (board[7]==letter and board[8]==letter and board[9]==letter) or
                (board[1]==letter and board[4]==letter and board[7]==letter) or
                (board[2]==letter and board[5]==letter and board[8]==letter) or
                (board[3]==letter and board[6]==letter and board[9]==letter) or
                (board[1]==letter and board[5]==letter and board[9]==letter) or
                (board[3]==letter and board[5]==letter and board[7]==letter))

    def isBoardFull(self, board):
        # Function to verify whether every space on the board has been taken. If yes, returns True
        for i in range(1,10):
            if self.isSpaceAvailable(board, i):
                return False
        return True

    def playAgain(self):
        # Function to verify whether user wants to play again. If yes, returns True
        print("Do you want to play again? ('y' or 'n')")
        return input('> ').lower().startswith('y')

    def play(self):
        # Game initialization function
        print('Welcome to Tic-Tac-Toe!')
        print('Board input numbering reference:')
        self.drawBoard('0 1 2 3 4 5 6 7 8 9'.split())
        print('')

        while True:
            # Resetting the board
            theBoard = [' '] * 10
            playerLetter, computerLetter = self.choosePlayerLetter()
            turn = self.whoGoesFirst()
            print('The ' + turn + ' will go first!')
            gameIsRunning = True

            while gameIsRunning:
                if turn == 'player':
                    self.drawBoard(theBoard)
                    move = self.getPlayerMove(theBoard)
                    self.makeMove(theBoard, playerLetter, move)

                    if self.isWinner(theBoard, playerLetter):
                        self.drawBoard(theBoard)
                        print('You are the winner!')
                        gameIsRunning = False
                    else:
                        if self.isBoardFull(theBoard):
                            self.drawBoard(theBoard)
                            print('The game is a tie!')
                            break
                        else:
                            turn = 'computer'
                else:
                    move = self.findBestAIMove(theBoard, computerLetter)
                    self.makeMove(theBoard, computerLetter, move)

                    if self.isWinner(theBoard, computerLetter):
                        self.drawBoard(theBoard)
                        print('You lost the game!')
                        gameIsRunning = False
                    else:
                        if self.isBoardFull(theBoard):
                            self.drawBoard(theBoard)
                            print('The game is a tie!')
                            break
                        else:
                            turn = 'player'
                            
            if not self.playAgain():
                exit()
                
            print('\n|====New Game====|')

if __name__ == "__main__":
    game = TicTacToe()
    game.play()