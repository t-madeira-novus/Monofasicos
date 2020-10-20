# Changing the data types of all strings in the module at once
from __future__ import unicode_literals
import pandas as pd
from appJar import gui
from funcoes import adicionar_banco_dados, gerar_planilha_monofasicos


def thread_pegar_relatorios():
    app.thread(pegar_relatorios())

def pegar_relatorios():
    global lista_relatorios
    lista_relatorios = app.openBox(title=None, dirName=None, fileTypes=None, asFile=False, parent=None, multiple=True,
                               mode='r')

def thread_adicionar_banco_dados():
    app.thread(adicionar_banco_dados(app))

def thread_gerar_planilha_monofasicos():
    app.thread(gerar_planilha_monofasicos(app))

def _aux():
    global adicionar
    global base

# def _thread_pegar_caminho_salvar_planilha():
#     app.thread(_pegar_caminho_salvar_planilha)
#
# def _pegar_caminho_salvar_planilha():
#     global caminho_salvar_planilha
#     global planilha_monofasicos
#     caminho_salvar_planilha = app.saveBox(title=None, fileName="base_monofasicos", dirName=None, fileExt=".csv", fileTypes=None, asFile=None, parent=None)
#     base.to_csv(caminho_salvar_planilha, encoding='latin-1', sep=';', index=False)

# Inicialização de variáveis globais
lista_relatorios = []
caminho_salvar_planilha = ""
planilha_monofasicos = pd.DataFrame()
adicionar = False
base = pd.read_csv("base_monofasicos.csv", encoding="ISO-8859-1", sep=";")

cfops_vendas = [5101, 5102, 5103, 5104, 5105, 5106, 5109, 5110, 5111, 5112, 5113, 5114, 5115, 5116, 5117, 5118,
                5119, 5120, 5122, 5123, 5251, 5252, 5253, 5254, 5255, 5256, 5257, 5258, 5301, 5302, 5303, 5304,
                5305, 5306, 5307, 5351, 5352, 5353, 5354, 5355, 5356, 5357, 5359, 5360, 5401, 5402, 5403, 5405,
                5551, 5651, 5652, 5653, 5654, 5655, 5656, 5667, 5922, 5932, 5933, 6101, 6102, 6103, 6104, 6105,
                6106, 6107, 6108, 6109, 6110, 6111, 6112, 6113, 6114, 6115, 6116, 6117, 6118, 6119, 6120, 6122,
                6123, 6251, 6252, 6253, 6254, 6255, 6256, 6257, 6258, 6301, 6302, 6303, 6304, 6305, 6306, 6307,
                6351, 6352, 6353, 6354, 6355, 6356, 6357, 6359, 6360, 6401, 6402, 6403, 6404, 6551, 6651, 6652,
                6653, 6654, 6655, 6656, 6667, 6922, 6932, 6933, 7101, 7102, 7105, 7106, 7127, 7251, 7301, 7358,
                7501, 7551, 7651, 7654, 7667]


# Criando a interface Gráfica
app = gui("que-Fásico")
app.setFont(10)

########################################################################################################################
coluna = 0
linha = 0
app.addButton("Pegar relatórios", thread_pegar_relatorios, row = linha, column = coluna)
linha += 1
app.addButton("Gerar planilha de monofásicos", thread_gerar_planilha_monofasicos, row = linha, column = coluna)
linha += 1

########################################################################################################################
coluna = 1
linha = 0
df = app.addButton("Adicionar produtos ao banco de dados", thread_adicionar_banco_dados, row = linha, column = coluna)
linha += 1

# app.addIconButton("title", _thread_pegar_caminho_salvar_planilha,
#                   "C:\\Users\\thiago.madeira\PycharmProjects\Sequenciador\monofasicos\\folder_selection",
#                   align=None, row = linha, column = coluna)
linha += 1

########################################################################################################################

# start the GUI
app.go()