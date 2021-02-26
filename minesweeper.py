import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()
        

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()
        

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if cell in self.cells: # First check if cell in sentence
            self.cells.remove(cell) # Remove cell from sentence
            self.count -= 1 # There is one mine less in sentence 
            #print(cell)
        

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells: # First check if cell in sentence
            self.cells.remove(cell) # Remove cell from sentence
            #print(cell)

        


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge.copy():
            sentence.mark_safe(cell)
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made

            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        #1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        #2) mark the cell as safe
        # Update all sentences in knowledge, now this cell is know to be safe
        self.mark_safe(cell)
        # 3) New sentence: set of cells around current cell and count of mines
        fullSentence = self.agregarCeldas(cell)
        # Verifico cantidad de celdas en la sentencia que ya se sabe que son minas
        minas = len(list(itertools.takewhile(lambda i:i in self.mines, fullSentence)))
        # Resto la(s) mina(s) ya conocida(s) en count
        count = count - minas
        # Quito del set las celdas que ya sé que son minas.
        cleanSentence = set(itertools.dropwhile(lambda i:i in self.mines, fullSentence))
        # Elimino del set las celdas que ya sé que están a salvo
        cleanSentence = set(itertools.dropwhile(lambda i:i in self.safes, cleanSentence))
        # Agrego la sentencia limpia al conocimiento base
        self.knowledge.append(Sentence(cleanSentence,count))

        '''
        If, based on any of the sentences in self.knowledge, 
        new cells can be marked as safe or as mines, then the function should do so.
        If, based on any of the sentences in self.knowledge, 
        new sentences can be inferred (using the subset method described in the Background),
        then those sentences should be added to the knowledge base as well.

        
        Para cada sentencia individual (ahora actualizadas)
        Verificar: 
        1)ejecutar known_mines
        Dentro de known mines: si len(set) = count -> todas son minas
        Para cada celda hacer el markMine, que vuelve a modificr todos 
        las sentencias en la base
        2) ejecutar known_safes
        Dentro de known_safes: si count == 0 -> todas a salvo
        Para cada celda hacer el markSafe, que modifica los registros


        Para cada una de las permutaciones (o combinaciones, ver que conviene) entre las sentencias
        de la base de datos, verificar si algún set está incluido en otro set. De ser así, generar 
        una nueva sentencia set2 - set1 = count2 - count1

        Si se generó una nueva secuencia, repetir 1 2 3 en loop.

        '''
        cambios = True
        while cambios:
            cambios = False
            for sentence in self.knowledge:
                nuevasMinas = sentence.known_mines()
                if len(nuevasMinas) != 0:
                    for mina in nuevasMinas.copy():
                        self.mark_mine(mina)
                        cambios = True
                else:
                    nuevasSalvo = sentence.known_safes()
                    if len(nuevasSalvo) != 0:
                        for safe in nuevasSalvo.copy():
                                self.mark_safe(safe)
                                cambios = True
             

            # Limpiar Sentence vacíos
            for i in self.knowledge.copy():
                if len(i.cells)== 0:
                    self.knowledge.remove(i)
                
            if len(self.knowledge)>1:               
                for i in list(itertools.permutations(self.knowledge.copy())):
                    if i[0].cells.issubset(i[1].cells):
                        #print(i[0].cells)
                       # print(i[1].cells)
                        self.knowledge.append(Sentence(i[1].cells.difference(i[0].cells),i[1].count-i[0].count))
                        #print(i[1].cells.difference(i[0].cells))
                        self.knowledge.remove(Sentence(i[1].cells, i[1].count))
                        cambios = True
                        break
                    #print(self.knowledge)
    def agregarCeldas(self,celda):
        
        celdas = set()
        if celda[0] == self.width-1:
            x = [celda[0]-1,celda[0]]
        elif celda[0] == 0:
            x = [celda[0],celda[0]+1]
        else:
            x = [celda[0]-1, celda[0],celda[0]+1]

        if celda[1] == self.height-1:
            y = [celda[1]-1,celda[1]]
        elif celda[1] == 0:
            y = [celda[1],celda[1]+1]
        else:
            y = [celda[1]-1, celda[1],celda[1]+1]

        for xx in x:
            for yy in y:
                a = (xx,yy)
                if a != celda:
                    celdas.add(a)
        
        return celdas

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.

        Retornarnar algun tupla que esté en safe y no esté en yausados
        Si no hay, None
        """
        if len(list(self.safes.difference(self.moves_made))) == 0:
            return None
        else:
            #print(list(self.safes.difference(self.moves_made))[0])
            #time.sleep(1)
            return list(self.safes.difference(self.moves_made))[0]

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        todo = set()
        for i in range(self.height):
            for j in range(self.width):
                todo.add((i,j))
        todo = todo.difference(self.mines)
        todo = todo.difference(self.moves_made)
        if len(todo) == 0:
            return None
        else:
            x = todo.pop()
            ##print(x)
            #time.sleep(1)
            return x

