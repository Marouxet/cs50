from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Game Rules
    Or(AKnight, AKnave), # A should be one of those
    Or(And(AKnight,Not(AKnave)),And(AKnave,Not(AKnight))), # A can not be both

    # Sentence: A says And(AKnight,AKnave), so:
    #if A is a Knave, so his sentence And(AKnight,AKnave) should be false
    #if A is a Knigth, so his sentence And(AKnight,AKnave) should be true

    Or( And(Not(And(AKnight,AKnave)),AKnave), And((And(AKnight,AKnave)),AKnight) ) 

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
# Game Rules
    Or(AKnight, AKnave), # A should be one of those
    Or(BKnight, BKnave), # B should be one of those
    Or(And(AKnight,Not(AKnave)),And(AKnave,Not(AKnight))), # A can not be both
    Or(And(BKnight,Not(BKnave)),And(BKnave,Not(BKnight))), # B can not be both

    # Sentence: A says And(AKnave,BKnave), so:
    # If A is a Knight, the sentence should be true or if A is a Knave, the sentence should be false
    Or(And(And(AKnave,BKnave),AKnight),
    And(Not(And(AKnave,BKnave)),AKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
   # Game Rules
    Or(AKnight, AKnave), # A should be one of those
    Or(BKnight, BKnave), # B should be one of those
    Or(And(AKnight,Not(AKnave)),And(AKnave,Not(AKnight))), # A can not be both
    Or(And(BKnight,Not(BKnave)),And(BKnave,Not(BKnight))), # B can not be both

   # Sentences 

   # A says  Or(And(AKnave,BKnave),And(AKnight,BKnight)) - The same type
   # B says  Or(And(AKnave,BKnight),And(AKnight,BKnave)) - The different type

   # If A is KNight, the sentence is true. If A is a KNave, the sentence is false 
   # If B is KNight, the sentence is true. If B is a KNave, the sentence is false 

    Or(
       And(Or(And(AKnave,BKnave),And(AKnight,BKnight)), AKnight),

       And(Not(Or(And(AKnave,BKnave),And(AKnight,BKnight))), AKnave)
       
       ),

    Or(
       And(Or(And(AKnave,BKnight),And(AKnight,BKnave)), BKnight),

       And(Not(Or(And(AKnave,BKnight),And(AKnight,BKnave))), BKnave)
       
       )

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    # Game Rules
    Or(AKnight, AKnave), # A should be one of those
    Or(BKnight, BKnave), # B should be one of those
    Or(CKnight, CKnave), # C should be one of those

    Or(And(AKnight,Not(AKnave)),And(AKnave,Not(AKnight))), # A can not be both
    Or(And(BKnight,Not(BKnave)),And(BKnave,Not(BKnight))), # B can not be both
    Or(And(CKnight,Not(CKnave)),And(CKnave,Not(CKnight))), # B can not be both

    # C says "A is a knight" -> If C is a knight, that is true, if C is a Knave, that is false

    Or(
        And(AKnight,CKnight),
        And(Not(AKnight),CKnave)
    ),    

    # B says "C is a knave" -> If B is a knigth, that's true, if B is a knave, that is false

    Or(
        And(CKnave,BKnight),
        And(Not(CKnave),BKnave)
    ), 

    # B says "A said 'I am a knave'." There are four options. B and A could be lying or not

    Or(And(BKnight,(Or(

            And(AKnight,AKnave),
            And(AKnave,Not(AKnave))
    ))),
       And(BKnave,Not(Or(

            And(AKnight,AKnave),
            And(AKnave,Not(AKnave))

       )))
        
    ) 

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
