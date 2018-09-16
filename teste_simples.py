import dayzkillfeed as gve

nome = input("Informe o nome do jogador:")
kill = gve.KillfeedGVE(nome_player = nome)

print('------------------------------')
print('JOGADOR: {0}'.format(kill.nomeplayer))
print('KILLS: {0}'.format(kill.qtdkills))
print('MORTES: {0}'.format(kill.qtdmorte))
print()

print('-------------------------------------------------------------------------------------')
print('     DATA E HORA     ||      MORTO       ||      ASSASSINO       ||      ARMA      ||')
print('-------------------------------------------------------------------------------------')
for linha in kill.banco_killfeed:
    print('  {0}  ||  {1}     ||  {2}         ||  {3}      ||'. format(linha[0], linha[1], linha[2], linha[3]))
    print('---------------------------------------------------------------------------------')
