from itertools import combinations

#variaveis globais
list_default = [1,2,3,4]

#função para listar subconjuntos
def subgroup(grouplist,max_size=None, min_size=None, distinct_only=False, sort_subsets=False):
    if distinct_only:
        conjunto = list(set(grouplist))

    if sort_subsets: #ordena a lista
        grouplist.sort()

    subgrouplists = [[]] #vazio

    for lenghtin in range(1, len(grouplist) + 1):
        if (min_size is not None and lenghtin < min_size) or (max_size is not None and lenghtin > max_size):
            continue
        
        # Adiciona combinações do tamanho especificado
        subgrouplists += [list(comb) for comb in combinations(grouplist, lenghtin)]
    
    return subgrouplists

sub_result = subgroup(list_default, max_size=3, min_size=2, distinct_only=True, sort_subsets=True)
print(sub_result)