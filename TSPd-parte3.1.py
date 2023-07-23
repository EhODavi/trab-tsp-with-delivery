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


def solucao_aleatoria_gulosa(distancias, alpha):
    solucao = [0]
    cidades_nao_visitadas = []

    for i in range(1, len(distancias)):
        cidades_nao_visitadas.append(i)

    qtd_cidades = len(cidades_nao_visitadas)

    i = 0

    while i < qtd_cidades:
        avaliacoes = []

        for cidade in cidades_nao_visitadas:
            avaliacoes.append((cidade, distancias[solucao[len(solucao) - 1]][cidade]))

        avaliacoes.sort(key=lambda x: x[1])

        LRC = max(1, int(alpha * len(cidades_nao_visitadas)))

        melhores_avaliacoes = []

        for j in range(LRC):
            melhores_avaliacoes.append(avaliacoes[j])

        escolhido = random.choice(melhores_avaliacoes)

        solucao.append(escolhido[0])
        cidades_nao_visitadas.remove(escolhido[0])

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


def GRASP(distancias, k, v):
    melhor_solucao = None
    avaliacao_melhor_solucao = None

    inicio = time.time()

    for i in range(100):
        solucao = solucao_aleatoria_gulosa(distancias, 0.05)
        solucao, avaliacao_solucao = busca_local(distancias, k, v, solucao)

        if i == 0:
            melhor_solucao = solucao
            avaliacao_melhor_solucao = avaliacao_solucao
        elif avaliacao_solucao < avaliacao_melhor_solucao:
            melhor_solucao = solucao
            avaliacao_melhor_solucao = avaliacao_solucao

        fim = time.time()

        if fim - inicio > 300:
            break

    return melhor_solucao, avaliacao_melhor_solucao


def main():
    if len(sys.argv) != 5:
        print("Erro, use: python TSPd-parte3.1.py arquivo tipo k v")
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

    melhor_solucao, avaliacao_melhor_solucao = GRASP(distancias, k, v)

    print(f"{melhor_solucao} = {avaliacao_melhor_solucao}")

    arquivo.close()


if __name__ == "__main__":
    inicio = time.time()
    main()
    fim = time.time()
    print(fim - inicio)
