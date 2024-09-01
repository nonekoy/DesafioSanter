

# Variáveis globais
default_list = [10,20,30,41,53]
created_list = []
allow_duplicates = True
sorted_pairs = False
unique_pairs = False
digit = int()

# Diminuir repetições
def choice(): 
    while True:
        try:
            x = int(input())
            if x<1 or x>2:
                raise Exception
            return x == 1
        except:
            print("entrada inválida")

# Muda os parâmetros
def configure(): 
    global allow_duplicates
    global sorted_pairs
    global unique_pairs
    print("defina a configuração:")
    print("Allow duplicates 1= on 2= off")
    allow_duplicates = choice()
    print("sorted_pairs 1= on 2= off")
    sorted_pairs = choice()
    print("unique_pairs 1= on 2= off")
    unique_pairs = choice()

# Função que pega o par com menor diferença
def minor_pairs(listed, allow_duplicates, sorted_pairs, unique_pairs): 
    minor_distance = float('inf')
    result = []
    if len(listed)<2:
        return []
    listed.sort()
    if not allow_duplicates: # Se for falso remove todos os resultados duplicados da lista
        listed = set(listed)

    for i in range(len(listed)-1):
        distance = listed[i+1] - listed[i]
        
        if distance < minor_distance:
            minor_distance = distance
            result = [(listed[i],listed[i+1])]
            continue
        if distance == minor_distance:
            result.append((listed[i], listed[i+1]))
    
    if sorted_pairs:    # Só reorganiza os pares se ativo
        result.sort()
    
    if unique_pairs:  # Remove os pares repetidos
        result = list(set(result))
        #result.sort()
        #final = list(pair) for pair in result
    return result

        

while True:
    try: # Match case com tratamento de exceções
        op = int(input("Digite uma opção: Criar lista(1), usar lista existente(2), mudar configurações(3), fechar (4) \n"))
        match op:
            case 1:
                print("enquanto não digitar 0 a lista será adicionada");
                while True:
                    try:
                        while True:
                            digit = int(input())
                            if digit == 0:
                                break
                            created_list.append(digit)
                    except:
                        print("Entrada inválida.")
                    if digit == 0:
                        break
                print("lista criada", created_list)
                print(minor_pairs(created_list,allow_duplicates,sorted_pairs,unique_pairs))
                digit = 1
                created_list = []

            case 2:
                
                print(minor_pairs(default_list,allow_duplicates,sorted_pairs,unique_pairs))
            case 3:
                configure()
                print("configurações atuais:")
                print("allow_duplicates =", allow_duplicates)
                print("sorted_pairs =", sorted_pairs)
                print("unique_pairs =", unique_pairs)
            case 4:
                break
            case _:
                raise Exception
    except:
        print("Entrada inválida.")
