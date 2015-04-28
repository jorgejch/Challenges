#! /usr/bin/python3
__author__ = 'Jorge Haddad'
import csv
import sys

# TODO: Colocar PrecoPorKg na Rota.

"""
 Script que calcula o prazo e preço de frete.

    - seguro    = valor da nota fiscal * seguro / 100
    - fixa      = o próprio valor da taxa
    - kg        = define o nome da faixa que é usada para cobrar por kilograma,
                  a faixa é definida no arquivo `preco_por_kg.csv`
    - alfandega = subtotal * (alfandega / 100) (NA TABELA2)
    - ICMS      = valor fixo definido no arquivo `rotas.csv` que deve ser
                  utilizado por último para calcular o total do frete:
                  TOTAL = SUBTOTAL / ((100 - icms) / 100) (SEMPRE 6 PARA TABELA 1)

 Assinatura: axado.py <origem> <destino> <nota_fiscal> <peso>
 Output por tabela:  <nome da pasta>:<prazo>, <frete calculado>
"""


class Tabelas ():
    TABELA1 = 0
    TABELA2 = 1


class Rota:
    def __init__(self, origem, destino, prazo, seguro, kg, icms=6):
        self.origem = origem
        self.destino = destino
        self.prazo = int(prazo)
        self.seguro = float(seguro)
        self.icms = float(icms)
        self.kg = kg

    def calcular_taxas(self, valor_nota):
        return (float(valor_nota) * self.seguro) / 100  # Valor do seguro.


class RotaTabela1(Rota):
    def __init__(self, origem, destino, prazo, seguro, kg, fixa):
        Rota.__init__(self, origem, destino, prazo, seguro, kg)
        self.fixa = float(fixa)

    def calcular_taxas(self, valor_nota: float):
        assert valor_nota is not None
        return super().calcular_taxas(valor_nota) + self.fixa

    def calcular_total(self, preco: float, peso: float, valor_nota: float):
        assert peso is not None
        assert valor_nota is not None

        if preco is None:
            return "-"

        subtotal = ((peso * preco) + self.calcular_taxas(valor_nota))
        return subtotal / ((100 - self.icms) / 100)


class RotaTabela2(Rota):
    def __init__(self, origem, destino, prazo, seguro, kg, limite, alfandega, icms):
        Rota.__init__(self, origem, destino, prazo, seguro, kg, icms)
        self.limite = limite
        self.alfandega = float(alfandega)

    def calcular_total(self, preco: float, peso: float, valor_nota: float):
        if 0 < self.limite < peso:
            return "-"

        if preco is None:
            return "-"

        subtotal = ((peso * preco) + self.calcular_taxas(valor_nota))
        alfandega = subtotal * (self.alfandega / 100)
        return (subtotal + alfandega) / ((100 - self.icms) / 100)


class PrecoPorKg:
    def __init__(self, nome, inicial: float, final: float, preco: float):
        self.nome = nome
        self.inicial = inicial
        self.final = final
        self.preco = preco

    def testar_intervalo(self, peso: float):
        final = (self.final or peso + 1)
        return True if self.inicial <= peso < final else False


class Orcamento:

    def __init__(self, origem: str, destino: str, nota_fiscal: float, peso: float):
        self.origem = origem
        self.destino = destino
        self.nota_fiscal = nota_fiscal
        self.peso = peso

        def carregar_csv(arquivo, delim=','):
            assert arquivo

            with open(arquivo, 'r') as csvfile:
                file = csv.DictReader(csvfile, delimiter=delim, quotechar='|')
                return [row for row in file]

        def gerar_rotas_list(rotas_list: list, opcao_tabela: int):
            assert rotas_list and len(rotas_list) > 0
            assert opcao_tabela is not None

            if opcao_tabela == Tabelas.TABELA1:
                return [RotaTabela1(rota["origem"], rota["destino"], int(rota["prazo"]), float(rota["seguro"]),
                                    rota["kg"], float(rota["fixa"])) for rota in rotas_list]
            elif opcao_tabela == Tabelas.TABELA2:
                return [RotaTabela2(rota["origem"], rota["destino"], int(rota["prazo"]), float(rota["seguro"]), rota["kg"],
                                    float(rota["limite"]), float(rota["alfandega"]), float(rota["icms"]))
                        for rota in rotas_list]

        def gerar_preco_por_kg_list(preco_por_kg_list: list):
            assert preco_por_kg_list and len(preco_por_kg_list) > 0

            return [PrecoPorKg(preco_por_kg["nome"], float(preco_por_kg["inicial"]),
                               float(preco_por_kg["final"]) if preco_por_kg["final"] else None,
                               float(preco_por_kg["preco"])) for preco_por_kg in preco_por_kg_list]

        def obter_rota(rotas_list: list):
            assert rotas_list and len(rotas_list) > 0

            for rota in rotas_list:
                if rota.origem == self.origem and rota.destino == self.destino:
                    return rota

        def obter_preco_por_kg(rota: Rota, precos_por_kg_list: list):
            assert rota
            assert precos_por_kg_list and len(precos_por_kg_list) > 0

            for preco_por_kg in precos_por_kg_list:
                if preco_por_kg.nome == rota.kg and preco_por_kg.testar_intervalo(self.peso):
                    return preco_por_kg.preco

            return None

        self.__rotas_por_tabela__ = []
        self.__precos_por_kg_por_tabela__ = []
        self.rota = []
        self.__preco_por_kg__ = []

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
        self.__precos_por_kg_por_tabela__.append(gerar_preco_por_kg_list(carregar_csv("tabela2/preco_por_kg.tsv", '\t')))
        self.rota.append(obter_rota(self.__rotas_por_tabela__[tabela]))
        self.__preco_por_kg__.append(obter_preco_por_kg(self.rota[tabela],
                                                        self.__precos_por_kg_por_tabela__[tabela]))

    def calcular_total(self, opcao_tabela: int):
        return self.rota[opcao_tabela].calcular_total(self.__preco_por_kg__[opcao_tabela], self.peso,
                                                          self.nota_fiscal)


def gerar_output(orcamento_final: Orcamento, opcao_tabela: int):
    try:
        return "tabela{0}:{1}, {2:.2f}".format(opcao_tabela + 1 if opcao_tabela > 0 else "",
                                               orcamento_final.rota[opcao_tabela].prazo,
                                               orcamento_final.calcular_total(opcao_tabela))
    except:
        return "tabela{0}:{1}, {2}".format(opcao_tabela + 1 if opcao_tabela > 0 else "", "-",
                                           orcamento_final.calcular_total(opcao_tabela))

if __name__ == "__main__":
    orcamento = Orcamento(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))

    print(gerar_output(orcamento, Tabelas.TABELA1))
    print(gerar_output(orcamento, Tabelas.TABELA2))
