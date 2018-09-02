import dayzkillfeed as gve
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import sqlite3

banco_ui = sqlite3.connect('killfeed.db')
banco_cursor_ui = banco_ui.cursor()

class Janela_info(Screen):
    pass

class KillfeedApp(BoxLayout):
    lista_final = ListProperty([])
    list_args_converter = lambda i,j,dado: dict(height=30, size_hint_y=None, datahora=dado[0], morto=dado[1],assa=dado[2], arma=dado[3])

    def buscar_banco(self):
        nome_entrada = self.ids['entrada_nome']
        dados_killfeed = gve.KillfeedGVE(nome_player=nome_entrada.text)
        dados_killfeed.gravar()

        select = banco_cursor_ui.execute('SELECT DATAHORA, MORTO, ASSA, ARMA FROM KILLFEED  WHERE MORTO = (?) OR ASSA = (?)', (nome_entrada.text, nome_entrada.text))
        lista_banco = select.fetchall()
        self.lista_final = lista_banco

class Killfeed(App):
    screen_m = ScreenManager(transition=RiseInTransition())
    def abrir_janela(self):
        self.screen_m.add_widget(Janela_info(name='Detalhes'))

    def fechar_janela(self):
        self.screen_m.remove_widget(self.screen)

    def build(self):
        return KillfeedApp()

Killfeed().run()
