import json
intrare=open("teste.json",'r')
x=json.load(intrare)

for i in range(0,20):
    print(x[i])