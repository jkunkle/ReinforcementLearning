import json

ofile = open( 'results.json', 'r' )

results = json.load( ofile )

n_win_1 = 0
n_win_2 = 0
n_draw = 0

for res in results : 
    if res[0] == 1 : 
        n_win_1 += 1
    if res[0] == 2 : 
        n_win_2 += 1
    if res[0] == 0 : 
        n_draw += 1


print ('Player 1 won %d times' %n_win_1)
print ('Player 2 won %d times' %n_win_1)
print ('There were %d draws' %n_draw)

ofile.close()
