'''
Name: Lai Minh Thong
Student ID: 20127635
Propositional logic resolution - Inference Rule Implementation
'''

INPUT_FOLDER = 'Input data'
OUTPUT_FOLDER = 'Output data'

# Read inputfiles
def readFile(filename):
    f = open(filename, "r")
    alpha = f.readline().strip().splitlines() # read clause in query alpha

    num_KB = int(*f.readline().strip().splitlines()) # read number of clauses KB
    KB = [clause.strip().split(' OR ') for clause in f.read().splitlines()] # remove character 'OR'
    return alpha, KB

# Write generated data to outputfiles 
def writeFile(filename, Data):
    Data = stdizeData(Data) # standardize Data before write to file

    f = open(filename, "w")
    for clause in Data:
        f.writelines(clause)

    f.close()

# Standardize Data before write to file
def stdizeData(Data):
    for clause in Data:
        i = 1
        for j in range(len(clause)-1):
            clause.insert(i, ' OR ')
            i += 2
        clause.append('\n')
    Data[-1].pop(-1)

    return Data

# Negate form of a statement
def negate(s):
    new_list = []
    s = [str(i) for i in s]
    res = str("".join(s))  
    if res[0] == '-': negate = res[1]
    elif res[0] != '-': negate = '-' + res[0] 
    new_list.append(negate)
    return new_list

# Propositional logic resolution inference rule
def PL_Resolution(KB, alpha):
    """ Negate the alpha clauses to add it into KB """
    not_alpha = negate(alpha)

    """ Add KB AND NOT alpha into KB """
    clauses = (KB + [not_alpha])

    generatedData = []
    while True:
        new_clauses = []
        can_entail = False

        clauses_pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i+1,len(clauses))]

        for pair in clauses_pairs:
            resolvents = PL_Resolve(*pair)
            
            if resolvents == False:
                continue
            elif len(resolvents) == 0:
                can_entail = True
                new_clauses.append(['{}'])
                break
            else:
                if resolvents not in (clauses + new_clauses):
                    new_clauses.append(resolvents)

        generatedData.append([str(len(new_clauses))])
        generatedData.extend(new_clauses)

        if can_entail:
            generatedData.append(['YES'])
            return can_entail, generatedData
        elif len(new_clauses) == 0:
            generatedData.append(['NO'])
            return can_entail, generatedData

        clauses.extend(new_clauses)

def PL_Resolve(ci, cj):
    new_clause = ci + cj # merge pair of clauses Ci, Cj in clauses
    new_clause.sort(key=lambda kv:kv[-1]) # sort by alphabet before resolving
    resolvedNum = 0

    for x in ci:
        for y in cj:
            if x == y: new_clause.remove(x) # Reduce the same elements 
            
            elif x == str(*negate(y)): # Resolving 2 Sentences are having complementary literals
                new_clause.remove(x)
                new_clause.remove(y)
                resolvedNum += 1

            # Else if clause is empty, return an empty clause
            elif len(new_clause) == 0:
                break
    
    if resolvedNum == 1:
        return new_clause
    return False
    

def main():
    # Run all 9 test cases
    for idx in range(9):
        readFileName = (INPUT_FOLDER + "/input") + str(idx + 1) + ".txt"
        writeFileName = (OUTPUT_FOLDER + "/output") + str(idx + 1) + ".txt"

        alpha, KB = readFile(readFileName)
        isEntailable, DataClauses = PL_Resolution(KB, alpha)
        writeFile(writeFileName, DataClauses)

if __name__ == '__main__':
    main()