import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        def verifyLength(string, length):
            if len(string) != length:
                return string
          

        for variable,domain in self.domains.items():
            keys2delete = map(verifyLength,domain,[variable.length for x in range(len(domain))])
            for key in list(keys2delete):
                if key is not None:
                    self.domains[variable].remove(key)
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revition = False
        overlap = self.crossword.overlaps[(x,y)]
        if overlap == None:
            return revition
        else:
            for palabrax in self.domains[x].copy():
                match = False
                for palabray in self.domains[y]:
                    match = match or ( (palabrax[overlap[0]] == palabray[overlap[1]]) and (palabrax != palabray) )
                if not match:
                    self.domains[x].remove(palabrax)
                    revition = True
                
            return revition
                

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            queue = set()
            for arc , overlap in self.crossword.overlaps.items():
                if overlap != None:
                    queue.add(arc)
            while not (len(queue) == 0):
                arc = queue.pop()
                X = arc[0]
                Y = arc[1]
                revision = self.revise(X,Y)
                if revision:
                    if len(self.domains[X])==0:
                        return False
                for neigbor in self.crossword.neighbors(X):
                    if neigbor != Y:
                        queue.add((neigbor,X)) 
            return True 
        
        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True
 
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        if len(assignment)== 1:
            return True
        for variable1 in assignment:
            copy = assignment.copy()
            copy.pop(variable1)
            for variable2 in copy:
                if assignment[variable1] == assignment[variable2]:
                    return False
                cruce= self.crossword.overlaps[(variable1,variable2)]
                if cruce is not None:
                    x = cruce[0]
                    y = cruce [1]
                    if assignment[variable1][x] != assignment[variable2][y]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        def costo(list1, list2):
            costo = []
            for caracter in list1:
                costo.append(sum(map(lambda x: x == caracter, list2)))

            return costo
            

        cost= [0 for x in self.domains[var]]

        for vecino in self.crossword.neighbors(var):
            cruce = self.crossword.overlaps[(var,vecino)]
            caracter = [x[cruce[0]] for x in self.domains[var]]
            caracter2 = [x[cruce[1]] for x in self.domains[vecino]]
            cost2 = costo(caracter,caracter2)
            cost = [sum(x) for x in zip(cost, cost2)]   
            
        return [x for _,x in sorted(zip(cost2,self.domains[var]))]

        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        remaining = 1e10 
        degree = 0
        
        var = None
        for variable in self.crossword.variables:
            if variable not in assignment:
                if len(self.domains[variable]) < remaining:
                    remaining = len(self.domains[variable])
                    var = variable
                elif len(self.domains[variable]) == remaining:
                    if len(self.crossword.neighbors(variable)) > degree:
                        degree = len(self.crossword.neighbors(variable))
                        var = variable
        return var        
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        #for value in self.domains[var]:
        for value in self.order_domain_values(var, assignment):
            copyofass = assignment.copy()
            copyofass.update({var:value})
            consistency = self.consistent(copyofass)
            if consistency:
                assignment.update({var:value})
                #assignment.update({var:value})
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                else:
                    assignment.pop(var)
        return None

        
        
       


def main():

    ## Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None



    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
