import csv
from datetime import datetime
from time import sleep
from tabulate import tabulate
import pandas as pd


saudacaoInicial = ('''------------------------------------------------------------------
------------- BEM-VINDO AO BANCO DE DADOS DO SIGVIG3 --------------
------------------------------------------------------------------''')

menuGeral = True

while menuGeral:

    print(saudacaoInicial)

    operacao = int(input('''Qual o tipo de operação deseja pesquisar: exportação ou importação?
Digite [1] para exportação
Digite [2] para importação
Digite [3] para relatório geral por período
Digite [4] para sair da aplicação
-------------------------------------------------------------------\n'''))

    usoPropostoVegetal = (
    "produto vegetal para consumo direto", "embalagem e suportes de madeira", "material de pesquisa de origem vegetal",
    "agente para controle biológico", "vinhos e derivados da uva e do vinho", "máquinas agrícolas",
    "produto vegetal industrializado", "produto vegetal in natura", "agrotóxico", "material para propagação vegetal",
    "fertilizante", "bebidas em geral", "corretivo", "inoculante")

    usoPropostoAnimal = (
    "animal vivo doméstico de companhia", "animal vivo para cria", "animal vivo para abate", "animal vivo para engorda",
    "produto de origem animal comestível", "outros produtos destinados à alimentação animal",
    "animal vivo para esporte", "animal vivo para exposição e espetáculo", "animal vivo para pesquisa",
    "animal vivo para reprodução", "animal vivo para zoológico", "material de pesquisa de origem animal",
    "material de multiplicação animal",
    "produto de uso veterinário", "produto biológico", "produto de origem animal não comestível para industrialização",
    "produto de origem animal não comestível para fins opoterápicos", "troféu de caça e taxidermia",
    "produto de origem vegetal destinado à alimentação animal")

    arquivo_1 = 'extracao_dados_pov.csv'
    arquivo_2 = 'extracao_dados_impo_pov.csv'
    arquivo_3 = 'extracao_dados_poa.csv'
    arquivo_4 = 'sigvig3_fitos.csv'

    menuAnimalVegetal = True

    while menuAnimalVegetal:

        if operacao == 1:

            area = int(input('''Qual área agropecuária deseja pesquisar?
Digite [1] para animal
Digite [2] para vegetal
Digite [3] para sair\n'''))

            if area == 1:

                menuAnimal = True

                while menuAnimal:

                    # Utilizar data no formato dd/mm/aa
                    dataInicio = input("Qual a data do início do período de pesquisa? Usar formato dd/mm/aa\n")
                    dataFim = input("Qual a data do final do período de pesquisa? Usar formato dd/mm/aa\n")

                    produto = input("Qual produto deseja pesquisar na base de dados?\n").lower()

                    perguntaPais = input("Deseja pesquisa combinada por país? Tecle 'S' para 'Sim'\n").lower()

                    if perguntaPais == 's':
                        pais = input("Qual país deseja pesquisar?\n")

                    else:
                        pais = 'NÃO'

                    def buscaExportacaoAnimal(dataInicio, dataFim, produto, pais):

                        minhaDataInicio = datetime.strptime(dataInicio, "%d/%m/%y")
                        minhaDataFim = datetime.strptime(dataFim, "%d/%m/%y")

                        tabela1 = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_3}'))
                        c = 0
                        nea = 0
                        neap = 0
                        deferido = 0
                        indeferido = 0

                        for linha in tabela1:
                            mercadoria = linha[18]
                            paisDestino = linha[24]
                            status = linha[15]
                            if linha[5] != "Data de Recebimento":
                                dataRecebimento = linha[5][0:8]
                                minhaDataRecebimento = datetime.strptime(dataRecebimento, "%d/%m/%y")
                                if minhaDataInicio <= minhaDataRecebimento <= minhaDataFim:
                                    c += 1
                                if perguntaPais == 's':
                                    if minhaDataInicio <= minhaDataRecebimento <= minhaDataFim and produto in mercadoria.lower() and pais in paisDestino.lower():
                                        neap += 1
                                        if status == 'DEFERIDO':
                                            deferido += 1
                                        elif status == 'INDEFERIDO':
                                            indeferido += 1
                                else:
                                    if minhaDataInicio <= minhaDataRecebimento <= minhaDataFim and produto in mercadoria.lower():
                                        nea += 1
                                        if status == 'DEFERIDO':
                                            deferido += 1
                                        elif status == 'INDEFERIDO':
                                            indeferido += 1

                        if perguntaPais == 's':
                            print('----------------------------------------------------')
                            print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                            print('----------------------------------------------------')
                            print(f'Data inicial de busca: {dataInicio}')
                            print(f'Data final de busca: {dataFim}')
                            tabelaFinal = [['Tipo de Operação', 'Expressão de busca', 'País de destino', 'Número total de LPCOs',
                                            f'Número total de LPCOs \ncom a expressão \n{produto.upper()} \nna descrição do produto e para o país pesquisado', 'LPCOs deferidas', 'LPCOs indeferidas'],
                                           ['Exportação Animal', produto.upper(), pais.upper(), c, neap, deferido, indeferido]]
                            print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

                        else:

                            print('----------------------------------------------------')
                            print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                            print('----------------------------------------------------')
                            print(f'Data inicial de busca: {dataInicio}')
                            print(f'Data final de busca: {dataFim}')
                            tabelaFinal = [['Tipo de Operação', 'Expressão de busca','Número total de LPCOs',
                                            f'Número total de LPCOs \ncom a expressão \n{produto.upper()} \nna descrição do produto', 'LPCOs deferidas', 'LPCOs indeferidas'],
                                           ['Exportação Animal', produto.upper(), c, nea, deferido, indeferido]]
                            print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))


                    buscaExportacaoAnimal(dataInicio, dataFim, produto, pais)

                    pergunta1 = input("Deseja voltar ao menu da Exportação Animal?\nDigite 'S' para voltar:\n").lower()

                    if pergunta1 != 's':
                        menuAnimal = False

                sleep(1)

            elif area == 2:

                menuVegetal = True

                while menuVegetal:

                    tipoPesquisa = int(input('''Qual o tipo de pesquisa deseja fazer?
Digite [1] para pesquisar quantas LPCOs foram registradas na base de dados.
Digite [2] para pesquisar quantos CF válidos foram registrados na base de dados.
Digite [3] para pesquisar quantos CF válidos existem na base de dados por AFFA.
Digite [4] para pesquisar quantos CF válidos existem na base de dados por países de destino.
Digite [5] para pesquisar quantos CF válidos emitidos por Unidade Vigiagro existem na base de dados.
Digite [6] para realizar pesquisas combinadas por AFFA e país de destino.
Digite [7] para realizar pesquisas combinadas por produto, país de destino e períodos.
Digite [8] para realizar pesquisas combinadas por uso proposto, país de destino e períodos.
Digite [9] para retornar ao menu principal.\n'''))

                    if tipoPesquisa == 1:

                        produto = input("Qual produto deseja pesquisar na base de dados?\n").lower()

                        def buscaExportacaoPorQuantidade(produto):

                            tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_1}'))
                            c = 0
                            p = 0

                            for linha in tabela:
                                c += 1
                                mercadoria = linha[22]
                                if produto in mercadoria.lower():
                                    p += 1
                            print('----------------------------------------------------')
                            print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                            print('----------------------------------------------------')
                            tabelaFinal = [['Tipo de Operação', 'Número total de LPCOs',
                                            f'Número total de LPCOs \ncom a expressão {produto.upper()} \nna descrição do produto'],
                                           ['Exportação Vegetal', c, p]]
                            print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

                            if p == 0:
                                print("Não foram encontradas LPCOs contendo a expressão {} na base de dados.".format(produto.upper()))

                        buscaExportacaoPorQuantidade(produto)

                        pergunta2 = input("Deseja voltar ao menu da Exportação Vegetal?\nDigite 'S' para voltar:\n").lower()

                        sleep(1)

                        if pergunta2 != 's':
                            menuVegetal = False

                    elif tipoPesquisa == 2:

                        def buscaExportacaoVegetalCFTotal():

                            tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_4}'))
                            cont = 0

                            for linha in tabela:
                                dados = linha[2]
                                if dados == 'VALIDO':
                                    cont += 1
                            print('----------------------------------------------------')
                            print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                            print('----------------------------------------------------')
                            tabelaFinal = [['Tipo de Operação', 'Número de CF emitidos'],
                                           ['Exportação Vegetal', cont]]
                            print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

                        buscaExportacaoVegetalCFTotal()

                        pergunta3 = input(
                            "Deseja voltar ao menu da Exportação Vegetal?\nDigite 'S' para voltar:\n").lower()

                        sleep(1)

                        if pergunta3 != 's':
                            menuVegetal = False

                    elif tipoPesquisa == 3:

                        qualFiscal = input("Qual AFFA deseja pesquisar na base de dados?\n").lower()

                        def buscaExportacaoVegetalPorFiscal(fiscal):

                            tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_4}'))
                            f = 0
                            nomeCompleto = ""

                            for linha in tabela:
                                dados = linha[3]
                                if fiscal in dados.lower() and linha[2] == 'VALIDO':
                                    f += 1
                                    nomeCompleto = f"{dados}"
                            print('----------------------------------------------------')
                            print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                            print('----------------------------------------------------')
                            tabelaFinal = [['Tipo de Operação', 'Nome do AFFA',
                                            'Número de CF emitidos'],
                                           ['Exportação Vegetal', nomeCompleto, f]]
                            print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

                            if f == 0:
                                print("Não foram encontrados CF emitidos pelo(a) AFFA {} na base de dados.".format(fiscal.upper()))


                        buscaExportacaoVegetalPorFiscal(qualFiscal)

                        pergunta3 = input("Deseja voltar ao menu da Exportação Vegetal?\nDigite 'S' para voltar:\n").lower()

                        sleep(1)

                        if pergunta3 != 's':
                            menuVegetal = False

                    elif tipoPesquisa == 4:

                        qualPais = input("Qual o país de destino deseja pesquisar na base de dados?\n").lower()

                        def buscaExportacaoPorPais(pais):

                            tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_4}'))
                            p = 0
                            nomePais = ""

                            for linha in tabela:
                                dados = linha[10]
                                if pais in dados.lower():
                                    p += 1
                                    nomePais = f"{dados}"
                            print('----------------------------------------------------')
                            print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                            print('----------------------------------------------------')
                            tabelaFinal = [['Tipo de Operação', 'País de destino',
                                            'Número total de CF'],
                                           ['Exportação Vegetal', nomePais, p]]
                            print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

                            if p == 0:
                                print("Não foram encontradas LPCOs emitidas contendo o país de destino {} na base de dados.".format(
                                    pais.upper()))

                        buscaExportacaoPorPais(qualPais)

                        sleep(1)

                        pergunta4 = input("Deseja voltar ao menu da Exportação Vegetal?\nDigite 'S' para voltar:\n").lower()

                        if pergunta4 != 's':
                            menuVegetal = False

                    elif tipoPesquisa == 5:

                        unidades = {
                            'V034 - VIGIAGRO PARANAGUÁ - PR': [
                                'SERVIÇO DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PARANAGUÁ-PR', 0],
                            'V064 - VIGIAGRO SANTOS - SP': [
                                'SERVIÇO DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SANTOS-SP', 0],
                            'V032 - VIGIAGRO FOZ DO IGUAÇU - PR': [
                                'SERVIÇO DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE FOZ DO IGUAÇU-PR',
                                0],
                            'V055 - VIGIAGRO URUGUAIANA - RS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE URUGUAIANA-RS', 0],
                            'V052 - VIGIAGRO RIO GRANDE - RS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE RIO GRANDE-RS', 0],
                            'V020 - VIGIAGRO CORUMBÁ - MS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE CORUMBÁ-MS', 0],
                            'V029 - VIGIAGRO SUAPE - PE': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SUAPE-PE',
                                0],
                            'V054 - VIGIAGRO SÃO BORJA - RS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SAO BORJA-RS', 0],
                            'V045 - VIGIAGRO ACEGUÁ-BAGÉ - RS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ACEGUÁ-BAGE-RS',
                                0],
                            'V061 - VIGIAGRO SÃO FRANCISCO DO SUL - SC': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SAO FRANCISCO DO SUL-SC',
                                0],
                            'V026 - VIGIAGRO VILA DO CONDE - PA': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE VILA DO CONDE-PA',
                                0],
                            'V058 - VIGIAGRO ITAJAÍ - SC': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ITAJAI-SC',
                                0],
                            'V017 - VIGIAGRO ITAQUÍ-MADEIRA - MA': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ITAQUI-MADEIRA-MA',
                                0],
                            'V049 - VIGIAGRO PORTO ALEGRE - RS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PORTO ALEGRE-RS',
                                0],
                            'V010 - VIGIAGRO SALVADOR - BA': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SALVADOR-BA', 0],
                            'V024 - VIGIAGRO BELÉM - PA': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE BELÉM-PA',
                                0],
                            'V060 - VIGIAGRO ITAPOÁ - SC': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ITAPOA-SC',
                                0],
                            'V063 - VIGIAGRO GUARULHOS - SP': [
                                'SERVIÇO DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE GUARULHOS-SP', 0],
                            'V028 - VIGIAGRO RECIFE - PE': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE RECIFE-PE',
                                0],
                            'U040 - UTRA CAMPINAS - SP': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA EM CAMPINAS - SP',
                                                          0],
                            'V015 - VIGIAGRO VITÓRIA - ES': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE VITORIA-ES', 0],
                            'U046 - UTRA REGIÃO METROPOLITANA - SP': [
                                'UNIDADE TECNICA REGIONAL DE AGRICULTURA DA REGIAO METROPOLITANA - SP', 0],
                            'V053 - VIGIAGRO SANTANA DO LIVRAMENTO - RS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SANTANA DO LIVRAMENTO-RS',
                                0],
                            'U034 - UTRA CAXIAS DO SUL - RS': [
                                'UNIDADE TECNICA REGIONAL DE AGRICULTURA DE CAXIAS DO SUL - RS', 0],
                            'V046 - VIGIAGRO CHUÍ - RS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE CHUI-RS', 0],
                            'V051 - VIGIAGRO QUARAÍ - RS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE QUARAÍ-RS',
                                0],
                            'V039 - VIGIAGRO NATAL - RN': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE NATAL-RN',
                                0],
                            'V048 - VIGIAGRO JAGUARÃO - RS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE JAGUARAO-RS', 0],
                            'SF21 - SFA - RIO GRANDE DO SUL': [
                                'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO RIO GRANDE DO SUL', 0],
                            'V059 - VIGIAGRO IMBITUBA - SC': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE IMBITUBA-SC', 0],
                            'V056 - VIGIAGRO DIONÍSIO CERQUEIRA - SC': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE DIONÍSIO CERQUEIRA-SC',
                                0],
                            'V047 - VIGIAGRO ITAQUÍ - RS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ITAQUI-RS',
                                0],
                            'V013 - VIGIAGRO PECÉM - CE': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DO PECEM-CE',
                                0],
                            'V050 - VIGIAGRO PORTO XAVIER - RS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PORTO XAVIER-RS',
                                0],
                            'V025 - VIGIAGRO SANTARÉM - PA': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SANTAREM-PA', 0],
                            'V003 - VIGIAGRO MACEIÓ - AL': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE MACEIO-AL',
                                0],
                            'V030 - VIGIAGRO VALE DO SÃO FRANCISCO - PE': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DO VALE DO SÃO FRANCISCO-PE',
                                0],
                            'V036 - VIGIAGRO ITAGUAÍ - RJ': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ITAGUAÍ-RJ', 0],
                            'V038 - VIGIAGRO PORTO DO RIO DE JANEIRO - RJ': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL PORTO DO RIO DE JANEIRO-RJ',
                                0],
                            'U041 - UTRA FAZENDA IPANEMA - SP': [
                                'UNIDADE TECNICA REGIONAL DE AGRICULTURA NA FAZENDA IPANEMA - SP', 0],
                            'V065 - VIGIAGRO VIRACOPOS - SP': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE VIRACOPOS-SP', 0],
                            'V005 - VIGIAGRO MANAUS - AM': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE MANAUS-AM',
                                0],
                            'V018 - VIGIAGRO CONFINS - MG': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE CONFINS-MG', 0],
                            'U018 - UTRA UBERLÂNDIA - MG': [
                                'UNIDADE TECNICA REGIONAL DE AGRICULTURA DE UBERLANDIA - MG', 0],
                            'V002 - VIGIAGRO EPITACIOLÂNDIA - AC': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE EPITACIOLANDIA-AC',
                                0],
                            'U023 - UTRA SANTARÉM - PA': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA DE SANTAREM - PA',
                                                          0],
                            'V031 - VIGIAGRO CURITIBA - PR': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE CURITIBA-PR', 0],
                            'U017 - UTRA UBERABA - MG': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA DE UBERABA - MG', 0],
                            'U019 - UTRA VARGINHA - MG': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA DE VARGINHA - MG',
                                                          0],
                            'V062 - VIGIAGRO ARACAJÚ - SE': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ARACAJU-SE', 0],
                            'SF25 - SFA - SÃO PAULO': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE SÃO PAULO',
                                                       0],
                            'V021 - VIGIAGRO PONTA PORÃ - MS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PONTA PORÃ-MS', 0],
                            'V012 - VIGIAGRO FORTALEZA - CE': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE FORTALEZA-CE', 0],
                            'V037 - VIGIAGRO GALEÃO - RJ': [
                                'SERVIÇO DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DO GALEÃO-RJ', 0],
                            'SFA - PARANÁ': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO PARANÁ', 0],
                            'SF16 - SFA - PARANÁ': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO PARANÁ', 0],
                            'U042 - UTRA GUARATINGUETÁ - SP': [
                                'UNIDADE TECNICA REGIONAL DE AGRICULTURA EM GUARATINGUETA - SP', 0],
                            'VIGIAGRO URUGUAIANA - RS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE URUGUAIANA-RS', 0],
                            'V040 - VIGIAGRO GUAJARÁ-MIRIM - RO': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE GUAJARA MIRIM-RO',
                                0],
                            'VIGIAGRO ACEGUÁ-BAGÉ - RS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ACEGUÁ-BAGE-RS',
                                0],
                            'VIGIAGRO PARANAGUÁ - PR': [
                                'SERVIÇO DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PARANAGUÁ-PR', 0],
                            'V023 - VIGIAGRO CUIABÁ - MT': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE CUIABÁ-MT',
                                0],
                            'V004 - VIGIAGRO AEROPORTO DE MANAUS - AM': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL AEROPORTO DE MANAUS-AM',
                                0],
                            'SF08 - SFA - ESPÍRITO SANTO': [
                                'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO NO ESPÍRITO SANTO', 0],
                            'SF10 - SFA - MARANHÃO': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO MARANHÃO',
                                                      0],
                            'SF19 - SFA - RIO DE JANEIRO': [
                                'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO RIO DE JANEIRO', 0],
                            'V011 - VIGIAGRO AEROPORTO DE FORTALEZA - CE': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE AEROPORTO DE FORTALEZA-CE',
                                0],
                            'U039 - UTRA BOTUCATU - SP': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA DE BOTUCATU - SP',
                                                          0],
                            'V057 - VIGIAGRO FLORIANÓPOLIS - SC': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE FLORIANOPOLIS-SC',
                                0],
                            'SF14 - SFA - PARÁ': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO PARÁ', 0],
                            'V027 - VIGIAGRO CABEDELO - PB': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE CABEDELO-PB', 0],
                            'SF24 - SFA - SANTA CATARINA': [
                                'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE SANTA CATARINA', 0],
                            'SF26 - SFA - SERGIPE': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE SERGIPE', 0],
                            'V043 - VIGIAGRO BONFIM - RR': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE BONFIM-RR',
                                0],
                            'SF13 - SFA - MINAS GERAIS': [
                                'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE MINAS GERAIS', 0],
                            'SF17 - SFA - PERNAMBUCO': [
                                'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE PERNAMBUCO', 0],
                            'SF11 - SFA - MATO GROSSO': [
                                'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE MATO GROSSO', 0],
                            'SF06 - SFA - CEARÁ': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO CEARÁ', 0],
                            'SF12 - SFA - MATO GROSSO DO SUL': [
                                'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE MATO GROSSO DO SUL',
                                0],
                            'U010 - UTRA DIVINÓPOLIS - MG': [
                                'UNIDADE TECNICA REGIONAL DE AGRICULTURA EM DIVINOPOLIS - MG', 0],
                            'U005 - UTRA VITÓRIA DA CONQUISTA - BA': [
                                'UNIDADE TECNICA REGIONAL DE AGRICULTURA DE VITORIA DA CONQUISTA - BA', 0],
                            'SF03 - SFA - AMAZONAS': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO AMAZONAS',
                                                      0],
                            'SF20 - SFA - RIO GRANDE DO NORTE': [
                                'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO RIO GRANDE DO NORTE',
                                0],
                            'U011 - UTRA JUIZ DE FORA - MG': [
                                'UNIDADE TECNICA REGIONAL DE AGRICULTURA JUIZ DE FORA - MG', 0],
                            'SF05 - SFA - BAHIA': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DA BAHIA', 0],
                            'SF15 - SFA - PARAÍBA': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DA PARAÍBA', 0],
                            'SF01 - SFA - ACRE': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO ACRE', 0],
                            'V016 - VIGIAGRO ANÁPOLIS - GO': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ANÁPOLIS-GO', 0],
                            'SF09 - SFA - GOIÁS': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE GOIÁS', 0],
                            'U024 - UTRA CAMPINA GRANDE - PB': [
                                'UNIDADE TECNICA REGIONAL DE AGRICULTURA DE CAMPINA GRANDE - PB', 0],
                            'V041 - VIGIAGRO PORTO VELHO - RO': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PORTO VELHO-RO',
                                0],
                            'V014 - VIGIAGRO BRASÍLIA - DF': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE BRASILIA-DF', 0],
                            'U013 - UTRA MONTES CLAROS - MG': [
                                'UNIDADE TECNICA REGIONAL DE AGRICULTURA EM MONTES CLAROS - MG', 0],
                            'SF02 - SFA - ALAGOAS': ['SUPERINTENDÊCIA FEDERAL DE AGRICULTURA NO ESTADO DE ALAGOAS', 0],
                            'V001 - VIGIAGRO ASSIS BRASIL - AC': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ASSIS BRASIL-AC',
                                0],
                            'SF07 - SFA - DISTRITO FEDERAL': [
                                'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO DISTRITO FEDERAL', 0],
                            'V035 - VIGIAGRO SANTA HELENA - PR': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SANTA HELENA-PR',
                                0],
                            'U037 - UTRA ARAÇATUBA - SP': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA EM ARACATUBA - SP',
                                                           0],
                            'V033 - VIGIAGRO GUAÍRA - PR': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE GUAIRA-PR',
                                0],
                            'SF04 - SFA - AMAPÁ': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO AMAPÁ', 0],
                            'V022 - VIGIAGRO MUNDO NOVO - MS': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE MUNDO NOVO-MS', 0],
                            'SF23 - SFA - RORAIMA': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE RORAIMA', 0],
                            '': ['', 0],
                            'V007 - VIGIAGRO SANTANA - AP': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SANTANA-AP', 0],
                            'V044 - VIGIAGRO PACARAIMA - RR': [
                                'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PACARAIMA-RR', 0],
                            'U014 - UTRA PATOS DE MINAS - MG': ['UNIDADE TECNICA REGIONAL DE PATOS DE MINAS - MG', 0],
                            'V66 - VIGIAGRO BAURU - SP': ['VIGIAGRO BAURU - SP', 0]}

                        unidade_vigiagro = input("Qual Unidade Vigiagro deseja pesquisar a quantidade de CF emitidos e "
                                                 "válidos?\n").upper()

                        def buscaExportacaoCFPorUnidade():

                            tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_4}'))

                            for linha in tabela:
                                for key, value in unidades.items():
                                    if linha[4] in key and linha[2] == 'VALIDO':
                                        value[1] += 1

                            print('----------------------------------------------------')
                            print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                            print('----------------------------------------------------')
                            for key, value in unidades.items():
                                if unidade_vigiagro in key:
                                    tabelaFinal = [
                                        ['Unidade Vigiagro', 'Número total de CF'],
                                        [f'{value[0]}', value[1]]]
                                    print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

                        buscaExportacaoCFPorUnidade()

                        sleep(1)

                        pergunta5 = input(
                            "Deseja voltar ao menu da Exportação Vegetal?\nDigite 'S' para voltar:\n").lower()

                        if pergunta5 != 's':
                            menuVegetal = False

                    elif tipoPesquisa == 6:

                        qualFiscal = input("Qual AFFA deseja pesquisar na base de dados?\n").lower()
                        qualPais = input("Qual destino deseja pesquisar na base de dados?\n").lower()


                        def buscaExportacaoVegetalCombinada1(fiscal, pais):

                            tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_4}'))
                            n = 0
                            nomeCompleto = ""
                            nomePais = ""

                            for linha in tabela:
                                dados1 = linha[3]
                                dados2 = linha[10]
                                if fiscal in dados1.lower() and pais in dados2.lower() and linha[2] == 'VALIDO':
                                    n += 1
                                    nomeCompleto = f"{dados1}"
                                    nomePais = f"{dados2}"

                            print('----------------------------------------------------')
                            print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                            print('----------------------------------------------------')
                            tabelaFinal = [['Tipo de Operação', 'Nome do AFFA', 'País de destino',
                                            'Número de CF'],
                                           ['Exportação Vegetal', nomeCompleto, nomePais, n]]
                            print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

                            if n == 0:
                                print(
                                    "Não foram encontrados CF emitidos pelo AFFA {}, contendo coletivamente o país de destino {}.".format(qualFiscal.upper(),
                                        qualPais.upper()))

                        buscaExportacaoVegetalCombinada1(qualFiscal, qualPais)

                        sleep(1)

                        pergunta5 = input("Deseja voltar ao menu da Exportação Vegetal?\nDigite 'S' para voltar:\n").lower()

                        if pergunta5 != 's':
                            menuVegetal = False

                    elif tipoPesquisa == 7:

                        qualProduto = input("Qual produto deseja pesquisar na base de dados?\n").lower()
                        qualPais = input("Qual destino deseja pesquisar na base de dados?\n").lower()

                        dataInicio = input("Qual a data do início do período de pesquisa? Usar formato dd/mm/aa\n")
                        dataFim = input("Qual a data do final do período de pesquisa? Usar formato dd/mm/aa\n")

                        retornaLPCO = input("Deseja que retorne os LPCOs referentes às buscas?\nDigite 'S' para SIM\n").lower()


                        def buscaExportacaoVegetalCombinada2(produto, pais, dataInicio, dataFim):

                            minhaDataInicio = datetime.strptime(dataInicio, "%d/%m/%y")
                            minhaDataFim = datetime.strptime(dataFim, "%d/%m/%y")

                            tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_1}'))
                            n = 0
                            nomeProduto = ""
                            nomePais = ""
                            listaLPCO = []

                            for linha in tabela:
                                dados1 = linha[22]
                                dados2 = linha[11]

                                if linha[5] != "Data de Recebimento":
                                    dataRecebimento = linha[5][0:8]
                                    minhaDataRecebimento = datetime.strptime(dataRecebimento, "%d/%m/%y")
                                    if minhaDataInicio <= minhaDataRecebimento <= minhaDataFim:
                                        if produto in dados1.lower() and pais in dados2.lower() and linha[17] == "DEFERIDO":
                                            n += 1
                                            nomeProduto = produto.upper()
                                            nomePais = f"{dados2}"
                                            if retornaLPCO == 's':
                                                listaLPCO.append(linha[2])

                            print('----------------------------------------------------')
                            print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                            print('----------------------------------------------------')
                            tabelaFinal = [['Tipo de Operação', 'Data inicial de busca', 'Data final de busca', 'Nome do produto', 'País de destino',
                                            'Número de LPCOs'],
                                           ['Exportação Vegetal', minhaDataInicio, minhaDataFim, nomeProduto, nomePais, n]]
                            print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

                            df = pd.DataFrame({'Número do LPCO': listaLPCO})
                            print(df.to_numpy())

                            if n == 0:
                                print(
                                    "Não foram encontradas LPCOs registradas para o produto {}, coletivamente para o país de destino {},\nno período entre {} e {}.".format(qualProduto.upper(),
                                        qualPais.upper(), minhaDataInicio, minhaDataFim))

                        buscaExportacaoVegetalCombinada2(qualProduto, qualPais, dataInicio, dataFim)

                        sleep(1)

                        pergunta5 = input("Deseja voltar ao menu da Exportação Vegetal?\nDigite 'S' para voltar:\n").lower()

                        if pergunta5 != 's':
                            menuVegetal = False

                    elif tipoPesquisa == 8:

                        qualUsoProposto = input("Qual uso proposto deseja pesquisar na base de dados?\n").lower()
                        qualPais = input("Qual destino deseja pesquisar na base de dados?\n").lower()

                        dataInicio = input("Qual a data do início do período de pesquisa? Usar formato dd/mm/aa\n")
                        dataFim = input("Qual a data do final do período de pesquisa? Usar formato dd/mm/aa\n")

                        retornaLPCO = input("Deseja que retorne os LPCOs referentes às buscas?\nDigite 'S' para SIM\n").lower()


                        def buscaExportacaoVegetalCombinada2(usoProposto, pais, dataInicio, dataFim):

                            minhaDataInicio = datetime.strptime(dataInicio, "%d/%m/%y")
                            minhaDataFim = datetime.strptime(dataFim, "%d/%m/%y")

                            tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_1}'))
                            n = 0
                            nomeUsoProposto = ""
                            nomePais = ""
                            listaLPCO = []

                            for linha in tabela:
                                dados1 = linha[14]
                                dados2 = linha[11]

                                if linha[5] != "Data de Recebimento":
                                    dataRecebimento = linha[5][0:8]
                                    minhaDataRecebimento = datetime.strptime(dataRecebimento, "%d/%m/%y")
                                    if minhaDataInicio <= minhaDataRecebimento <= minhaDataFim:
                                        if usoProposto in dados1.lower() and pais in dados2.lower() and linha[17] == "DEFERIDO":
                                            n += 1
                                            nomeUsoProposto = f"{dados1}"
                                            nomePais = f"{dados2}"
                                            if retornaLPCO == 's':
                                                listaLPCO.append(linha[2])

                            print('----------------------------------------------------')
                            print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                            print('----------------------------------------------------')
                            tabelaFinal = [['Tipo de Operação', 'Data inicial de busca', 'Data final de busca', 'Uso Proposto', 'País de destino',
                                            'Número de LPCOs'],
                                           ['Exportação Vegetal', minhaDataInicio, minhaDataFim, nomeUsoProposto, nomePais, n]]
                            print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

                            df = pd.DataFrame({'Número do LPCO': listaLPCO})
                            print(df.to_numpy())

                            if n == 0:
                                print(
                                    "Não foram encontradas LPCOs registradas para o uso proposto que contenha {}, coletivamente para o país de destino {},\nno período entre {} e {}.".format(qualUsoProposto.upper(),
                                        qualPais.upper(), minhaDataInicio, minhaDataFim))

                        buscaExportacaoVegetalCombinada2(qualUsoProposto, qualPais, dataInicio, dataFim)

                        sleep(1)

                        pergunta5 = input("Deseja voltar ao menu da Exportação Vegetal?\nDigite 'S' para voltar:\n").lower()

                        if pergunta5 != 's':
                            menuVegetal = False

                    elif tipoPesquisa == 9:
                        menuAnimalVegetal = False
                        menuVegetal = False

            elif area == 3:

                pergunta7 = input("Deseja voltar ao menu geral?\nDigite 'S' para voltar:\n").lower()

                if pergunta7 != 's':
                    menuGeral = False
                    menuAnimalVegetal = False
                    menuVegetal = False
                    menuAnimal = False

                elif pergunta7 == 's':
                    menuAnimalVegetal = False
                    menuVegetal = False
                    menuAnimal = False

        elif operacao == 2:

            uso_proposto = int(input('''Deseja pesquisar por área agropecuária, NCM ou Unidades Vigiagro?
Digite [1] para animal ou [2] para vegetal.
Digite [3] para pesquisar por NCM.
Digite [4] para pesquisar por Unidades Vigiagro.
Digite [5] para pesquisar pelo CNPJ do importador.
Digite [6] para pesquisar por período de busca.\n'''))
            if uso_proposto == 1:
                qualArea = "Animal"
                for i in usoPropostoAnimal:
                    print(f"{usoPropostoAnimal.index(i) + 1} - {i}")
                print("Qual dos usos propostos deseja pesquisar?")
                uso = usoPropostoAnimal[int(input()) - 1]
                print(uso)

            elif uso_proposto == 2:
                qualArea = "Vegetal"
                for i in usoPropostoVegetal:
                    print(f"{usoPropostoVegetal.index(i) + 1} - {i}")
                print("Qual dos usos propostos deseja pesquisar?")
                uso = usoPropostoVegetal[int(input()) - 1]
                print(uso)

            elif uso_proposto == 3:
                ncm = input("Qual NCM deseja pesquisar?\nDigite sem espaços ou pontos.\n")

                tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_2}'))

                w = 0
                for linha in tabela:
                    ncm_code = linha[4].strip('="')
                    if ncm == ncm_code:
                        w += 1

                if w == 0:
                    w = 'zero'

                tabelaFinal = [
                    ['Tipo de Operação', 'NCM', 'Número total de LPCOs com o NCM'],
                    ['Importação', f'{ncm}', w]]

                print('----------------------------------------------------')
                print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                print('----------------------------------------------------')
                print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

            elif uso_proposto == 4:
                # Para extrair o nome das Unidades do .csv das Unidades Vigiagro
                # tabela2 = csv.reader(open('/Users/pauloroberto/Desktop/unidades_vigiagro_atual.csv'))
                #
                # novasUnidades = {}
                # for linha in tabela2:
                #     novaUnidade = linha[0].split(';')[3]
                #     if novaUnidade != 'NM_ORGAO_EXTENSO':
                #         print(novaUnidade)
                #         novasUnidades[novaUnidade] = 0
                # print(novasUnidades)

                unidades = {
                    'V034 - VIGIAGRO PARANAGUÁ - PR': [
                        'SERVIÇO DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PARANAGUÁ-PR', 0],
                    'V064 - VIGIAGRO SANTOS - SP': ['SERVIÇO DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SANTOS-SP', 0],
                    'V032 - VIGIAGRO FOZ DO IGUAÇU - PR': [
                        'SERVIÇO DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE FOZ DO IGUAÇU-PR',
                        0],
                    'V055 - VIGIAGRO URUGUAIANA - RS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE URUGUAIANA-RS', 0],
                    'V052 - VIGIAGRO RIO GRANDE - RS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE RIO GRANDE-RS', 0],
                    'V020 - VIGIAGRO CORUMBÁ - MS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE CORUMBÁ-MS', 0],
                    'V029 - VIGIAGRO SUAPE - PE': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SUAPE-PE',
                        0],
                    'V054 - VIGIAGRO SÃO BORJA - RS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SAO BORJA-RS', 0],
                    'V045 - VIGIAGRO ACEGUÁ-BAGÉ - RS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ACEGUÁ-BAGE-RS', 0],
                    'V061 - VIGIAGRO SÃO FRANCISCO DO SUL - SC': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SAO FRANCISCO DO SUL-SC',
                        0],
                    'V026 - VIGIAGRO VILA DO CONDE - PA': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE VILA DO CONDE-PA', 0],
                    'V058 - VIGIAGRO ITAJAÍ - SC': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ITAJAI-SC',
                        0],
                    'V017 - VIGIAGRO ITAQUÍ-MADEIRA - MA': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ITAQUI-MADEIRA-MA', 0],
                    'V049 - VIGIAGRO PORTO ALEGRE - RS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PORTO ALEGRE-RS', 0],
                    'V010 - VIGIAGRO SALVADOR - BA': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SALVADOR-BA', 0],
                    'V024 - VIGIAGRO BELÉM - PA': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE BELÉM-PA',
                        0],
                    'V060 - VIGIAGRO ITAPOÁ - SC': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ITAPOA-SC',
                        0],
                    'V063 - VIGIAGRO GUARULHOS - SP': [
                        'SERVIÇO DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE GUARULHOS-SP', 0],
                    'V028 - VIGIAGRO RECIFE - PE': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE RECIFE-PE',
                        0],
                    'U040 - UTRA CAMPINAS - SP': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA EM CAMPINAS - SP', 0],
                    'V015 - VIGIAGRO VITÓRIA - ES': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE VITORIA-ES', 0],
                    'U046 - UTRA REGIÃO METROPOLITANA - SP': [
                        'UNIDADE TECNICA REGIONAL DE AGRICULTURA DA REGIAO METROPOLITANA - SP', 0],
                    'V053 - VIGIAGRO SANTANA DO LIVRAMENTO - RS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SANTANA DO LIVRAMENTO-RS',
                        0],
                    'U034 - UTRA CAXIAS DO SUL - RS': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA DE CAXIAS DO SUL - RS',
                                                       0],
                    'V046 - VIGIAGRO CHUÍ - RS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE CHUI-RS', 0],
                    'V051 - VIGIAGRO QUARAÍ - RS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE QUARAÍ-RS',
                        0],
                    'V039 - VIGIAGRO NATAL - RN': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE NATAL-RN',
                        0],
                    'V048 - VIGIAGRO JAGUARÃO - RS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE JAGUARAO-RS', 0],
                    'SF21 - SFA - RIO GRANDE DO SUL': [
                        'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO RIO GRANDE DO SUL', 0],
                    'V059 - VIGIAGRO IMBITUBA - SC': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE IMBITUBA-SC', 0],
                    'V056 - VIGIAGRO DIONÍSIO CERQUEIRA - SC': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE DIONÍSIO CERQUEIRA-SC', 0],
                    'V047 - VIGIAGRO ITAQUÍ - RS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ITAQUI-RS',
                        0],
                    'V013 - VIGIAGRO PECÉM - CE': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DO PECEM-CE',
                        0],
                    'V050 - VIGIAGRO PORTO XAVIER - RS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PORTO XAVIER-RS', 0],
                    'V025 - VIGIAGRO SANTARÉM - PA': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SANTAREM-PA', 0],
                    'V003 - VIGIAGRO MACEIÓ - AL': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE MACEIO-AL',
                        0],
                    'V030 - VIGIAGRO VALE DO SÃO FRANCISCO - PE': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DO VALE DO SÃO FRANCISCO-PE',
                        0],
                    'V036 - VIGIAGRO ITAGUAÍ - RJ': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ITAGUAÍ-RJ', 0],
                    'V038 - VIGIAGRO PORTO DO RIO DE JANEIRO - RJ': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL PORTO DO RIO DE JANEIRO-RJ',
                        0],
                    'U041 - UTRA FAZENDA IPANEMA - SP': [
                        'UNIDADE TECNICA REGIONAL DE AGRICULTURA NA FAZENDA IPANEMA - SP', 0],
                    'V065 - VIGIAGRO VIRACOPOS - SP': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE VIRACOPOS-SP', 0],
                    'V005 - VIGIAGRO MANAUS - AM': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE MANAUS-AM',
                        0],
                    'V018 - VIGIAGRO CONFINS - MG': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE CONFINS-MG', 0],
                    'U018 - UTRA UBERLÂNDIA - MG': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA DE UBERLANDIA - MG', 0],
                    'V002 - VIGIAGRO EPITACIOLÂNDIA - AC': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE EPITACIOLANDIA-AC', 0],
                    'U023 - UTRA SANTARÉM - PA': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA DE SANTAREM - PA', 0],
                    'V031 - VIGIAGRO CURITIBA - PR': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE CURITIBA-PR', 0],
                    'U017 - UTRA UBERABA - MG': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA DE UBERABA - MG', 0],
                    'U019 - UTRA VARGINHA - MG': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA DE VARGINHA - MG', 0],
                    'V062 - VIGIAGRO ARACAJÚ - SE': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ARACAJU-SE', 0],
                    'SF25 - SFA - SÃO PAULO': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE SÃO PAULO', 0],
                    'V021 - VIGIAGRO PONTA PORÃ - MS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PONTA PORÃ-MS', 0],
                    'V012 - VIGIAGRO FORTALEZA - CE': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE FORTALEZA-CE', 0],
                    'V037 - VIGIAGRO GALEÃO - RJ': ['SERVIÇO DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DO GALEÃO-RJ', 0],
                    'SFA - PARANÁ': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO PARANÁ', 0],
                    'SF16 - SFA - PARANÁ': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO PARANÁ', 0],
                    'U042 - UTRA GUARATINGUETÁ - SP': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA EM GUARATINGUETA - SP',
                                                       0],
                    'VIGIAGRO URUGUAIANA - RS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE URUGUAIANA-RS', 0],
                    'V040 - VIGIAGRO GUAJARÁ-MIRIM - RO': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE GUAJARA MIRIM-RO', 0],
                    'VIGIAGRO ACEGUÁ-BAGÉ - RS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ACEGUÁ-BAGE-RS', 0],
                    'VIGIAGRO PARANAGUÁ - PR': ['SERVIÇO DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PARANAGUÁ-PR', 0],
                    'V023 - VIGIAGRO CUIABÁ - MT': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE CUIABÁ-MT',
                        0],
                    'V004 - VIGIAGRO AEROPORTO DE MANAUS - AM': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL AEROPORTO DE MANAUS-AM', 0],
                    'SF08 - SFA - ESPÍRITO SANTO': [
                        'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO NO ESPÍRITO SANTO', 0],
                    'SF10 - SFA - MARANHÃO': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO MARANHÃO', 0],
                    'SF19 - SFA - RIO DE JANEIRO': [
                        'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO RIO DE JANEIRO', 0],
                    'V011 - VIGIAGRO AEROPORTO DE FORTALEZA - CE': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE AEROPORTO DE FORTALEZA-CE',
                        0],
                    'U039 - UTRA BOTUCATU - SP': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA DE BOTUCATU - SP', 0],
                    'V057 - VIGIAGRO FLORIANÓPOLIS - SC': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE FLORIANOPOLIS-SC', 0],
                    'SF14 - SFA - PARÁ': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO PARÁ', 0],
                    'V027 - VIGIAGRO CABEDELO - PB': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE CABEDELO-PB', 0],
                    'SF24 - SFA - SANTA CATARINA': [
                        'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE SANTA CATARINA', 0],
                    'SF26 - SFA - SERGIPE': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE SERGIPE', 0],
                    'V043 - VIGIAGRO BONFIM - RR': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE BONFIM-RR',
                        0],
                    'SF13 - SFA - MINAS GERAIS': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE MINAS GERAIS',
                                                  0],
                    'SF17 - SFA - PERNAMBUCO': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE PERNAMBUCO', 0],
                    'SF11 - SFA - MATO GROSSO': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE MATO GROSSO', 0],
                    'SF06 - SFA - CEARÁ': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO CEARÁ', 0],
                    'SF12 - SFA - MATO GROSSO DO SUL': [
                        'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE MATO GROSSO DO SUL',
                        0],
                    'U010 - UTRA DIVINÓPOLIS - MG': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA EM DIVINOPOLIS - MG', 0],
                    'U005 - UTRA VITÓRIA DA CONQUISTA - BA': [
                        'UNIDADE TECNICA REGIONAL DE AGRICULTURA DE VITORIA DA CONQUISTA - BA', 0],
                    'SF03 - SFA - AMAZONAS': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO AMAZONAS', 0],
                    'SF20 - SFA - RIO GRANDE DO NORTE': [
                        'SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO RIO GRANDE DO NORTE',
                        0],
                    'U011 - UTRA JUIZ DE FORA - MG': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA JUIZ DE FORA - MG', 0],
                    'SF05 - SFA - BAHIA': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DA BAHIA', 0],
                    'SF15 - SFA - PARAÍBA': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DA PARAÍBA', 0],
                    'SF01 - SFA - ACRE': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO ACRE', 0],
                    'V016 - VIGIAGRO ANÁPOLIS - GO': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ANÁPOLIS-GO', 0],
                    'SF09 - SFA - GOIÁS': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE GOIÁS', 0],
                    'U024 - UTRA CAMPINA GRANDE - PB': [
                        'UNIDADE TECNICA REGIONAL DE AGRICULTURA DE CAMPINA GRANDE - PB', 0],
                    'V041 - VIGIAGRO PORTO VELHO - RO': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PORTO VELHO-RO', 0],
                    'V014 - VIGIAGRO BRASÍLIA - DF': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE BRASILIA-DF', 0],
                    'U013 - UTRA MONTES CLAROS - MG': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA EM MONTES CLAROS - MG',
                                                       0],
                    'SF02 - SFA - ALAGOAS': ['SUPERINTENDÊCIA FEDERAL DE AGRICULTURA NO ESTADO DE ALAGOAS', 0],
                    'V001 - VIGIAGRO ASSIS BRASIL - AC': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE ASSIS BRASIL-AC', 0],
                    'SF07 - SFA - DISTRITO FEDERAL': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO DISTRITO FEDERAL', 0],
                    'V035 - VIGIAGRO SANTA HELENA - PR': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SANTA HELENA-PR', 0],
                    'U037 - UTRA ARAÇATUBA - SP': ['UNIDADE TECNICA REGIONAL DE AGRICULTURA EM ARACATUBA - SP', 0],
                    'V033 - VIGIAGRO GUAÍRA - PR': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE GUAIRA-PR',
                        0],
                    'SF04 - SFA - AMAPÁ': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DO AMAPÁ', 0],
                    'V022 - VIGIAGRO MUNDO NOVO - MS': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE MUNDO NOVO-MS', 0],
                    'SF23 - SFA - RORAIMA': ['SUPERINTENDÊNCIA FEDERAL DE AGRICULTURA NO ESTADO DE RORAIMA', 0],
                    '': ['', 0],
                    'V007 - VIGIAGRO SANTANA - AP': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE SANTANA-AP', 0],
                    'V044 - VIGIAGRO PACARAIMA - RR': [
                        'UNIDADE DESCENTRALIZADA DE VIGILÂNCIA AGROPECUÁRIA INTERNACIONAL DE PACARAIMA-RR', 0],
                    'U014 - UTRA PATOS DE MINAS - MG': ['UNIDADE TECNICA REGIONAL DE PATOS DE MINAS - MG', 0],
                    'V66 - VIGIAGRO BAURU - SP': ['VIGIAGRO BAURU - SP', 0]}

                tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_2}'))

                unidade_vigiagro = input("Qual unidade deseja pesquisar a quantidade de LPCOs?\n").upper()

                for linha in tabela:
                    for key, value in unidades.items():
                        if key == linha[18]:
                            value[1] += 1

                print('----------------------------------------------------')
                print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                print('----------------------------------------------------')
                for key, value in unidades.items():
                    if unidade_vigiagro in key:
                        tabelaFinal = [
                            ['Unidade Vigiagro', 'Número total de LPCOs'],
                            [f'{value[0]}', value[1]]]
                        print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

            if uso_proposto == 1 or uso_proposto == 2:

                produto = input("Qual produto deseja pesquisar na base de dados?\n").lower()

                if uso_proposto == 1:
                    hashAnimal = {}

                    i = 0
                    for i in usoPropostoAnimal:
                        hashAnimal[i] = 0

                    l = 0
                    somaAnimal = 0
                    for u in usoPropostoAnimal:
                        res = list(hashAnimal.keys())[l]
                        tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_2}'))
                        n = 0
                        for linha in tabela:
                            usoProposto = linha[11]
                            if res in usoProposto.lower():
                                n += 1
                        hashAnimal[res] = n
                        l += 1

                        somaAnimal += n

                elif uso_proposto == 2:

                    hashVegetal = {}

                    i = 0
                    for i in usoPropostoVegetal:
                        hashVegetal[i] = 0

                    l = 0
                    somaVegetal = 0
                    for u in usoPropostoVegetal:
                        res = list(hashVegetal.keys())[l]
                        tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_2}'))
                        n = 0
                        for linha in tabela:
                            usoProposto = linha[11]
                            if res in usoProposto.lower():
                                n += 1
                        hashVegetal[res] = n
                        l += 1

                        somaVegetal += n

                def buscaImportacaoVegetal(produto):

                    tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_2}'))
                    p = 0
                    u = 0

                    for linha in tabela:
                        mercadoria = linha[6]
                        usoProposto = linha[11]
                        if produto in mercadoria.lower():
                            p += 1
                        if uso in usoProposto.lower():
                            u += 1

                    c = 0
                    if uso_proposto == 1:
                        c = somaAnimal

                    elif uso_proposto == 2:
                        c = somaVegetal

                    tabelaFinal = [
                        ['Tipo de Operação', 'Número total de LPCOs', f'Número de LPCOs do\nUso Proposto {uso.upper()}',
                         f'Número de LPCOs contendo o\n produto {produto.upper()} na descrição'],
                        [f'Importação {qualArea}', c, u, p]]

                    print('----------------------------------------------------')
                    print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                    print('----------------------------------------------------')
                    print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

                buscaImportacaoVegetal(produto)

            elif uso_proposto == 5:

                cnpj = input("Qual CNPJ do importador deseja pesquisar?\n"
                             "Informe um número válido com 8 dígitos (raiz) ou 14 dígitos (completo)\n"
                             "sem pontos, barra e hífen.\n")

                tabela = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_2}'))

                if len(cnpj) == 8:
                    nc = 0
                    cnpj_root = ''
                    razao_social = ''
                    for linha in tabela:
                        cnpj_code = linha[7]
                        cnpj_code_root = cnpj_code[0:8]
                        cnpj_root = cnpj

                        if cnpj_root == cnpj_code_root:
                            nc += 1
                            razao_social = linha[9]

                            if nc == 0:
                                nc = 'zero'

                    cnpj_final = f'{cnpj[0:2]}' + '.' + f'{cnpj[2:5]}' + '.' + f'{cnpj[5:8]}' + '/XXX-XX'

                    tabelaFinal = [
                        ['Tipo de Operação', 'Razão Social do Importador', 'CNPJ',
                         'Número total de LPCOs com o CNPJ'],
                        ['Importação', f'{razao_social}', f'{cnpj_final}', nc]]

                    print('----------------------------------------------------')
                    print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                    print('----------------------------------------------------')
                    print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

                elif len(cnpj) == 14:
                    nc = 0
                    razao_social = ''
                    for linha in tabela:
                        cnpj_code = linha[7]
                        cnpj_root = cnpj

                        if cnpj_code == cnpj:
                            nc += 1
                            razao_social = linha[9]

                            if nc == 0:
                                nc = 'zero'

                    cnpj_final = f'{cnpj[0:2]}' + '.' + f'{cnpj[2:5]}' + '.' + f'{cnpj[5:8]}' + '/' + f'{cnpj[8:12]}' + '-' + f'{cnpj[12:14]}'

                    tabelaFinal = [
                        ['Tipo de Operação', 'Razão Social do Importador', 'CNPJ',
                         'Número total de LPCOs com o CNPJ'],
                        ['Importação', f'{razao_social}', f'{cnpj_final}', nc]]

                    print('----------------------------------------------------')
                    print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                    print('----------------------------------------------------')
                    print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

                else:
                    while len(cnpj) != 8 and len(cnpj) != 14:
                        print(
                            'Foi informado um número de CNPJ diferente do formato com 8 dígitos (raiz) ou 14 dígitos.')
                        cnpj = input("Qual CNPJ do importador deseja pesquisar?\n"
                                     "Informe um número válido com 8 dígitos (raiz) ou 14 dígitos (completo).\n")

            elif uso_proposto == 6:

                # Utilizar data no formato dd/mm/aa
                dataInicio = input("Qual a data do início do período de pesquisa? Usar formato dd/mm/aa\n")
                dataFim = input("Qual a data do final do período de pesquisa? Usar formato dd/mm/aa\n")

                produto = input("Qual produto deseja pesquisar na base de dados?\n").lower()

                perguntaPais = input("Deseja pesquisa combinada por país? Tecle 'S' para 'Sim'\n").lower()

                if perguntaPais == 's':
                    pais = input("Qual país deseja pesquisar?\n")

                else:
                    pais = 'NÃO'


                def buscaImportacao(dataInicio, dataFim, produto, pais):

                    minhaDataInicio = datetime.strptime(dataInicio, "%d/%m/%y")
                    minhaDataFim = datetime.strptime(dataFim, "%d/%m/%y")

                    tabela1 = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_2}'))
                    c = 0
                    ni = 0
                    nip = 0
                    deferido = 0
                    indeferido = 0

                    for linha in tabela1:
                        mercadoria = linha[6]
                        paisOrigem = linha[5]
                        status = linha[19]
                        if linha[24] != "Data de Recebimento":
                            dataRecebimento = linha[24][0:8]
                            minhaDataRecebimento = datetime.strptime(dataRecebimento, "%d/%m/%y")
                            if minhaDataInicio <= minhaDataRecebimento <= minhaDataFim:
                                c += 1
                            if perguntaPais == 's':
                                if minhaDataInicio <= minhaDataRecebimento <= minhaDataFim and produto in mercadoria.lower() and pais in paisOrigem.lower():
                                    nip += 1
                                    if status == 'DEFERIDO':
                                        deferido += 1
                                    elif status == 'INDEFERIDO':
                                        indeferido += 1
                            else:
                                if minhaDataInicio <= minhaDataRecebimento <= minhaDataFim and produto in mercadoria.lower():
                                    ni += 1
                                    if status == 'DEFERIDO':
                                        deferido += 1
                                    elif status == 'INDEFERIDO':
                                        indeferido += 1

                    if perguntaPais == 's':
                        print('----------------------------------------------------')
                        print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                        print('----------------------------------------------------')
                        print(f'Data inicial de busca: {dataInicio}')
                        print(f'Data final de busca: {dataFim}')
                        tabelaFinal = [
                            ['Tipo de Operação', 'Expressão de busca', 'País de destino', 'Número total de LPCOs',
                             f'Número total de LPCOs \ncom a expressão \n {produto.upper()} \nna descrição do produto e para o país pesquisado',
                             'LPCOs deferidas', 'LPCOs indeferidas'],
                            ['Importação', produto.upper(), pais.upper(), c, nip, deferido, indeferido]]
                        print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

                    else:

                        print('----------------------------------------------------')
                        print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                        print('----------------------------------------------------')
                        print(f'Data inicial de busca: {dataInicio}')
                        print(f'Data final de busca: {dataFim}')
                        tabelaFinal = [['Tipo de Operação', 'Expressão de busca', 'Número total de LPCOs',
                                        f'Número total de LPCOs \ncom a expressão \n {produto.upper()} \nna descrição do produto',
                                        'LPCOs deferidas', 'LPCOs indeferidas'],
                                       ['Importação', produto.upper(), c, ni, deferido, indeferido]]
                        print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))


                buscaImportacao(dataInicio, dataFim, produto, pais)

            pergunta7 = input("Deseja fazer nova pesquisa sobre áreas agropecuárias, usos propostos, NCM ou Unidade Vigiagro?\nDigite 'S' para pesquisar:\n").lower()

            if pergunta7 != 's':
                menuAnimalVegetal = False

        elif operacao == 3:

            # Utilizar data no formato dd/mm/aa
            dataInicio = input("Qual a data do início do período de pesquisa? Usar formato dd/mm/aa\n")
            dataFim = input("Qual a data do final do período de pesquisa? Usar formato dd/mm/aa\n")

            while len(dataInicio) != 8 or len(dataFim) != 8:
                print("---------------------------------------------------------------------------------")
                print("As datas de início e do final do período de pesquisa devem ter o formato dd/mm/aa")
                print("---------------------------------------------------------------------------------")
                dataInicio = input("Qual a data do início do período de pesquisa? Usar formato dd/mm/aa\n")
                dataFim = input("Qual a data do final do período de pesquisa? Usar formato dd/mm/aa\n")

            minhaDataInicio = datetime.strptime(dataInicio, "%d/%m/%y")
            minhaDataFim = datetime.strptime(dataFim, "%d/%m/%y")

            while minhaDataInicio > minhaDataFim:
                print("---------------------------------------------------------------------------------")
                print("A data de início do período de pesquisa deve ser anterior ao do final do período")
                print("---------------------------------------------------------------------------------")

                # Utilizar data no formato dd/mm/aa
                dataInicio = input("Qual a data do início do período de pesquisa? Usar formato dd/mm/aa\n")
                dataFim = input("Qual a data do final do período de pesquisa? Usar formato dd/mm/aa\n")

                minhaDataInicio = datetime.strptime(dataInicio, "%d/%m/%y")
                minhaDataFim = datetime.strptime(dataFim, "%d/%m/%y")


            def buscaRelatorioTotalPorPeriodo(dataInicio, dataFim):

                minhaDataInicio = datetime.strptime(dataInicio, "%d/%m/%y")
                minhaDataFim = datetime.strptime(dataFim, "%d/%m/%y")

                tabela1 = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_3}'))
                nea = 0

                for linha in tabela1:
                    if linha[5] != "Data de Recebimento":
                        dataRecebimento = linha[5][0:8]
                        minhaDataRecebimento = datetime.strptime(dataRecebimento, "%d/%m/%y")
                        if minhaDataInicio <= minhaDataRecebimento <= minhaDataFim:
                            nea += 1

                tabela2 = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_1}'))
                nev = 0

                for linha in tabela2:
                    if (linha[5]) != "Data de Recebimento":
                        dataRecebimento = linha[5][0:8]
                        minhaDataRecebimento = datetime.strptime(dataRecebimento, "%d/%m/%y")
                        if minhaDataInicio <= minhaDataRecebimento <= minhaDataFim:
                            nev += 1

                tabela3 = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_2}'))
                nia = 0

                for linha in tabela3:
                    if linha[24] != "Data de Recebimento":
                        dataRecebimento = linha[24][0:8]
                        minhaDataRecebimento = datetime.strptime(dataRecebimento, "%d/%m/%y")
                        for i in usoPropostoAnimal:
                            if minhaDataInicio <= minhaDataRecebimento <= minhaDataFim and i in linha[11].lower():
                                nia += 1

                tabela3 = csv.reader(open(f'/Users/pauloroberto/Desktop/{arquivo_2}'))
                niv = 0

                for linha in tabela3:
                    if linha[24] != "Data de Recebimento":
                        dataRecebimento = linha[24][0:8]
                        minhaDataRecebimento = datetime.strptime(dataRecebimento, "%d/%m/%y")
                        for i in usoPropostoVegetal:
                            if minhaDataInicio <= minhaDataRecebimento <= minhaDataFim and i in linha[11].lower():
                                niv += 1

                tabelaFinal = [['Tipo de Operação','Número de LPCOs'], ['Exportação Animal',  nea],
                           ['Exportação Vegetal', nev], ['Importação Animal', nia], ['Importação Vegetal', niv]]

                print('----------------------------------------------------')
                print('---RELATÓRIO DE REGISTRO DE LPCO NA BASE DE DADOS---')
                print('----------------------------------------------------')
                print(f'Período requisitado: {dataInicio} a {dataFim}')
                print(tabulate(tabelaFinal, headers='firstrow', tablefmt='fancy_grid'))

            buscaRelatorioTotalPorPeriodo(dataInicio, dataFim)

            sleep(1)

            pergunta6 = input("Deseja fazer nova pesquisa na base com outras datas?\nDigite 'S' para pesquisar:\n").lower()

            if pergunta6 != 's':
                menuAnimalVegetal = False

        elif operacao == 4:
            saudacaoFinal1 = "Desligando..."
            print(saudacaoFinal1)
            sleep(2)
            saudacaoFinal2 = "Desligado!"
            print(saudacaoFinal2)
            menuGeral = False
            menuAnimalVegetal = False
            menuVegetal = False
            menuAnimal = False
