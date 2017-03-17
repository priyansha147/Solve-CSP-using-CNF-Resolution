import copy

def get_value(literal):
    if literal[0] == "~":
        return literal[1:], False
    else:
        return literal, True

def find_assignment(clause, model):
    P, value = None, None
    for literal in clause:
        l, v = get_value(literal)
        if l in model:
            if model[l] == v:
                return None, None  # clause already True
        elif P:
            return None, None  # more than 1 unbound variable
        else:
            P, value = l, v
    return P, value

#This function finds unit clause if it exists
def get_unitClause(cnf, model):
    for clause in cnf:
        P, value = find_assignment(clause, model)
        if P:
            return P, value
    return None, None

def buildModel(model, P, value):
    modelcopy = copy.copy(model)
    if P[0] != "~":
        modelcopy[P] = value
    return modelcopy

def removeAll(P, symbols):
    symbolscopy = copy.copy(symbols)
    del symbolscopy[symbolscopy.index(P)]
    return symbolscopy

#This function finds finds if complement of the passed literal is present in the clauses
def find_complement(s, clauses):
    if s[0] == "~":
        compl = s[1:]
        flag = False
    else:
        compl = "~" + s
        flag = True

    for c in clauses:
        if compl in c:
            return True, flag
    return False, flag

#This function finds a pure symbol if it exists
def get_pureSymbol(symbols, clauses):
    for s in symbols:
        for c in clauses:
            if s in c:
                res, val = find_complement(s, clauses)
                if res == False:
                    return s, val
            if "~" + s in c:
                res, val = find_complement("~" + s, clauses)
                if res == False:
                    return s, val

    return None, None

#This function finds if the passed clause is true, false or unknown
def is_true(clause, model = {}):
    if not model:
        return None

    flag = 0
    for literal in clause:
        if literal[0] == "~":
            compl = literal[1:]
        else:
            compl = "~" + literal
        if literal in model:
            if model[literal] == True:
                return True
            else:
                flag += 1
        elif literal not in model:
            if compl in model:
                if model[compl] == False:
                    return True
                else:
                    flag += 1
            else:
                continue

    if flag == len(clause):
        return False
    else:
        return None

#This function finds if the cnf is satisfiable or not; if yes - returns one solution
def dpll(cnf, symbols, model):
    unknown_clauses = []
    for c in cnf:
        val = is_true(c, model)
        if val is False:
            return False
        if val is not True:
            unknown_clauses.append(c)
    if not unknown_clauses:
        return model
    #Calling Pure Symbols
    P, value = get_pureSymbol(symbols, unknown_clauses)
    if P:
        return dpll(cnf, removeAll(P, symbols), buildModel(model, P, value))
    #Calling Unit Clause
    P, value = get_unitClause(cnf, model)
    if P:
        return dpll(cnf, removeAll(P, symbols), buildModel(model, P, value))
    #Guessing a literal
    P, symbols = symbols[0], symbols[1:]
    return (dpll(cnf, symbols, buildModel(model, P, True)) or dpll(cnf, symbols, buildModel(model, P, False)))

def get_symbols(cnf):
    symbols = []
    for clause in cnf:
        for c in clause:
            if c[0] != "~":
                if c not in symbols:
                    symbols.append(c)
    return symbols

# This function generates cnf statements
def generate_cnf():
    cnf = []

    for m in range(1, M + 1):
        clause = []
        for n in range(1, N+1):
            clause.append("X" + str([m, n]))
            for ni in range(n+1, N+1):
                clauseneg = []
                clauseneg.append("~X" + str([m, n]))
                clauseneg.append("~X" + str([m, ni]))
                cnf.append(clauseneg)
        cnf.append(clause)

    for x in range(1, M+1):
        for y in range(1, M+1):
            if R[x][y] == 1:
                for n in range(1, N+1):
                    clause = []
                    clause.append("X" + str([y, n]))
                    clause.append("~X" + str([x, n]))
                    cnf.append(clause)
                    clause = []
                    clause.append("X" + str([x, n]))
                    clause.append("~X" + str([y, n]))
                    cnf.append(clause)

    for x in range(1, M+1):
        for y in range(1, M+1):
            if R[x][y] == -1:
                for n in range(1, N+1):
                    clause = []
                    clause.append("~X" + str([x, n]))
                    clause.append("~X" + str([y, n]))
                    cnf.append(clause)

    symbols = get_symbols(cnf)
    return dpll(cnf, symbols, {})

fo = open("input.txt", "r")
inputList = fo.readlines()
line1 = []
for word in inputList[0].split(" "):
    line1.append(int(word))

M = line1[0]    #Number of guests
N = line1[1]   #Number of tables

if M != 0 and N != 0:
    R = [[]]
    for x in range(0,M):
        inner = [[]]
        for y in range(0,M):
            inner.append(0)
        R.append(inner)

    for val in range(1,len(inputList)):
        b = inputList[val].split(" ")
        if b[2] == "F" or b[2] == "F\n":
            R[int(b[0])][int(b[1])] = 1
        else:
            R[int(b[0])][int(b[1])] = -1

    output = generate_cnf()
    fo = open("output.txt", "w")
    if output == False:
        fo.write("no")
    else:
        fo.write("yes\n")
        list = []
        for (k,v) in output.iteritems():
            if v == True:
                list.append(k)
        listnew = []
        for val in list:
            listtemp = []
            temp = val[2:-1].split(",")
            listtemp.append(int(temp[0]))
            listtemp.append(int(temp[1]))
            listnew.append(listtemp)
        for val in sorted(listnew):
            fo.write(str(val[0]) + " " + str(val[1]))
            fo.write("\n")
    fo.close()

else:
    fo = open("output.txt", "w")
    fo.write("no")
    fo.close()