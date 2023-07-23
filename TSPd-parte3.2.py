import math
import sys
import random
import time


def ler_tipo_0(conteudo):
    numeros = []

    conteudo_linha = conteudo[3].split()
    dimension = int(conteudo_linha[len(conteudo_linha) - 1])

    k = 7

    while True:
        if conteudo[k] == "EOF":
            break

        conteudo_linha = conteudo[k].split()

        for numero in conteudo_linha:
            numeros.append(int(numero))

        k = k + 1

    matriz_distancias = []

    for i in range(dimension):
        matriz_distancias.append([])

        for j in range(dimension):
            matriz_distancias[i].append(0)

    posicao_atual = 0

    for j in range(dimension):
        for i in range(dimension):
            if i <= j:
                matriz_distancias[i][j] = numeros[posicao_atual]
                matriz_distancias[j][i] = numeros[posicao_atual]
                posicao_atual = posicao_atual + 1

    return matriz_distancias


def ler_tipo_1(conteudo):
    numeros = []

    conteudo_linha = conteudo[3].split()
    dimension = int(conteudo_linha[len(conteudo_linha) - 1])

    k = 8

    while True:
        if conteudo[k] == "DISPLAY_DATA_SECTION":
            break

        conteudo_linha = conteudo[k].split()

        for numero in conteudo_linha:
            numeros.append(int(numero))

        k = k + 1

    matriz_distancias = []

    for i in range(dimension):
        matriz_distancias.append([])

        for j in range(dimension):
            matriz_distancias[i].append(0)

    posicao_atual = 0

    for j in range(dimension):
        for i in range(dimension):
            if i <= j:
                matriz_distancias[i][j] = numeros[posicao_atual]
                matriz_distancias[j][i] = numeros[posicao_atual]
                posicao_atual = posicao_atual + 1

    return matriz_distancias


def ler_tipo_2(conteudo):
    x = []
    y = []

    conteudo_linha = conteudo[3].split()
    dimension = int(conteudo_linha[len(conteudo_linha) - 1])

    k = 6

    while True:
        if conteudo[k] == "EOF":
            break

        conteudo_linha = conteudo[k].split()

        x.append(int(float(conteudo_linha[1])))
        y.append(int(float(conteudo_linha[2])))

        k = k + 1

    matriz_distancias = []

    for i in range(dimension):
        matriz_distancias.append([])

        for j in range(dimension):
            matriz_distancias[i].append(0)

    distance = lambda x1, y1, x2, y2: int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) + 0.5)

    for i in range(dimension):
        for j in range(dimension):
            matriz_distancias[i][j] = distance(x[i], y[i], x[j], y[j])

    return matriz_distancias


def ler_tipo_3(conteudo):
    numeros = []

    conteudo_linha = conteudo[3].split()
    dimension = int(conteudo_linha[len(conteudo_linha) - 1])

    k = 7

    while True:
        if conteudo[k] == "EOF":
            break

        conteudo_linha = conteudo[k].split()

        for numero in conteudo_linha:
            numeros.append(int(numero))

        k = k + 1

    matriz_distancias = []

    for i in range(dimension):
        matriz_distancias.append([])

        for j in range(dimension):
            matriz_distancias[i].append(0)

    posicao_atual = 0

    for i in range(dimension):
        for j in range(dimension):
            if i < j:
                matriz_distancias[i][j] = numeros[posicao_atual]
                matriz_distancias[j][i] = numeros[posicao_atual]
                posicao_atual = posicao_atual + 1

    return matriz_distancias


def solucao_inicial(distancias):
    solucao = [0]
    cidades_nao_visitadas = []

    for i in range(1, len(distancias)):
        cidades_nao_visitadas.append(i)

    qtd_cidades = len(cidades_nao_visitadas)

    i = 0

    while i < qtd_cidades:
        melhor_distancia = math.inf
        melhor_cidade = None

        for cidade in cidades_nao_visitadas:
            if distancias[solucao[len(solucao) - 1]][cidade] < melhor_distancia:
                melhor_distancia = distancias[solucao[len(solucao) - 1]][cidade]
                melhor_cidade = cidade

        solucao.append(melhor_cidade)
        cidades_nao_visitadas.remove(melhor_cidade)

        i = i + 1

    return solucao


def avalia_solucao(solucao, distancias, k, v):
    valor_total = 0

    for i in range(len(solucao) - 1):
        valor_total = valor_total + distancias[solucao[i]][solucao[i + 1]]

    valor_total = valor_total + distancias[solucao[len(solucao) - 1]][solucao[0]]

    entregas = []

    for j in range(1, k + 1):
        entregas.append((2 * j - 1, 2 * j))

    qtd_entregas_realizadas = 0

    for entrega in entregas:
        inicio = solucao.index(entrega[0])
        fim = solucao.index(entrega[1])

        if inicio < fim:
            qtd_entregas_realizadas = qtd_entregas_realizadas + 1

    valor_total = valor_total - qtd_entregas_realizadas * v

    return valor_total


def melhor_vizinho(solucao, distancias, k, v):
    melhor_solucao = solucao
    melhor_avaliacao = avalia_solucao(solucao, distancias, k, v)

    solucao.append(solucao[0])

    for i in range(1, len(solucao) - 2):
        for j in range(i + 1, len(solucao)):
            if j - i == 1:
                continue

            nova_solucao = solucao[:]
            nova_solucao[i:j] = solucao[j - 1:i - 1:-1]
            nova_solucao.pop(len(nova_solucao) - 1)

            avaliacao = avalia_solucao(nova_solucao, distancias, k, v)

            if avaliacao < melhor_avaliacao:
                melhor_avaliacao = avaliacao
                melhor_solucao = nova_solucao

    solucao.pop(len(solucao) - 1)

    return melhor_solucao, melhor_avaliacao


def busca_local(distancias, k, v, solucao_inicial):
    solucao_atual = solucao_inicial
    avaliacao_solucao_atual = avalia_solucao(solucao_atual, distancias, k, v)

    while True:
        vizinho, avaliacao_vizinho = melhor_vizinho(solucao_atual, distancias, k, v)

        if avaliacao_vizinho < avaliacao_solucao_atual:
            solucao_atual = vizinho
            avaliacao_solucao_atual = avaliacao_vizinho
        else:
            break

    return solucao_atual, avaliacao_solucao_atual


def iterated_greedy(distancias, k, v):
    solucao = solucao_inicial(distancias)
    solucao, avaliacao_solucao = busca_local(distancias, k, v, solucao)

    melhor_solucao = solucao.copy()
    avaliacao_melhor_solucao = avaliacao_solucao

    inicio = time.time()

    for _ in range(1000):
        solucao_nova = solucao.copy()
        parte_destruida = []

        d = int(0.50 * len(solucao_nova))

        for i in range(d):
            indice = random.randint(1, len(solucao_nova) - 1)

            parte_destruida.append(solucao_nova[indice])
            solucao_nova.pop(indice)

        for i in range(d):
            melhor_indice = 1
            menor_distancia = distancias[solucao_nova[0]][parte_destruida[i]] + distancias[parte_destruida[i]][solucao_nova[1]] - distancias[solucao_nova[0]][solucao_nova[1]]

            for j in range(2, len(solucao_nova) + 1):
                if j != len(solucao_nova):
                    if (distancias[solucao_nova[j - 1]][parte_destruida[i]] + distancias[parte_destruida[i]][solucao_nova[j]] - distancias[solucao_nova[j - 1]][solucao_nova[j]]) < menor_distancia:
                        melhor_indice = j
                        menor_distancia = distancias[solucao_nova[j - 1]][parte_destruida[i]] + distancias[parte_destruida[i]][solucao_nova[j]] - distancias[solucao_nova[j - 1]][solucao_nova[j]]
                elif (distancias[solucao_nova[j - 1]][parte_destruida[i]] + distancias[parte_destruida[i]][solucao_nova[0]] - distancias[solucao_nova[j - 1]][solucao_nova[0]]) < menor_distancia:
                    melhor_indice = j
                    menor_distancia = distancias[solucao_nova[j - 1]][parte_destruida[i]] + distancias[parte_destruida[i]][solucao_nova[0]] - distancias[solucao_nova[j - 1]][solucao_nova[0]]

            if melhor_indice == len(solucao_nova):
                solucao_nova.append(parte_destruida[i])
            else:
                solucao_nova.insert(melhor_indice, parte_destruida[i])

        solucao_nova, avaliacao_solucao_nova = busca_local(distancias, k, v, solucao_nova)

        if avaliacao_solucao_nova < avaliacao_solucao:
            solucao = solucao_nova.copy()
            avaliacao_solucao = avaliacao_solucao_nova

            if avaliacao_solucao < avaliacao_melhor_solucao:
                melhor_solucao = solucao.copy()
                avaliacao_melhor_solucao = avaliacao_solucao

        fim = time.time()

        if fim - inicio > 300:
            break

    return melhor_solucao, avaliacao_melhor_solucao


def main():
    if len(sys.argv) != 5:
        print("Erro, use: python TSPd-parte3.2.py arquivo tipo k v")
        exit(-1)

    arquivo = open(sys.argv[1], 'r')
    conteudo_arquivo = []

    for linha in arquivo:
        linha = linha.strip()
        conteudo_arquivo.append(linha)

    if sys.argv[2] == "0":
        distancias = ler_tipo_0(conteudo_arquivo)
    elif sys.argv[2] == "1":
        distancias = ler_tipo_1(conteudo_arquivo)
    elif sys.argv[2] == "2":
        distancias = ler_tipo_2(conteudo_arquivo)
    elif sys.argv[2] == "3":
        distancias = ler_tipo_3(conteudo_arquivo)

    k = int(sys.argv[3])
    v = int(sys.argv[4])

    melhor_solucao, avaliacao_melhor_solucao = iterated_greedy(distancias, k, v)

    print(f"{melhor_solucao} = {avaliacao_melhor_solucao}")

    arquivo.close()


if __name__ == "__main__":
    inicio = time.time()
    main()
    fim = time.time()
    print(fim - inicio)
