def is_code_by_sardinas(L):
    # print("L0", L)
    if len(L) == 0:
        return True
    
    L1 = remove_eps(residuel(L, L))
    # print("L1", L1)
    if len(L1) == 0:
        return True

    i = 2
    Ln = L1
    tab = [Ln]
    while True:
        Ln_1 = list(set(residuel(L, Ln) + residuel(Ln, L)))
        # print("L" + str(i), Ln_1)

        if Ln_1 in tab:
            # print("Periodique")
            return True
        elif len(Ln_1) == 0:
            return True
        elif "" in Ln_1:
            # print("Misy eps")
            return False
        
        tab.append(Ln_1)
        i += 1
        Ln = Ln_1

def residuel(L1, L2):
    output = []
    for item1 in L1:
        for item2 in L2:
            tmp = item1.removeprefix(item2)
            if tmp != item1:
                output.append(tmp)
    return output

def remove_eps(language):
    return [item for item in language if item != '']