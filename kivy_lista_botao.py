import dayzkillfeed as gve
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3

banco_ui = sqlite3.connect('killfeed.db')
banco_cursor_ui = banco_ui.cursor()

class KillfeedApp(Screen):
    lista_final = ListProperty([])
    list_args_converter = lambda i,j,dado: dict(height=30, size_hint_y=None, datahora=dado[0], morto=dado[1],assa=dado[2], arma=dado[3])

    def buscar_banco(self):
        nome_entrada = self.ids['entrada_nome']
        dados_killfeed = gve.KillfeedGVE(nome_player=nome_entrada.text)
        dados_killfeed.gravar()
        print(dados_killfeed.killfeed)

        select = banco_cursor_ui.execute('SELECT DATAHORA, MORTO, ASSA, ARMA FROM KILLFEED  WHERE MORTO = (?) OR ASSA = (?)', (nome_entrada.text, nome_entrada.text))
        lista_banco = select.fetchall()
        self.lista_final = lista_banco

sm = ScreenManager()
tela_prin = KillfeedApp(name = 'killfeed')
sm.add_widget(tela_prin)
print(sm.screens)

class Killfeed(App):
    def build(self):
        return sm

Killfeed().run()
