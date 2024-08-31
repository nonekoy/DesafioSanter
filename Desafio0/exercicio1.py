

def star_list(x): 
    list=[]
    for i in range(x):
        list.append("*"*(i+1))
    print(list)

while True:
    try:
        valor= int(input("Digite um valor N:"))
        star_list(valor)
        break
    except:
        print("Entrada inválida.")