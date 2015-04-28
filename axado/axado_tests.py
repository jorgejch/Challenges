import unittest
from axado import Orcamento
from axado import Tabelas
from axado import gerar_output
__author__ = 'Jorge Haddad'


class TestarPrazos(unittest.TestCase):

    def teste_prazo_orcamento_tabela1(self):
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(9))
        prazo = orcamento.rota[Tabelas.TABELA1].prazo
        print("Teste do prazo para frete entre Florianopolis e Sao Paulo, na tabela 1. Resultado: {0}".format(prazo))
        assert prazo == 4

    def teste_prazo_orcamento_tabela2(self):
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(9))
        prazo = orcamento.rota[Tabelas.TABELA2].prazo
        print("Teste do prazo para frete entre Florianopolis e Sao Paulo, na tabela 1. Resultado: {0}".format(prazo))
        assert prazo == 3


class TestarCalculoTotalEmDiferentesFaixasDePeso(unittest.TestCase):

    def teste_calculo_total_florianopolis_saopaulo_tabela1_9kilos(self):
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(9))
        resultado = "{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA1))
        print("Teste do calculo total do frete entre Florianopolis e Sao Paulo, na tabela 1, com pacote de 9 kilos. " +
              "Resultado: {0}".format(resultado))
        assert resultado == "122.66"

    def teste_calculo_total_florianopolis_saopaulo_tabela1_19kilos(self):
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(19))
        resultado = "{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA1))
        print("Teste do calculo total do frete entre Florianopolis e Sao Paulo, na tabela 1, com pacote de 19 kilos. " +
              "Resultado: {0}".format(resultado))
        assert resultado == "230.11"

    def teste_calculo_total_florianopolis_saopaulo_tabela1_29kilos(self):
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(29))
        resultado = "{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA1))
        print("Teste do calculo total do frete entre Florianopolis e Sao Paulo, na tabela 1, com pacote de 29 kilos. " +
                "Resultado: {0}".format(resultado))
        assert resultado == "316.28"

    def teste_calculo_total_florianopolis_saopaulo_tabela1_39kilos(self):
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(39))
        resultado = "{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA1))
        print("Teste do calculo total do frete entre Florianopolis e Sao Paulo, na tabela 1, com pacote de 39 kilos. " +
              "Resultado: {0}".format(resultado))
        assert resultado == "215.21"

    def teste_calculo_total_florianopolis_saopaulo_tabela2_19kilos(self):
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(19))
        resultado = "{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA2))
        print("Teste do calculo total do frete entre Florianopolis e Sao Paulo, na tabela 2, com pacote de 19 kilos. " +
              "Resultado: {0}".format(resultado))
        assert resultado == "314.35"

    def teste_calculo_total_florianopolis_saopaulo_tabela2_69kilos(self):
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(69))
        resultado = "{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA2))
        print("Teste do calculo total do frete entre Florianopolis e Sao Paulo, na tabela 2, com pacote de 69 kilos. " +
              "Resultado: {0}".format(resultado))
        assert resultado == "1062.05"

    def teste_calculo_total_florianopolis_saopaulo_tabela2_149kilos(self):
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(149))
        resultado = "{0:.2f}".format(orcamento.calcular_total(Tabelas.TABELA2))
        print("Teste do calculo total do frete entre Florianopolis e Sao Paulo, na tabela 2, com pacote de 149 kilos. " +
              "Resultado: {0}".format(resultado))
        assert resultado == "2123.19"

    def teste_calculo_total_florianopolis_saopaulo_tabela2_159kilos(self):
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(159))
        resultado = orcamento.calcular_total(Tabelas.TABELA2)
        print("Teste do calculo total do frete entre Florianopolis e Sao Paulo, na tabela 2, com pacote de 159 kilos. " +
              "Resultado: {0}".format(resultado))
        assert resultado == "-"


class TestarOutput(unittest.TestCase):

    def testar_output_tabela1(self):
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(9))
        resultado = orcamento.calcular_total(Tabelas.TABELA1)
        prazo = orcamento.rota[Tabelas.TABELA1].prazo
        output_esperado = "tabela:{0}, {1:.2f}".format(prazo, resultado)
        output_obtido = gerar_output(orcamento, Tabelas.TABELA1)
        print("Teste output_esperado com resultado do calculo do frete entre Florianopolis e Sao Paulo, na tabela 1," +
              " com pacote de 9 kilos. Output obtido: {0}; Output esperado: {1}".format(output_obtido, output_esperado))
        assert output_obtido == output_esperado

    def testar_output_tabela2_resultado_ok(self):
        orcamento = Orcamento("florianopolis", "saopaulo", float(10), float(9))
        resultado = orcamento.calcular_total(Tabelas.TABELA2)
        prazo = orcamento.rota[Tabelas.TABELA2].prazo
        output_esperado = "tabela2:{0}, {1:.2f}".format(prazo, resultado)
        output_obtido = gerar_output(orcamento, Tabelas.TABELA2)
        print("Teste output com resultado do calculo do frete entre Florianopolis e Sao Paulo, na tabela 2," +
              " com pacote de 9 kilos. Output obtido: {0}; Output esperado: {1}".format(output_obtido, output_esperado))
        assert output_obtido == output_esperado

    def testar_output_tabela2_resultado_indisponivel(self):
        orcamento = Orcamento("florianopolis", "curitiba", float(10), float(70.01))
        resultado = orcamento.calcular_total(Tabelas.TABELA2)
        output_esperado = "tabela2:{0}, {1}".format("-", resultado)
        output_obtido = gerar_output(orcamento, Tabelas.TABELA2)
        print("Teste output com resultado do calculo do frete entre Florianopolis e Curitiba, na tabela 2," +
              " com pacote de 70.01 kilos. Output obtido: {0}; Output esperado: {1}".
              format(output_obtido, output_esperado))
        assert output_obtido == output_esperado


class TestarLimiteDePeso(unittest.TestCase):

    def testar_peso_dentro_do_limite(self):
        orcamento = Orcamento("florianopolis", "curitiba", float(10), float(70))
        resultado = orcamento.calcular_total(Tabelas.TABELA2)
        print("Teste do limite de peso entre Florianopolis e Curitiba, na tabela 2, com pacote de 70 kilos. " +
              "Resultado: {0}".format(resultado))
        assert resultado != "-"

    def testar_peso_fora_do_limite(self):
        orcamento = Orcamento("florianopolis", "curitiba", float(10), float(70.01))
        resultado = orcamento.calcular_total(Tabelas.TABELA2)
        print("Teste do limite de peso entre Florianopolis e Curitiba, na tabela 2, com pacote de 70.01 kilos. " +
              "Resultado: {0}".format(resultado))
        assert resultado == "-"

if __name__ == '__main__':
    unittest.main()
