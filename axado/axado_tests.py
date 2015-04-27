import unittest
from axado import Orcamento
from axado import Tabelas

__author__ = 'Jorge Haddad'


class TestarOrcamentosEmDiferentesFaixasDePeso(unittest.TestCase):

    def teste_orcamento_florianopolis_saopaulo_tabela1_9kilos(self):
        print("Teste do orcamento de frete entre Florianopolis e Sao Paulo, na tabela 1, com pacote de 9 kilos.")
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(9))
        assert "{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA1)) == "122.66"

    def teste_orcamento_florianopolis_saopaulo_tabela1_19kilos(self):
        print("Teste do orcamento de frete entre Florianopolis e Sao Paulo, na tabela 1, com pacote de 19 kilos.")
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(19))
        print("{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA1)))

    def teste_orcamento_florianopolis_saopaulo_tabela1_29kilos(self):
        print("Teste do orcamento de frete entre Florianopolis e Sao Paulo, na tabela 1, com pacote de 29 kilos.")
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(29))
        print("{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA1)))

    def teste_orcamento_florianopolis_saopaulo_tabela1_39kilos(self):
        print("Teste do orcamento de frete entre Florianopolis e Sao Paulo, na tabela 1, com pacote de 39 kilos.")
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(39))
        print("{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA1)))

    def teste_orcamento_florianopolis_saopaulo_tabela2_19kilos(self):
        print("Teste do orcamento de frete entre Florianopolis e Sao Paulo, na tabela 2, com pacote de 19 kilos.")
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(19))
        print("{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA2)))

    def teste_orcamento_florianopolis_saopaulo_tabela2_69kilos(self):
        print("Teste do orcamento de frete entre Florianopolis e Sao Paulo, na tabela 2, com pacote de 69 kilos.")
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(69))
        print("{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA2)))

    def teste_orcamento_florianopolis_saopaulo_tabela2_149kilos(self):
        print("Teste do orcamento de frete entre Florianopolis e Sao Paulo, na tabela 2, com pacote de 149 kilos.")
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(149))
        print("{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA2)))

    def teste_orcamento_florianopolis_saopaulo_tabela2_159kilos(self):
        print("Teste do orcamento de frete entre Florianopolis e Sao Paulo, na tabela 2, com pacote de 159 kilos.")
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(159))
        assert orcamento.calcular_total(Tabelas.TABELA2) == "-"


class TestarLimiteDePeso(unittest.TestCase):

    def testar_peso_fora_do_limite(self):
        print("Teste do limite de peso entre Florianopolis e Curitiba, na tabela 2, com pacote de 159 kilos.")
        orcamento = Orcamento("florianopolis", "curitiba", float(10), float(159))
        assert orcamento.calcular_total(Tabelas.TABELA2) == "-"

if __name__ == '__main__':
    unittest.main()
