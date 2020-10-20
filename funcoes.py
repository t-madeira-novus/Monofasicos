import pandas as pd
import time
from tqdm import tqdm

def removeFirstOccur(string, char):
    string2 = ''
    length = len(string)

    for i in range(length):
        if(string[i] == char):
            string2 = string[0:i] + string[i + 1:length]
            break
    return string2

def virgula_por_ponto(df, coluna):
    """Trocar virgulas por pontos na coluna passada"""
    for i in df.index:
        df.at[i, coluna] = str(df.at[i, coluna]).replace(",", ".")
        if str(df.at[i, coluna]).count(".") > 1:
            df.at[i, coluna] = removeFirstOccur(df.at[i, coluna], ".")

        if pd.isna(df.at[i, coluna]) == True: # se o valor não for nan
            print (df.at[i, coluna])
            df.at[i, coluna] = float(df.at[i, coluna])

    return df

def ponto_por_virgula(df, coluna):
    """Trocar pontos por virgulas na coluna passada"""
    df[coluna] = df[coluna].astype(str)
    for i in df.index:
        # Trocar pontos por virgulas na coluna passada
        df.at[i, coluna] =(df.at[i, coluna].replace(".", ","))

    return df

def adicionar_banco_dados(app):
    global lista_relatorios
    global caminho_salvar_planilha
    global cfops_vendas

    base = pd.read_csv("base_monofasicos.csv", encoding="ISO-8859-1", sep=";")
    base['Descrição'] = base['Descrição'].astype(str)
    base['Data'] = base['Data'].astype(str)
    base['Monofásico?'] = base['Monofásico?'].astype(str)
    j = len(base["Descrição"])

    for relatorio in lista_relatorios:
        df = pd.read_excel(relatorio, encoding='latin-1', sep=';')

        for i in tqdm(df.index):

            try:
                cfop = int(str(df.at[i, "CFOP"]).replace("-", ""))
            except ValueError:
                continue

            descricao = df.at[i, "Descrição"]

            if pd.isna(descricao) == False and descricao != "Descrição" and cfop in cfops_vendas:  # encontrou uma descricao

                if descricao in base["Descrição"].tolist():
                    aux = base["Descrição"].tolist().index(descricao) # posicao do produto na base
                    try:
                        data_base = time.strptime(str(base.at[aux, "Data"]), "%d/%m/%Y %H:%M") # "%Y-%m-%d %H:%M:%S"
                    except:
                        data_base = time.strptime(str(base.at[aux, "Data"]), "%Y-%m-%d %H:%M:%S")  # "%Y-%m-%d %H:%M:%S"
                    data_relatorio = time.strptime(str(df.at[i, "Data"]), "%Y-%m-%d %H:%M:%S")

                    if data_relatorio > data_base:

                        base.at[aux, "NCMs"] = df.at[i, "Unnamed: 12"][4:15] # pega o ncm
                        base.at[aux, "CFOPs"] = round (cfop, 0)
                        base.at[aux, "Descrição"] = descricao

                        if "Produtos Monofásicos" in str(df.at[i, "Unnamed: 12"]):
                            base.at[aux, "Monofásico?"] = "Sim"
                        elif "Produtos Não Monofásicos" in str(df.at[i, "Unnamed: 12"]) :
                            base.at[aux, "Monofásico?"] = "Não"

                        base.to_csv("base_monofasicos.csv", encoding='latin-1', sep=';', index=False)


                else:
                    base.at[j, "NCMs"] = df.at[i, "Unnamed: 12"][4:15] # pega o ncm
                    base.at[j, "CFOPs"] = round (cfop, 0)
                    base.at[j, "Descrição"] = descricao
                    base.at[j, "Data"] = df.at[i, "Data"]

                    if "Produtos Monofásicos" in str(df.at[i, "Unnamed: 12"]):
                        base.at[j, "Monofásico?"] = "Sim"
                    elif "Produtos Não Monofásicos" in str(df.at[i, "Unnamed: 12"]) :
                        base.at[j, "Monofásico?"] = "Não"
                    try:
                        base.to_csv("base_monofasicos.csv", encoding='latin-1', sep=';', index=False)
                    except UnicodeEncodeError:
                        print("Esse cara aqui tá esquisito: " , descricao,  '(linha ' + str(i+2) +', ou talvez ali perto! rs)')
                        return
                    j += 1

            # else:
            #     print ("Não adicionado: ", descricao)


    app.infoBox("Concluído", "Todos os itens dos relatorios foram adicionados à base de dados", parent=None)

def gerar_planilha_monofasicos(app):
    global cfops_vendas
    global planilha_monofasicos
    global adicionar
    global base
    monofasico = 0
    k = 0

    base = pd.read_csv("base_monofasicos.csv", encoding="ISO-8859-1", sep=";")

    for relatorio in lista_relatorios:

        df = pd.read_excel(relatorio, encoding='latin-1', sep=';')
        df = virgula_por_ponto(df, "Valor Produto")

        # for i in df.index:
        for i in tqdm(df.index):

            # if ( i % 200 == 0):
            #     print (i, "/", len(df.index))

            try:
                cfop = int(str(df.at[i, "CFOP"]).replace("-", ""))
            except ValueError:
                continue

            descricao = df.at[i, "Descrição"]
            tam = len(base["Descrição"])
            ncm = df.at[i, "Unnamed: 12"][4:15]  # pega o ncm

            if pd.isna(descricao) == False and descricao != "Descrição"\
            and cfop in cfops_vendas and descricao not in base["Descrição"].tolist(): # encontrou uma descricao nova


                adicionar = app.yesNoBox("Adicionar produto", "O produto "+descricao+", de NCM "+ncm+", não está "
                            "cadastrado no banco de dados. Clique em \"Sim\", caso ele seja monofásico, para "
                            "cadastrá-lo.", parent=None)

                base.at[tam, "NCMs"] = ncm
                base.at[tam, "CFOPs"] = round(cfop, 0)
                base.at[tam, "Descrição"] = descricao

                if adicionar == False:
                    base.at[tam, "Monofásico?"] = "Não"

                elif adicionar == True:
                    base.at[tam, "Monofásico?"] = "Sim"

                t = time.localtime()
                current_time = time.strftime("%d/%m/%Y %H:%M", t)
                base.at[tam, "Data"] = current_time


            base.to_csv("base_monofasicos.csv", encoding='latin-1', sep=';', index=False)

            for j in base.index:
                if base.at[j, 'Monofásico?'] == "Sim" and base.at[j, 'Descrição'] == descricao:
                    monofasico += float(df.at[i, "Valor Produto"])
                    planilha_monofasicos.at[k, "CFOP"] = cfop
                    planilha_monofasicos.at[k, "NCM"] = ncm
                    planilha_monofasicos.at[k, "Descrição"] = descricao
                    planilha_monofasicos.at[k, "Valor Produto"] = str(float(df.at[i, "Valor Produto"])).replace(".", ",")
                    k += 1

        app.infoBox("Valor Final", "O valor dos monofásicos é: R$"+str(monofasico))
        path = app.saveBox(title=None, fileName="Monofásicos de ",
                                              dirName=None, fileExt=".csv", fileTypes=None, asFile=None, parent=None)
        try:
            planilha_monofasicos.to_csv(path, encoding='latin-1', sep=';', index=False)
        except FileNotFoundError:
            app.infoBox("Não salvou", "Planilha não foi salva")