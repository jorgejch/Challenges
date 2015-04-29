#! /usr/bin/python3
__author__ = 'Jorge Haddad'
import csv
import sys


"""
 Este programa calcula opções de prazo e preço de frete de acordo com tabelas distintas.


 Assinatura: axado.py <origem> <destino> <nota_fiscal> <peso>
 Output por tabela:  <nome da pasta>:<prazo>, <frete calculado> * Caso nao exista valos disponivel
                                                                                            <nome da pasta>:"-", "-"
"""


class Tabelas:
    TABELA1 = 0
    TABELA2 = 1


class Rota:
    """
    Define um objeto Rota com os elementos basicos de uma rota.
    """

    def __init__(self, origem, destino, prazo, seguro, kg, icms):
        """
        :param origem: str Descrição da origem. Arquivos `rotas.c(t)sv`. Nos arquivos `rotas.c(t)sv`.
        :param destino: str Descrição do destino. Arquivos `rotas.c(t)sv`. Nos arquivos `rotas.c(t)sv`.
        :param prazo: int Dias de prazo para a entrega do frete. Nos arquivos `rotas.c(t)sv`.
        :param seguro: float Taxa do seguro a ser utilizada do valor do seguro (nota_fiscal * seguro / 100).
        Nos arquivos `rotas.c(t)sv`.
        :param kg: str Define o nome da faixa com a taxa a ser utilizada para cobrar por kilograma.
        Nos arquivos `preco_por_kg.c(t)sv`.
        :param icms: float Valor fixo definido no arquivo  que deve ser utilizado no calculo do total. Sendo,
        TOTAL = SUBTOTAL / ((100 - icms) / 100). Nos arquivos `preco_por_kg.c(t)sv`.
        """
        self.origem = origem
        self.destino = destino
        self.prazo = int(prazo)
        self.seguro = float(seguro)
        self.icms = float(icms)
        self.kg = kg

    def calcular_taxas(self, valor_nota):
        """
        Metodo que calcula as taxas a serem aplicadas.
        :param valor_nota: float Valor da nota.
        :returns: float
        """
        assert valor_nota >= 0

        seguro = (float(valor_nota) * self.seguro) / 100  # Valor do seguro.
        return seguro


class RotaTabela1(Rota):
    """
    Implementa um objeto Rota do tipo Tabela1.
    """

    def __init__(self, origem, destino, prazo, seguro, kg, fixa):
        """
        :param origem: Vide Rota.
        :param destino: Vide Rota.
        :param prazo: Vide Rota.
        :param seguro: Vide Rota.
        :param kg: Vide Rota.
        :param fixa: float Taxa fixa a ser cobrada para todos os fretes desta rota. Nos arquivos `rotas.c(t)sv`.
        """
        Rota.__init__(self, origem, destino, prazo, seguro, kg, 6)  # Valor padrão do ICMS para tabela 1 é 6.
        self.fixa = float(fixa)

    def calcular_taxas(self, valor_nota: float):
        """
        Funçao que faz o override da mesma na classe Rota, e adiciona as peculiaridades dessa tabela ao calculo das
        taxas da rota.
        :param valor_nota: float Valor da nota.
        """
        assert valor_nota >= 0
        return super().calcular_taxas(valor_nota) + self.fixa  # A taxa fixa e adicionada.

    def calcular_total(self, preco: float, peso: float, valor_nota: float):
        """
        Funçao que faz o override da mesma na classe Rota, e adiciona as peculiaridades dessa tabela ao calculo do total
        do frete.
        :param preco: float Valor a ser cobrado relativo ao peso do frete.
        :param peso: float Peso do frete.
        :param valor_nota: float Valor da nota.
        :returns: float
        """
        assert peso >= 0
        assert valor_nota >= 0

        if preco is None:
            return "-"

        subtotal = ((peso * preco) + self.calcular_taxas(valor_nota))
        return subtotal / ((100 - self.icms) / 100)


class RotaTabela2(Rota):
    """
    Implementa um objeto Rota do tipo Tabela1.
    """

    def __init__(self, origem, destino, prazo, seguro, kg, limite, alfandega, icms):
        """
        :param origem: Vide Rota.
        :param destino: Vide Rota.
        :param prazo: Vide Rota.
        :param seguro: Vide Rota.
        :param kg: Vide Rota.
        :param limite: float Limite de peso a ser respeitado. Nos arquivos `rotas.c(t)sv`. Nos arquivos `rotas.c(t)sv`.
        :param alfandega: float Valor do parametro alfandega na expressao (subtotal * (alfandega / 100)) que sera
        adicionada a subtotal anterior compondo um novo a ser utilizado do calculo do total.Nos arquivos `rotas.c(t)sv`.
        """
        Rota.__init__(self, origem, destino, prazo, seguro, kg, icms)
        self.limite = limite
        self.alfandega = float(alfandega)

    def calcular_total(self, preco: float, peso: float, valor_nota: float):
        """
        Funçao que faz o override da mesma na classe Rota, e adiciona as peculiaridades dessa tabela ao calculo do total
        do frete.
        :param preco: float Valor a ser cobrado relativo ao peso do frete.
        :param peso: float Peso do frete.
        :param valor_nota: float Valor da nota.
        :returns: float
        """
        if 0 < self.limite < peso:
            return "-"

        if preco is None:
            return "-"

        subtotal = ((peso * preco) + self.calcular_taxas(valor_nota))
        alfandega = subtotal * (self.alfandega / 100)
        return (subtotal + alfandega) / ((100 - self.icms) / 100)


class PrecoPorKg:
    """
    Implementa um objeto PrecoPorKg que representa uma faixa nos arquivos preco_por_kg.c(t)sv`, e testa se um
    valor de peso pertence ao intervalo da faixa.
    """

    def __init__(self, nome, inicial: float, final: float, preco: float):
        """
        :param nome: str Nome da faixa com um valor de preco por kilograma.
        :param inicial: float Peso inicial da faixa.
        :param final: float Peso final da faixa.
        :param preco: float Valor a ser cobrado por kilograma de frete.
        """
        self.nome = nome
        self.inicial = inicial
        self.final = final
        self.preco = preco

    def testar_intervalo(self, peso: float):
        """
        Funcao que testa se um valor de peso pertence ao intervalo da faixa.
        :param peso: Peso do objeto.
        :return: boolean
        """
        final = (self.final or peso + 1)
        return True if self.inicial <= peso < final else False


class Orcamento:
    """
    Implementa um objeto orçamento, com todos os dados de um orçamento de frete em diferentes opçoes de tabela. Retorna
    o calculo do total para uma dada opçao de tabela.
    """

    def __init__(self, origem: str, destino: str, nota_fiscal: float, peso: float):
        """
        :param origem: Vide Rota.
        :param destino: Vide Rota.
        :param nota_fiscal: float Valor da nota.
        :param peso: Peso do objeto.
        """
        self.origem = origem
        self.destino = destino
        self.nota_fiscal = nota_fiscal
        self.peso = peso
        self.rota = []  # Lista que contem um objeto do tipo descendente de Rota para cada opçao de tabela.

        def carregar_csv(arquivo, delim=','):
            """
            Carrega as informações de um arquivo c(t)sv em uma lista.
            :param arquivo: str String com o caminho para o arquivo.
            :param delim: char Caracter delimitador das colunas no arquivo c(t)sv.
            :return: list Lista de dicionários onde as chaves são os cabeçalhos das colunas, e são as Strings nas
            celulas.
            """

            assert arquivo

            with open(arquivo, 'r') as csvfile:
                file = csv.DictReader(csvfile, delimiter=delim, quotechar='|')
                return [row for row in file]

        def gerar_rotas_list(rotas_list: list, opcao_tabela: int):
            """
            Gera uma lista de objetos descendentes de Rota a partir da lista de dicionarios obtida com o
            método carregar_csv().
            :param rotas_list: list Lista de dicionarios obtida com o método carregar_csv().
            :param opcao_tabela: int Opçao de tabela.
            :return: list Lista de objetos Rota de uma determinada tabela.
            """
            assert rotas_list and len(rotas_list) > 0
            assert opcao_tabela is not None

            if opcao_tabela == Tabelas.TABELA1:
                return [RotaTabela1(rota["origem"], rota["destino"], int(rota["prazo"]), float(rota["seguro"]),
                                    rota["kg"], float(rota["fixa"])) for rota in rotas_list]
            elif opcao_tabela == Tabelas.TABELA2:
                return [RotaTabela2(rota["origem"], rota["destino"], int(rota["prazo"]), float(rota["seguro"]),
                                    rota["kg"], float(rota["limite"]), float(rota["alfandega"]), float(rota["icms"]))
                        for rota in rotas_list]

        def gerar_preco_por_kg_list(preco_por_kg_list: list):
            """
            Gera uma lista de objetos PrecoPorKg a partir da lista de dicionarios obtida com o metodo carregar_csv().
            :param preco_por_kg_list: list Lista de dicionarios obtida com o método carregar_csv().
            :return: list Lista de objetos PrecoPorKg de uma determinada tabela.
            """
            assert preco_por_kg_list and len(preco_por_kg_list) > 0

            return [PrecoPorKg(preco_por_kg["nome"], float(preco_por_kg["inicial"]),
                               float(preco_por_kg["final"]) if preco_por_kg["final"] else None,
                               float(preco_por_kg["preco"])) for preco_por_kg in preco_por_kg_list]

        def obter_rota(rotas_list: list):
            """
            Retorna o objeto descendente de Rota em uma dada lista com origem e destino que correspondem os do self.
            :param rotas_list: list Lista de objetos descendentes de Rota.
            :return: Rota
            """
            assert rotas_list and len(rotas_list) > 0

            for rota in rotas_list:
                if rota.origem == self.origem and rota.destino == self.destino:
                    return rota

        def obter_preco_por_kg(rota: Rota, precos_por_kg_list: list):
            """
            Retorna o objeto PrecoPorKg em uma dada lista, com nome da faixa do self e com intervalo contendo o peso do
            self.
            :param rota: Rota O objeto Rota correspondente a lista de PrecoPorKg.
            :param precos_por_kg_list list Lista de objetos PrecoPorKg relativos a uma determinada tabela.
            :return: PrecoPorKg
            """
            assert rota
            assert precos_por_kg_list and len(precos_por_kg_list) > 0

            for preco_por_kg in precos_por_kg_list:
                if preco_por_kg.nome == rota.kg and preco_por_kg.testar_intervalo(self.peso):
                    return preco_por_kg.preco

            return None

        self.__rotas_por_tabela__ = []  # Lista de listas de objetos descendentes de Rota referentes a cada tabela.
        self.__precos_por_kg_por_tabela__ = []  # Listas de listas de objetos PrecoPorKg por tabela.
        self.__preco_por_kg__ = []  # Lista com os valores de preco por kg utilizados para cada tabela.

        # Adição da Tabela 1
        tabela = Tabelas.TABELA1
        self.__rotas_por_tabela__.append(gerar_rotas_list(carregar_csv("tabela/rotas.csv"), tabela))
        self.__precos_por_kg_por_tabela__.append(gerar_preco_por_kg_list(carregar_csv("tabela/preco_por_kg.csv")))
        self.rota.append(obter_rota(self.__rotas_por_tabela__[tabela]))
        self.__preco_por_kg__.append(obter_preco_por_kg(self.rota[tabela],
                                                        self.__precos_por_kg_por_tabela__[tabela]))

        # Adição da Tabela 2
        tabela = Tabelas.TABELA2
        self.__rotas_por_tabela__.append(gerar_rotas_list(carregar_csv("tabela2/rotas.tsv", '\t'), tabela))
        self.__precos_por_kg_por_tabela__.append(
            gerar_preco_por_kg_list(carregar_csv("tabela2/preco_por_kg.tsv", '\t')))
        self.rota.append(obter_rota(self.__rotas_por_tabela__[tabela]))
        self.__preco_por_kg__.append(obter_preco_por_kg(self.rota[tabela],
                                                        self.__precos_por_kg_por_tabela__[tabela]))

    def calcular_total(self, opcao_tabela: int):
        """
        Encapsula a chamada da funcao calcula_total() da tabela selecionada.
        :param opcao_tabela: int Tabela selecionada.
        :return: float
        """
        return self.rota[opcao_tabela].calcular_total(self.__preco_por_kg__[opcao_tabela], self.peso,
                                                      self.nota_fiscal)


def gerar_output(orcamento_final: Orcamento, opcao_tabela: int):
    """
    Cria uma String pronta para ser imprimida m STDOUT.
    :param orcamento_final: Orcamento
    :param opcao_tabela: int Tabela selecionada.
    :return: String formatada.
    """
    try:
        return "tabela{0}:{1}, {2:.2f}".format(opcao_tabela + 1 if opcao_tabela > 0 else "",
                                               orcamento_final.rota[opcao_tabela].prazo,
                                               orcamento_final.calcular_total(opcao_tabela))
    except:
        return "tabela{0}:{1}, {2}".format(opcao_tabela + 1 if opcao_tabela > 0 else "", "-",
                                           orcamento_final.calcular_total(opcao_tabela))


if __name__ == "__main__":
    '''
    Ponto de entrada do programa, quando rodado diretamente.
    '''
    orcamento = Orcamento(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))

    print(gerar_output(orcamento, Tabelas.TABELA1))
    print(gerar_output(orcamento, Tabelas.TABELA2))
