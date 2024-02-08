#realisé par
# ABED Nada fatima zohra
# REBAI Mohamed Younes

import matplotlib.pyplot as plt
import networkx as nx

def read_graph(path: str):
    A = []
    R = []
    with  open(path) as myfile:
        for line in myfile:
            if "arg" in line:
                debut_parenthese = line.find('(')
                fin_parenthese = line.find(')')
                A.append(line[debut_parenthese + 1: fin_parenthese])
            if "att" in line:
                debut_parenthese = line.find('(')
                fin_parenthese = line.find(')')
                X = line[debut_parenthese + 1: fin_parenthese].split(',')
                R.append(tuple(X))
    return A, R


def draw_graph(A, R):
    # Create a directed graph
    G = nx.DiGraph()

    G.add_nodes_from(A)

    G.add_edges_from(R)

    pos = nx.circular_layout(G)

    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_color="black",
            font_weight="bold", arrowsize=20)

    plt.show()

"""# **Etape 2: définir les fonctions de base**

* Conflict free
"""

from itertools import chain, combinations


from itertools import chain, combinations

def powerset(s):

    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def get_attacked(arg1,arg2,attacks): #get attacked by arg1 and remove arg2
    attacked_all = []
    for attack in attacks:
      attacker, attacked = attack
      if arg1 == attacker and attacked != arg2 :
        attacked_all.append(attacked)
    return attacked_all

def get_attackers(arg1,attacks): #get attackers of arg1
    attackers = []
    for attack in attacks:
      attacker, attacked = attack
      if arg1 == attacked :
        attackers.append(attacker)
    return attackers

def is_complete_extension(candidate_set, arguments, attacks):
    # Check if the set is conflict-free and defense-free

    if len(candidate_set)==0:
        return True
    elif len(candidate_set)==1:
        #no need to check conflict-free just check teh defense free
        arg = candidate_set[0]
        attackers = []
        #get all the the attackers of arg
        for attack in attacks:
            attacker, attacked = attack
            if arg == attacked:
                attackers.append(attacker)
        attacked_all = []
       #get all the attacked by arg
        for attack in attacks:
            attacker, attacked = attack
            if arg == attacker:
                attacked_all.append(attacked)
        if attacked_all != attackers : # check if he is protected completely by himself
            return False
        else: # check if he completely protectes smth outside of it self ---- if yes eliminated
            for attcked in attacked_all :
              for attacked1 in get_attacked(attcked,arg,attacks): # get the args attacked by the ones attacked by arg
                  if set(get_attackers(attacked1,attacks)).issubset(set(attacked_all)):
                    return False
            return True
    else:
        return all(
            (a1, a2) not in attacks for a1 in candidate_set for a2 in candidate_set if a1 != a2
        ) and all(
            any((attacker, arg) in attacks for attacker in candidate_set if attacker != arg) or arg in candidate_set
            for arg in arguments
        )


def find_complete_extensions01(arguments, attacks):
    complete_extensions = []

    # Generate all possible subsets of arguments
    all_subsets = list(powerset(arguments))
    for subset in all_subsets:
        # Check if the subset is a complete extension
        if is_complete_extension(subset, arguments, attacks):
            complete_extensions.append(set(subset))

    return complete_extensions
def is_cred(arg, complete_set):
    answer = ''
    if any(arg in ext for ext in complete_set):
        answer = "YES"
    else:
        answer = "NO"
    return answer


def is_skep(arg, complete_set):
    answer = ''
    if all(arg in ext for ext in complete_set):
        answer = "YES"
    else:
        answer = "NO"
    return answer


from itertools import chain, combinations


def powerset(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


def is_conflict_free(subset, attacks):
    for arg1 in subset:
        for arg2 in subset:
            if arg1 != arg2 and (arg1, arg2) in attacks:
                return False
    return True


def attacks_all_remaining(subset, remaining_args, attacks):
    dictionary = {element: False for element in remaining_args}
    for arg in subset:
        for argg in remaining_args:
            if (arg, argg) in attacks:
                dictionary[argg] = True
    return all(value for value in dictionary.values())


def find_stable_extension(arguments, attacks):
    all_subsets = powerset(arguments)
    result = []

    for subset in all_subsets:

        remaining_args = set(arguments) - set(subset)

        if is_conflict_free(subset, attacks) and attacks_all_remaining(subset, remaining_args, attacks):
            result.append(list(subset))

    return result


"""# **Etape 3: main**

1.   Task 1
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description="Argumentation Framework Analyzer")
    parser.add_argument("-p", choices=['VE-CO', 'VE-ST', 'DC-CO', 'DS-CO', 'DC-ST', 'DS-ST'],
                        help="Specify the type of analysis to perform", required=True)
    parser.add_argument("-f", help="Path to the text file describing the Argumentation Framework", required=True)
    parser.add_argument("-a", help="List of arguments in the query set S or the query argument", required=True)

    args = parser.parse_args()

    # Read the Argumentation Framework from the file
    arguments, attacks = read_graph(args.f)
    draw_graph(arguments, attacks)

    # Perform the appropriate analysis based on the specified command
    if args.p.startswith('VE-CO'):
        query_set = args.a.split(',')
        if query_set =="vide":
            sett = set()
            result = "YES" if sett in find_complete_extensions01(arguments, attacks) else "NO"
            print(result)
        else:
            result = "YES" if set(query_set) in find_complete_extensions01(arguments, attacks) else "NO"
            print(result)


    elif args.p.startswith('VE-ST'):
        query_set = args.a.split(',')
        if set(query_set) in (set(lst) for lst in find_stable_extension(arguments, attacks)):
            result = "YES"
        else:
            result = "NO"
        print(result)


    elif args.p.startswith('DC-ST'):
        query_argument = args.a
        Stable = find_stable_extension(arguments, attacks)
        print(is_cred(query_argument, Stable))
    elif args.p.startswith('DS-ST'):
        query_argument = args.a
        Stable = find_stable_extension(arguments, attacks)
        print(is_skep(query_argument, Stable))
    elif args.p.startswith('DC-CO'):
        query_argument = args.a
        result = find_complete_extensions01(arguments, attacks)
        print(is_cred(query_argument, result))
    elif args.p.startswith('DS-CO'):
        query_argument = args.a
        result = find_complete_extensions01(arguments, attacks)
        print(is_skep(query_argument, result))
    else:
        print("Invalid command")


if __name__ == "__main__":
    main()

    #python main.py -p VE-CO -f Files\test_af1.apx -a B,D