# Heurísticas para a Solução do Subset Sum
# Integrantes: Flávio Novaes de Oliveira, Guilherme de Melo Werneck, Gabriel Miranda, Gustavo de Menezes
# Matrículas: 2022101314, 2022101349, 2022101859, 2022101566

def calcSum(x, vet):
    soma = 0
    for i in vet:
        soma += x[i]
    return soma

def divEConq(x, a, T, vet):
    if a == len(x):
        return vet if calcSum(x, vet) == T else []
    else:
        l = vet[:a]
        r = vet[:a]
        r.append(a)
        vetl = divEConq(x, a+1, T, l)
        vetr = divEConq(x, a+1, T, r)
        sl = calcSum(x, vetl)
        sr = calcSum(x, vetr)
        if sl == T:
            return vetl
        elif sr == T:
            return vetr
        else:
            return []

# Teste
S = [4, 6, 3, 2, 7, 9, 1, 10]
T = 12
vet = divEConq(S, 0, T, [])
subset = [S[i] for i in vet]
print("\nAlgoritmo Exato (Divisão e Conquista):")
print("Subconjunto encontrado (índices):", vet)
print("Subconjunto encontrado (valores):", subset)
print("Soma dos pesos:", sum(subset))

def firstFit(S, T):
    bm = []
    soma = 0
    for i in range(len(S)):
        if soma + S[i] <= T:
            bm.append(i)
            soma += S[i]
            if soma == T:
                break
    return bm if soma == T else []

# Teste
S = [4, 6, 3, 2, 7, 9, 1, 10]
T = 12
vet = firstFit(S, T)
subset = [S[i] for i in vet]
print("\nFirst Fit:")
print("Subconjunto encontrado (índices):", vet)
print("Subconjunto encontrado (valores):", subset)
print("Soma dos pesos:", sum(subset))

def bestFit(S, T):
    indices = sorted(range(len(S)), key=lambda i: -S[i])
    bm = []
    soma = 0
    for i in indices:
        if soma + S[i] <= T:
            bm.append(i)
            soma += S[i]
            if soma == T:
                break
    return bm if soma == T else []

# Teste
S = [4, 6, 3, 2, 7, 9, 1, 10]
T = 12
vet = bestFit(S, T)
subset = [S[i] for i in vet]
print("\nBest Fit:")
print("Subconjunto encontrado (índices):", vet)
print("Subconjunto encontrado (valores):", subset)
print("Soma dos pesos:", sum(subset))

def worstFit(S, T):
    indices = sorted(range(len(S)), key=lambda i: S[i])
    bm = []
    soma = 0
    for i in indices:
        if soma + S[i] <= T:
            bm.append(i)
            soma += S[i]
            if soma == T:
                break
    return bm if soma == T else []

# Teste
S = [4, 6, 3, 2, 7, 9, 1, 10]
T = 12
vet = worstFit(S, T)
subset = [S[i] for i in vet]
print("\nWorst Fit:")
print("Subconjunto encontrado (índices):", vet)
print("Subconjunto encontrado (valores):", subset)
print("Soma dos pesos:", sum(subset))

import random

def getSum(S, mochila):
    return sum(S[i] if mochila[i] == '1' else 0 for i in range(len(S)))

def geraEstadoInicial(S, T):
    while True:
        mAtual = ''.join(random.choice('01') for _ in range(len(S)))
        sAtual = getSum(S, mAtual)
        if sAtual <= T:
            return mAtual, sAtual

def melhorVizinho(mAtual, S, T):
    melhor_m = mAtual
    melhor_s = getSum(S, mAtual)
    for i in range(len(mAtual)):
        vizinho = mAtual[:i] + ('0' if mAtual[i] == '1' else '1') + mAtual[i+1:]
        s_vizinho = getSum(S, vizinho)
        if s_vizinho <= T and abs(T - s_vizinho) < abs(T - melhor_s):
            melhor_m = vizinho
            melhor_s = s_vizinho
    return melhor_m, melhor_s

def subidaDeEncosta(S, T, max_iter=1000):
    mAtual, sAtual = geraEstadoInicial(S, T)
    for _ in range(max_iter):
        if sAtual == T:
            break
        mProxima, sProxima = melhorVizinho(mAtual, S, T)
        if sProxima == T:
            return mProxima, sProxima
        if abs(T - sProxima) < abs(T - sAtual):
            mAtual, sAtual = mProxima, sProxima
        else:
            break
    return mAtual, sAtual

# Teste
S = [4, 6, 3, 2, 7, 9, 1, 10]
T = 12
mochila, soma = subidaDeEncosta(S, T)
subset = [S[i] for i in range(len(S)) if mochila[i] == '1']
print("\nSubida de Encosta:")
print("Representação binária:", mochila)
print("Subconjunto encontrado (valores):", subset)
print("Soma dos pesos:", soma)

import random
import math

def getSum(S, mochila):
    return sum(S[i] for i in range(len(S)) if mochila[i] == '1')

def geraEstadoAleatorio(S, T):
    while True:
        mAtual = ''.join(random.choice('01') for _ in range(len(S)))
        sAtual = getSum(S, mAtual)
        if sAtual <= T:
            return mAtual, sAtual

def geraVizinhoAleatorio(mAtual, S, T, temperatura):
    while True:
        vizinho = list(mAtual)
        flip = random.sample(range(len(mAtual)), min(temperatura, len(mAtual)))
        for i in flip:
            vizinho[i] = '1' if vizinho[i] == '0' else '0'
        vizinho = ''.join(vizinho)
        s_vizinho = getSum(S, vizinho)
        if s_vizinho <= T:
            return vizinho, s_vizinho

def simulatedAnnealing(S, T, tamanhoAgenda=100):
    mAtual, sAtual = geraEstadoAleatorio(S, T)
    mMelhor, sMelhor = mAtual, sAtual
    T_schedule = [t for t in range(tamanhoAgenda, 0, -1)]
    
    for t in T_schedule:
        if sAtual == T:
            break
        mProxima, sProxima = geraVizinhoAleatorio(mAtual, S, T, t)
        delta = abs(T - sProxima) - abs(T - sAtual)
        
        if delta < 0 or random.random() < math.exp(-delta / t):
            mAtual, sAtual = mProxima, sProxima
            if abs(T - sAtual) < abs(T - sMelhor):
                mMelhor, sMelhor = mAtual, sAtual
    
    return mMelhor, sMelhor

# Teste
S = [4, 6, 3, 2, 7, 9, 1, 10]
T = 12
mochila, soma = simulatedAnnealing(S, T)
subset = [S[i] for i in range(len(S)) if mochila[i] == '1']
print("\nSimulated Annealing:")
print("Representação binária:", mochila)
print("Subconjunto encontrado (valores):", subset)
print("Soma dos pesos:", soma)