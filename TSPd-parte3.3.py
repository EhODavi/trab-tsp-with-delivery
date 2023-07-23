import math
import sys
import time

from numpy.random import choice


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


def ACO(d, k, v):
    inicio = time.time()

    melhor_solucao = None
    avaliacao_melhor_solucao = math.inf

    t = []

    for i in range(len(d)):
        t.append([])

        for j in range(len(d)):
            t[i].append(10)

    for i in range(1000):
        melhor_formiga = None
        avaliacao_melhor_formiga = math.inf

        for j in range(30):
            S = []

            for l in range(1, len(d)):
                S.append(l)

            formiga = [0]

            qtd_cidades = len(S)

            l = 0

            while l < qtd_cidades:
                p = []

                total = 0

                for s in S:
                    if d[formiga[-1]][s] == 0:
                        total = total + pow(t[formiga[-1]][s], 0.2)
                    else:
                        total = total + pow(t[formiga[-1]][s], 0.2) / pow(d[formiga[-1]][s], 3)

                for s in S:
                    if d[formiga[-1]][s] == 0:
                        ps = pow(t[formiga[-1]][s], 0.2) / total
                    else:
                        ps = (pow(t[formiga[-1]][s], 0.2) / pow(d[formiga[-1]][s], 3)) / total

                    p.append(ps)

                cidade_escolhida = choice(a=S, p=p)

                formiga.append(cidade_escolhida)
                S.remove(cidade_escolhida)

                l = l + 1

            avaliacao_formiga = avalia_solucao(formiga, d, k, v)

            if avaliacao_formiga < avaliacao_melhor_formiga:
                melhor_formiga = formiga.copy()
                avaliacao_melhor_formiga = avaliacao_formiga

        for j in range(len(t)):
            for l in range(len(t)):
                t[j][l] = (1 - 0.05) * t[j][l]

        melhor_formiga, avaliacao_melhor_formiga = busca_local(d, k, v, melhor_formiga)

        for j in range(len(melhor_formiga) - 1):
            t[melhor_formiga[j]][melhor_formiga[j + 1]] = t[melhor_formiga[j]][melhor_formiga[j + 1]] + 1 / avaliacao_melhor_formiga

        t[melhor_formiga[-1]][melhor_formiga[0]] = t[melhor_formiga[-1]][melhor_formiga[0]] + 1 / avaliacao_melhor_formiga

        if avaliacao_melhor_formiga < avaliacao_melhor_solucao:
            melhor_solucao = melhor_formiga.copy()
            avaliacao_melhor_solucao = avaliacao_melhor_formiga

        fim = time.time()

        if fim - inicio > 300:
            break

    return melhor_solucao, avaliacao_melhor_solucao


def main():
    if len(sys.argv) != 5:
        print("Erro, use: python TSPd-parte3.3.py arquivo tipo k v")
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

    melhor_solucao, avaliacao_melhor_solucao = ACO(distancias, k, v)

    print(f"{melhor_solucao} = {avaliacao_melhor_solucao}")

    arquivo.close()


if __name__ == "__main__":
    inicio = time.time()
    main()
    fim = time.time()
    print(fim - inicio)
