# from dfa import verificare
def parsare():
    import json

    chestie_intrare = open("teste.json", "r")
    chestie_parsata = json.load(chestie_intrare)
    return chestie_parsata


def transformare_postfix(sir_primit):
    sir_iesire = ""
    stiva = []
    operatori = "+*|?()."
    precedenta = {"*": 3, "+": 3, "?": 3, ".": 2, "|": 1, "(": 0}

    def insereaza_punct(sir):
        rezultat = ""
        i = 0
        while i < len(sir):
            rezultat += sir[i]
            if i + 1 < len(sir):
                caracter_curent = sir[i]
                caracter_urmator = sir[i + 1]
                if (
                    (caracter_curent.isalnum() and caracter_urmator.isalnum())
                    or (caracter_curent in ")*+?" and caracter_urmator.isalnum())
                    or (caracter_curent in ")" and caracter_urmator == "(")
                    or (caracter_curent.isalnum() and caracter_urmator == "(")
                    or (caracter_curent in ")*+?" and caracter_urmator == "(")):
                    rezultat += "."
            i = i + 1
        return rezultat

    sir_primit = insereaza_punct(sir_primit)
    for caracter in sir_primit:
        if caracter.isalnum(): 
            sir_iesire += caracter
        elif caracter == "(":
            stiva.append(caracter)
        elif caracter == ")":
            while stiva and stiva[-1] != "(":
                sir_iesire += stiva.pop()
            stiva.pop()
        elif caracter in operatori:
            while (
                stiva
                and stiva[-1] != "("
                and precedenta.get(stiva[-1], 0) >= precedenta.get(caracter, 0)
            ):
                sir_iesire += stiva.pop()
            stiva.append(caracter)
    while stiva:
        sir_iesire += stiva.pop()

    return sir_iesire


def repeta_peste0(nfa_initial):
    nfa_final=nfa_initial
    return nfa_final

def repeta_peste1(nfa_initial):
    nfa_final=nfa_initial
    return nfa_final

def prezenta_optionala(nfa_initial):
    nfa_final=nfa_initial
    return nfa_final

def reuniune(nfa1,nfa2):
    nfa_final=nfa1
    return nfa_final

def concatenare(nfa1,nfa2):
    nfa_final=nfa1
    return nfa_final

def transformare_lambda_nfa(regex):
    contor=0
    aux="q"
    n=len(regex)
    stiva=[]
    operatori = "+*|?."
    for i in range(0,n):
        stare_initiala=""
        stare_finala=[]
        dict={}
        if regex[i] not in operatori: # creeam un nfa cu o muchie
            stare=aux+str(contor)
            stare_initiala=stare
            contor+=1
            stare=aux+str(contor)
            contor+=1
            stare_finala.append(stare)
            dict[stare_initiala]=(stare,regex[i])
            stiva.append((stare_initiala,stare_finala,dict))
            print(stare_initiala)
            print(stare_finala)
            print(dict)
            print("\n\n")
        elif regex[i] == "*": # kleene adica repetam de >=0
            nfa1=stiva[-1]
            stiva.pop()
            nfa2=repeta_peste0(nfa1)
            stiva.append(nfa2)
        elif regex[i] == "+": # repetam de >=1
            nfa1=stiva[-1]
            stiva.pop()
            nfa2=repeta_peste1(nfa1)
            stiva.append(nfa2)
        elif regex[i] == "|":
            nfa2=stiva[-1]
            nfa1=stiva[-2]
            stiva.pop()
            stiva.pop()
            nfa3=reuniune(nfa1,nfa2)
            stiva.append(nfa3)
        elif regex[i] == "?":
            nfa1=stiva[-1]
            stiva.pop()
            nfa2=prezenta_optionala(nfa1)
            stiva.append(nfa2)
        elif regex[i] == ".":
            nfa2=stiva[-1]
            nfa1=stiva[-2]
            stiva.pop()
            stiva.pop()
            nfa3=concatenare(nfa1,nfa2)
            stiva.append(nfa3)
    print(stiva)




intrare = parsare()
for ind in range(0, 2):
    regex_intrare = intrare[ind]["regex"]
    regex_nou = transformare_postfix(regex_intrare)
    print(regex_intrare + "     " + regex_nou)

    # creeam un tuplu
    lambda_nfa=transformare_lambda_nfa(regex_nou)
    # print(lambda_nfa)