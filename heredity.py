import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.
    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    prob = []
    # Prob of a parent to give a gene to its child
    zero2zero = (1-PROBS["mutation"])
    zero2one = PROBS["mutation"]
    one2one = 0.5
    one2zero = 0.5
    two2zero = PROBS["mutation"]
    two2one = 1- PROBS["mutation"]
    
    for person, att in people.items():
        

        if person in one_gene:
            gene = 1
        elif person in two_genes:
            gene = 2
        else:
            gene = 0    
        if person in have_trait:
            trait = True
        else:
            trait = False
        

        if att["mother"] == None: # No hay madre padre -> probabilidad directa
            mother = None
            father = None

        elif att["mother"] in one_gene:
            mother = 1
            if att["father"] in one_gene:
                father = 1
            elif att["father"] in two_genes:
                father = 2
            else:
                father = 0
        elif att["mother"] in two_genes:
            mother = 2
            if att["father"] in one_gene:
                father = 1
            elif att["father"] in two_genes:
                father = 2
            else:
                father = 0
        else:
            mother = 0
            if att["father"] in one_gene:
                father = 1
            elif att["father"] in two_genes:
                father = 2
            else:
                father = 0

        # Opciones convinatorias
        if mother == None:
            prob.append((PROBS["gene"][gene]*PROBS["trait"][gene][trait]))

        elif gene == 0 and mother == 0 and father == 0:
            prob.append(zero2zero*zero2zero * PROBS["trait"][gene][trait])
        elif gene == 0 and mother == 1 and father == 0:
            prob.append((one2zero*zero2zero) * PROBS["trait"][gene][trait])
        elif gene == 0 and mother == 0 and father == 1:
            prob.append( (one2zero*zero2zero) * PROBS["trait"][gene][trait])
        elif gene == 0 and mother == 1 and father == 1:
            prob.append(one2zero*one2zero* PROBS["trait"][gene][trait])
        elif gene == 0 and mother == 2 and father == 0:
            prob.append(two2zero*zero2zero * PROBS["trait"][gene][trait])
        elif gene == 0 and mother == 0 and father == 2:
            prob.append(two2zero*zero2zero * PROBS["trait"][gene][trait])
        elif gene == 0 and mother == 2 and father == 2:
            prob.append(two2zero*two2zero * PROBS["trait"][gene][trait])
        elif gene == 0 and mother == 2 and father == 1:
            prob.append(two2zero*one2zero* PROBS["trait"][gene][trait])
        elif gene == 0 and mother == 1 and father == 2:
            prob.append(two2zero*one2zero * PROBS["trait"][gene][trait])
        
        elif gene == 1 and mother == 0 and father == 0:
            prob.append((zero2one*zero2zero*2) * PROBS["trait"][gene][trait])
        elif gene == 1 and mother == 1 and father == 0:
           prob.append((one2one*zero2zero+one2zero*zero2one) * PROBS["trait"][gene][trait])
        elif gene == 1 and mother == 0 and father == 1:
            prob.append((one2one*zero2zero+one2zero*zero2one)* PROBS["trait"][gene][trait])
        elif gene == 1 and mother == 1 and father == 1:
            prob.append((one2one*one2zero*2)* PROBS["trait"][gene][trait])
        elif gene == 1 and mother == 2 and father == 0:
           prob.append( (two2one*zero2zero+two2zero*zero2one) * PROBS["trait"][gene][trait])
        elif gene == 1 and mother == 0 and father == 2:
            prob.append((two2one*zero2zero+two2zero*zero2one) * PROBS["trait"][gene][trait])
        elif gene == 1 and mother == 2 and father == 2:
            prob.append((two2zero*two2one*2) * PROBS["trait"][gene][trait])
        elif gene == 1 and mother == 2 and father == 1:
            prob.append((two2zero*one2one+two2one*one2zero)* PROBS["trait"][gene][trait]) 
        elif gene == 1 and mother == 1 and father == 2:
            prob.append((two2zero*one2one+two2one*one2zero)* PROBS["trait"][gene][trait])
        
        elif gene == 2 and mother == 0 and father == 0:
            prob.append(zero2one*zero2one* PROBS["trait"][gene][trait])
        elif gene == 2 and mother == 1 and father == 0:
            prob.append(one2one*zero2one * PROBS["trait"][gene][trait])
        elif gene == 2 and mother == 0 and father == 1:
            prob.append(one2one*zero2one * PROBS["trait"][gene][trait])
        elif gene == 2 and mother == 1 and father == 1:
            prob.append(one2one*one2one * PROBS["trait"][gene][trait])   
        elif gene == 2 and mother == 2 and father == 0:
            prob.append(two2one*zero2one * PROBS["trait"][gene][trait])
        elif gene == 2 and mother == 0 and father == 2:
           prob.append(two2one*zero2one * PROBS["trait"][gene][trait])      
        elif gene == 2 and mother == 2 and father == 2:
            prob.append(two2one*two2one* PROBS["trait"][gene][trait])
        elif gene == 2 and mother == 2 and father == 1:
            prob.append(two2one*one2one* PROBS["trait"][gene][trait])
        elif gene == 2 and mother == 1 and father == 2:
            prob.append(two2one*one2one * PROBS["trait"][gene][trait])
        

    x = 1
    for probs in prob:
        x = x * probs
    return x
    


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.

    Youtube minuto 1:09:49
    Las probabilidades que se obtienen son para:
    - have_trait y not have_trait -> evidencia
    - one gene / two genes / zero genes -> hidden variables
    - X no se bien cual es.

    La idea es que estamos calculando las join probabilities para todas las opciones posibles de 
    la variable oculta (por eso hace el for en main). 
    En cada update, debemos sumar las probabilidades teniendo en cuenta
    cuales de las variables cambia.
    
    Recall from lecture that we can calculate a conditional probability by summing up 
    all of the joint probabilities that satisfy the evidence, 
    and then normalize those probabilities so that they each sum to 1.

    """
    
    for person in probabilities.keys():
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():
        for att in probabilities[person].keys():
            norma = sum(list(probabilities[person][att].values()))
            for x,y in probabilities[person][att].items():
                probabilities[person][att][x] = y/norma
    dic_prob = probabilities          
    

if __name__ == "__main__":
    main()
