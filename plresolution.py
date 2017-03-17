import copy

def pl_resolve(ci, cj):
    citemp = copy.deepcopy(ci)
    cjtemp = copy.deepcopy(cj)
    print citemp, cjtemp
    clauses = []
    flag = 0
    for i in ci:
        for j in cj:
            if i == "~" + j or j == "~" + i:
                flag = 1
                del citemp[citemp.index(i)]
                del cjtemp[cjtemp.index(j)]
                clauses.append(sorted(citemp + cjtemp))
                return clauses, flag

    return clauses, flag

def pl_resolution(cnf):
    new_cnf = set()
    cnt = 0
    while True:
        n = len(cnf)
        pairs = [(cnf[i], cnf[j]) for i in range(n) for j in range(i + 1, n)]
        for (ci, cj) in pairs:
            resolvents, flag = pl_resolve(ci, cj)
            print "R : " ,resolvents
            if flag == 1:
                for x in resolvents:
                    if not x:
                        return False
            else :
                continue
            new_cnf = new_cnf.union(set(tuple(row) for row in resolvents))
            print "Union : ", new_cnf
        if new_cnf.issubset(set(tuple(row) for row in cnf)):
            return True
        for c in new_cnf:
            c = list(c)
            #print type(c)
            #print "C " , c
            if c not in cnf:
                cnf.append(c)
        print "CNF : ", cnf
        print len(cnf)

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
                    clause.append("~X" + str([x, n]))
                    clause.append("X" + str([y, n]))
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
    print cnf
    print len(cnf)
    print pl_resolution(cnf)

fo = open("input.txt", "r")
inputList = fo.readlines()
line1 = []
for word in inputList[0].split(" "):
    line1.append(int(word))

M = line1[0]    #Number of guests
N = line1[1]   #Number of tables

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

print R
generate_cnf()

