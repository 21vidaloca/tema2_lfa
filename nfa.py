x=open("nfa_config_file.txt","r").readlines()
# print(x)
n=len(x)
stari_finale=[]
dict={}
c=0
invalid=0
# stare_initiala=""
for i in range(0,n):
    cuv=str(x[i])[:-1]
    # print(len(cuv))
    j=i
    
    if(cuv=="States:"):
        j=i+1
        while(j<n):
            stare=str(x[j])[:-1]
            ceva=stare.split(", ")
            if(stare!="End"):
                dict[ceva[0]]=[]
                if(len(ceva)==2):
                    if(ceva[1]=='S'):
                        stare_initiala=ceva[0]
                        c=c+1
                    if(ceva[1]=='F'):
                        stari_finale.append(ceva[0])
                if(len(ceva)==3):
                    if(ceva[1]=='S'):
                        stare_initiala=ceva[0] 
                        c=c+1
                    if(ceva[2]=='F'):
                        stari_finale.append(ceva[0])
            
            
            # print(ceva,"*****")
            j=j+1
            if(stare=="End"):
                break
        break

# print(dict,"\n")
alfabet=[]
for i in range(0,n):
    cuv=str(x[i])[:-1]
    # print(len(cuv))
    j=i
    if(cuv=="Sigma:"):
        j=i+1
        while(j<n):
            stare=str(x[j])[:-1]
            if(stare!="End"):
                alfabet.append(stare)
            j=j+1
            if(stare=="End"):
                break
        break
# print(dict)
for i in range(0,n):
    cuv=str(x[i])[:-1]
    # print(len(cuv))
    j=i
    if(cuv=="Transitions:"):
        j=i+1
        while(j<n):
            stare=str(x[j])[:-1]
            # print(stare)
            if(stare!="End" and stare!="En"):
                ceva=stare.split(", ")
                # print(ceva)
                if(ceva[0] not in dict or ceva[2] not in dict): # pentru noduri
                    invalid=1
                    # print("aici#2.1")
                else:
                    if(ceva[1] in alfabet):
                        dict[str(ceva[0])].append((ceva[1],ceva[2]))
                    else: # pentru muchii
                        invalid=1
                        # print(ceva,"aici#2.2")
            j=j+1
            if(stare=="End" or stare=="En"):
                break
        break
if(c>1):
    invalid=1
    # print("aici#3")
# etapa 1 - verificare daca este nfa
estenfa=1
for x in dict:
    fr={}
    for ceva in dict[x]:
        if(ceva[0] not in fr):
            fr[ceva[0]]=1
        else:
            fr[ceva[0]]+=1
    for ceva in fr:
        if(fr[ceva]>1):
            estenfa=2
if(invalid==1):
    print("automatul este invalid")
else:
    if(estenfa==2):
        print("automatul este nfa")
    else:
        print("automatul nu este nfa")

# etapa 2 - verificare string
# verificam sirul "adefbcefacf"(accept) sau ""(reject)
sir="abcefacfbc"
# print(sir)
ind=0
ok=0
n=len(sir)
# print(stari_finale)
def verificare(nod,ind):
    global ok
    for k in dict[nod]:
        if(ind<n):
            if(sir[ind]==k[0]):
                if(ind==(n-1) and (k[1] in stari_finale)):
                    # stop??
                    ok=1
                    # print("intru aci")
                    
                ind=ind+1
                # print(k,ind)
                verificare(k[1],ind)
                # print(k,ind)
                ind=ind-1
        # print(k)
verificare(stare_initiala,0)

if(sir=="" and (stare_initiala in stari_finale)):
    ok=1
if(ok!=0):
    print("sirul primit este bun")
else:
    print("sirul primit nu este bun")
