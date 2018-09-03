import requests
import sqlite3
from bs4 import BeautifulSoup
import time

#premissas para manipular o db e página
banco = sqlite3.connect('killfeed.db')
banco_cursor = banco.cursor()
banco_cursor.execute('CREATE TABLE IF NOT EXISTS killfeed(ID INTEGER PRIMARY KEY , DATAHORA DATETIME, MORTO TEXT, ASSA TEXT, ARMA TEXT)')

pagina_arq = open('D:\Guilherme\Projetos\Github projetos\dayzkillfeed\html teste.html').read()
pagina_str = requests.get("https://gvepvp.com/killfeed/live/")
#início funcões e classes principais do sistema---------------------------------------------------------------

#classe principal, possui como parametro o nome para busca e grava no banco de dados todos os eventos com o player indicado envolvido.
class KillfeedGVE(object):
    def __init__(self, nome_player =''):
        self.nomeplayer = nome_player
        if (self.nomeplayer == ''):
            print("Digite um nome para buscar")
        else:
            self.killfeed = self.__listar_kills__(pagina_str.content)

    def __listar_kills__(self, pagina):
        soup = BeautifulSoup(pagina, "html.parser")
        tag_script = list(soup.children)[23]
        console_infoaux = list(tag_script.children)[0]

        console_info = console_infoaux.splitlines()
        lista_final = []
        for linha_info in list(console_info):
            linha_info = linha_info.strip()
            if (self.__linha_util__(linha_info) == True):
                dados_kills = self.__atribuir_dados__(linha_info)
                if self.nomeplayer == dados_kills['morto'] or self.nomeplayer == dados_kills['assassino']:
                    lista_final.append(dados_kills)
            else:
                pass
        return lista_final

    def __linha_util__(self, linha):
        linha_aux = linha.split('\\u')
        if(linha.startswith('$') == True):
            try:
                if(linha_aux[1].startswith('002D') == True):
                    return True
            except:
                return False
        else:
            return False

    def __atribuir_dados__(self, linha_console):
        linha_console_list = linha_console.split("\\u")

        ano = str(time.localtime()[0])
        mes = fatiar_str(linha_console_list[0], 34, 36)
        dia = fatiar_str(linha_console_list[1], 4, 6)
        data =  dia + mes + ano
        hora = fatiar_str(linha_console_list[1], 6, 15)

        datahora = data + hora
        morto = fatiar_str(linha_console_list[6], 4)
        assassino = fatiar_str(linha_console_list[13], 4)

        arma = fatiar_str(linha_console_list[15], 6)
        arma = arma.split(")")[0]

        evento_dict = dict(datahora = datahora, morto = morto, assassino = assassino, arma = arma)
        return evento_dict

    def imprimir(self):
        for print_dict in self.killfeed:
            print("Data e Hora:", print_dict['datahora'], "Morto:", print_dict['morto'], "Assassino:", print_dict['assassino'], "Arma:", print_dict['arma'] + '\n')

    def gravar(self):
        for dict_evento in self.killfeed:
            if(self.__pode_gravar__(dict_evento) == True):
                banco_cursor.execute('INSERT INTO killfeed (DATAHORA, MORTO, ASSA,  ARMA) '
                             'VALUES (?,?,?,?)', (dict_evento['datahora'], dict_evento['morto'], dict_evento['assassino'], dict_evento['arma']))
        banco.commit()

#função pode_gravar foi criada para não criar dados repetidos no banco após várias requisições em pouco espaço de tempo, retorna booleano
    def __pode_gravar__(self, gravar_dict):
        banco_cursor.execute('SELECT DATAHORA, MORTO, ASSA FROM KILLFEED  WHERE MORTO = (?) OR ASSA = (?)ORDER BY ID DESC LIMIT 1', (self.nomeplayer, self.nomeplayer))
        ultimo_evento = banco_cursor.fetchone()
        if (ultimo_evento != None):
            data_banco = tuple(ultimo_evento)[0]
            data_aux = time.strptime(data_banco, '%d%m%Y %H:%M:%S' )
            data_evento = time.strptime(gravar_dict['datahora'], '%d%m%Y %H:%M:%S')
            if(data_evento <= data_aux):
                return False
            else:
                return True
        else:
            return True

def fatiar_str(string, liminf=0, limsup = None):
    string = string[liminf:limsup]
    return string

#fim funcões e classes principais do sistema---------------------------------------------------------------
