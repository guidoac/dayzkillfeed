import dayzkillfeed as gve
import sqlite3

banco_ui = sqlite3.connect('killfeed.db')
banco_cursor_ui = banco_ui.cursor()

nome = input("Informe o nome do jogador:")
kill = gve.KillfeedGVE(nome_player = nome)
kill.gravar()

select = banco_cursor_ui.execute('SELECT DATAHORA, MORTO, ASSA, ARMA FROM KILLFEED  WHERE MORTO = (?) OR ASSA = (?)', (nome, nome))
lista_banco = select.fetchall()
print(kill.killfeed)
