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
                    or (caracter_curent in ")*+?" and caracter_urmator == "(")
                ):
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


def repeta_peste0(nfa_initial, ind):
    sinit = "q" + str(ind)
    sfin = nfa_initial[1]
    sfin.append(sinit)
    dnou = nfa_initial[2]
    for sx in nfa_initial[1]:
        if sx not in dnou:
            dnou[sx] = [(nfa_initial[0], "")]
        else:
            dnou[sx].append((nfa_initial[0], ""))
    nfa_final = (sinit, sfin, dnou)
    # print(nfa_final)
    # print("final")
    return nfa_final


def repeta_peste1(nfa_initial, ind):
    sinit = "q" + str(ind)
    sfin = nfa_initial[1]
    dnou = nfa_initial[2]
    dnou[sinit] = [(nfa_initial[0], "")]
    for sx in nfa_initial[1]:
        if sx not in dnou:
            dnou[sx] = [(nfa_initial[0], "")]
        else:
            dnou[sx].append((nfa_initial[0], ""))
    nfa_final = (sinit, sfin, dnou)
    # print(nfa_final)
    # print("final")
    return nfa_final


def prezenta_optionala(nfa_initial, ind):
    sinit = "q" + str(ind)
    saux = "q" + str(ind + 1)
    sfin = [saux]
    dnou = nfa_initial[2]
    dnou[sinit] = [(nfa_initial[0], "")]
    dnou[sinit].append((saux, ""))
    for sx in nfa_initial[1]:
        if sx not in dnou:
            dnou[sx] = [(saux, "")]
        else:
            dnou[sx].append((saux, ""))
    nfa_final = (sinit, sfin, dnou)
    # print(nfa_final)
    # print("final semnu intrebarii")
    return nfa_final


def reuniune(nfa1, nfa2, ind):
    sinit = "q" + str(ind)  # asta va fi starea initiala
    sfin = []
    # print("intram aci")
    for sx in nfa1[1]:
        sfin.append(sx)
    for sx in nfa2[1]:
        sfin.append(sx)
    dnou = {}
    for dx in nfa1[2]:
        dnou[dx] = nfa1[2][dx]
    for dx in nfa2[2]:
        dnou[dx] = nfa2[2][dx]
    dnou[sinit] = [(nfa1[0], "")]
    dnou[sinit].append((nfa2[0], ""))
    nfa_final = (sinit, sfin, dnou)
    # print(nfa_final)
    # print("final reuniune/alternare")
    return nfa_final


def concatenare(nfa1, nfa2):
    sinit = nfa1[0]
    sfin = nfa2[1]
    dnou = {}
    for dx in nfa1[2]:
        dnou[dx] = nfa1[2][dx]
    for dx in nfa2[2]:
        dnou[dx] = nfa2[2][dx]
    for sx in nfa1[1]:
        if sx not in dnou:
            dnou[sx] = [(nfa2[0], "")]
        else:
            dnou[sx].append((nfa2[0], ""))
    nfa_final = (sinit, sfin, dnou)
    # print("inceput concatenare")
    # print(nfa_final)
    # print("final concatenare")
    return nfa_final


def transformare_lambda_nfa(regex):
    contor = 0
    aux = "q"
    n = len(regex)
    stiva = []
    operatori = "+*|?."
    for i in range(0, n):
        stare_initiala = ""
        stare_finala = []
        dict = {}
        if regex[i] not in operatori:  # creeam un nfa cu o muchie
            stare = aux + str(contor)
            stare_initiala = stare
            contor += 1
            stare = aux + str(contor)
            contor += 1
            stare_finala.append(stare)
            dict[stare_initiala] = [(stare, regex[i])]
            stiva.append((stare_initiala, stare_finala, dict))
            # print(stare_initiala)
            # print(stare_finala)
            # print(dict)
            # print("\n\n")
        elif regex[i] == "*":  # rezolvat kleene adica repetam de >=0
            nfa1 = stiva[-1]
            stiva.pop()
            nfa2 = repeta_peste0(nfa1, contor)
            contor += 1
            stiva.append(nfa2)
        elif regex[i] == "+":  # repetam de >=1 rezolvat
            nfa1 = stiva[-1]
            stiva.pop()
            nfa2 = repeta_peste1(nfa1, contor)
            contor += 1
            stiva.append(nfa2)
        elif regex[i] == "|":  # rezolvat
            nfa2 = stiva[-1]
            nfa1 = stiva[-2]
            stiva.pop()
            stiva.pop()
            nfa3 = reuniune(nfa1, nfa2, contor)
            contor += 1
            stiva.append(nfa3)
        elif regex[i] == "?":
            nfa1 = stiva[-1]
            stiva.pop()
            nfa2 = prezenta_optionala(nfa1, contor)
            contor += 2
            stiva.append(nfa2)
        elif regex[i] == ".":  # rezolvat
            nfa2 = stiva[-1]
            nfa1 = stiva[-2]
            stiva.pop()
            stiva.pop()
            nfa3 = concatenare(nfa1, nfa2)
            stiva.append(nfa3)
    # print(stiva)
    # print("\n\n\n")
    return stiva[0]


def transformare_nfa(nfa):
    ok = 1
    sinit = nfa[0]
    sfin = nfa[1]
    dict = nfa[2]
    while ok:
        aux = 0
        for x in dict:
            # print(x)
            # print(dict[x])
            for a in dict[x]:  # ne uitam pe (x,a[0],cost=a[1])
                if a[1] == "":
                    # print(dict[a[0]])
                    for b in dict[a[0]]:  # ne uitam pe (a[0],b[0],cost=b[1])
                        if b[0] != x and b[1] == "":
                            val = 1
                            for chestie in dict[x]:
                                if chestie[0] == b[0] and chestie[1] == "":
                                    val = 0
                                    break
                            # adaugam muchie intre x si b[0]
                            if val == 1:
                                dict[x].append((b[0], ""))
                                aux = 1
        ok = aux

    for x in dict:
        # print(x)
        # print(dict[x])
        for a in dict[x]:
            if a[0] in nfa[1] and a[1] == "" and x not in sfin:
                sfin.append(x)
    # print("\n\n",dict,sfin)
    ok = 1
    while ok:
        aux = 0
        for x in dict:
            # print(x)
            # print(dict[x])
            lg = len(dict[x])
            i = 0
            while i < lg:
                # avem tuplul dict[x][i]
                # print(i,len(dict[x]))
                elim = 0
                if i < len(dict[x]):
                    a = dict[x][i]
                    # print(i,len(dict[x]))
                    if a[1] == "":
                        for b in dict[a[0]]:
                            if b[1] != "":
                                # am gasit ceva deci legam (x,b[0],b[1])
                                # print(x,a[0],dict[x])
                                # print(dict[a[0]])
                                # print(b[0],b[1],i)
                                # print("terminam afisarea")

                                if (b[0], b[1]) not in dict[x]:
                                    dict[x].append((b[0], b[1]))

                                elim += 1
                                # print(dict[x])
                                # print(dict[a[0]])
                                # print("terminam afisarea din nou")
                                aux = 1
                        if elim:
                            dict[x].pop(i)
                i = i + 1 - elim
            # print("schimbaaaaaaaaaaaaaaaaaaaaaammmmmmmmmmm")
        ok = aux
    nfa_final = (sinit, sfin, dict)
    return nfa_final


def verificare_nfa(sir, nfa, nod, ind):
    global ok
    if nod in nfa[2]:
        for k in nfa[2][nod]:

            if ind < len(sir):
                # print("ma aflu aici",len(sir),ind,nod)
                if sir[ind] == k[1]:
                    if ind == (len(sir) - 1) and (k[0] in nfa[1]):
                        # stop??
                        ok = 1
                        # print("intru aci")

                    ind = ind + 1
                    # print(k[0],k[1],ok)
                    # print("intru",ind)
                    verificare_nfa(sir, nfa, k[0], ind)
                    # print(k,ok)
                    # print("ies",ind)
                    ind = ind - 1


def transformare_nfa_dfa(nfa):
    dfa_final = nfa
    return dfa_final


intrare = parsare()
suma = 0
for indice in range(0, 20):
    regex_intrare = intrare[indice]["regex"]
    regex_nou = transformare_postfix(regex_intrare)
    print(regex_intrare + "     " + regex_nou)

    # creeam un tuplu
    lambda_nfa = transformare_lambda_nfa(regex_nou)
    ind = 0
    ok = 0
    # print(lambda_nfa)
    nfa = transformare_nfa(lambda_nfa)
    # print("\n\n\n")
    # print(nfa)

    dfa = transformare_nfa_dfa(nfa)
    print(dfa)

    # aici verificam sirurile
    teste = intrare[indice]["test_strings"]
    for ceva in range(0, 1):  # len(teste)):

        ind = 0
        ok = 0
        sir_primit = intrare[indice]["test_strings"][ceva]["input"]
        # print(sir_primit, indice + 1)
        stare_init = nfa[0]
        verificare_nfa(sir_primit, nfa, stare_init, 0)
        ans = ""
        exp = intrare[indice]["test_strings"][ceva]["expected"]
        if sir_primit == "":
            if nfa[0] not in nfa[1]:
                ok = 0
            else:
                ok = 1
        if ok != exp:
            suma += 1
            print(exp)
            print(sir_primit, indice + 1)
            print("\n\n\n")
        # print("scshimbammmmmmmmmmmmmmmmmmm")


print(suma)
