import math
import sys


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


def main():
    if len(sys.argv) != 5:
        print("Erro, use: python TSPd-parte1.2.py arquivo tipo k v")
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

    solucao = [0]
    cidades_nao_visitadas = []

    for i in range(1, len(distancias)):
        cidades_nao_visitadas.append(i)

    qtd_cidades = len(cidades_nao_visitadas)

    i = 0

    while i < qtd_cidades:
        melhor_distancia = math.inf
        melhor_cidade = None
        comeco = None

        for cidade in cidades_nao_visitadas:
            if distancias[cidade][solucao[0]] < melhor_distancia:
                melhor_distancia = distancias[cidade][solucao[0]]
                melhor_cidade = cidade
                comeco = True

        for cidade in cidades_nao_visitadas:
            if distancias[solucao[len(solucao) - 1]][cidade] < melhor_distancia:
                melhor_distancia = distancias[solucao[len(solucao) - 1]][cidade]
                melhor_cidade = cidade
                comeco = False

        if comeco:
            solucao.insert(0, melhor_cidade)
        else:
            solucao.append(melhor_cidade)

        cidades_nao_visitadas.remove(melhor_cidade)

        i = i + 1

    nova_solucao = []

    indice_zero = solucao.index(0)

    for i in range(indice_zero, len(solucao)):
        nova_solucao.append(solucao[i])

    for i in range(indice_zero):
        nova_solucao.append(solucao[i])

    valor_total = 0

    for i in range(len(nova_solucao) - 1):
        valor_total = valor_total + distancias[nova_solucao[i]][nova_solucao[i + 1]]

    valor_total = valor_total + distancias[nova_solucao[len(nova_solucao) - 1]][nova_solucao[0]]

    entregas = []

    k = int(sys.argv[3])
    v = int(sys.argv[4])

    for j in range(1, k + 1):
        entregas.append((2 * j - 1, 2 * j))

    qtd_entregas_realizadas = 0

    for entrega in entregas:
        inicio = nova_solucao.index(entrega[0])
        fim = nova_solucao.index(entrega[1])

        if inicio < fim:
            qtd_entregas_realizadas = qtd_entregas_realizadas + 1

    valor_total = valor_total - qtd_entregas_realizadas * v

    print(f"{nova_solucao} = {valor_total}")

    arquivo.close()


if __name__ == "__main__":
    main()
