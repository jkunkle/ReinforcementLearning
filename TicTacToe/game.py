import argparse
import random
import player
import json



def main( ) : 

    run_game(1000)


def run_game( n_games ) : 

    x_player = player.player( 1 )
    o_player = player.player( 2 )

    piece_order = [1, 2]

    player_order = [x_player, o_player]

    results = []

    first_player = random.randint(0, 1) 
    second_player = first_player+1
    if second_player == 2 : 
        second_player = 0

    first_piece = piece_order[first_player]
    second_piece = piece_order[second_player]

    for igame in range( 0, n_games ) : 

        game_state = player.game_state()

        print ('Starting state')
        print (game_state.state )

        while True : 

            player_order[first_player].act( game_state )

            print ('State after player 1')
            print (game_state.state)

            if game_state.end() : 
                res_first = game_state.get_result(first_piece)
                res_second = game_state.get_result(second_piece)
                player_order[first_player].finish_game( res_first ) 
                player_order[second_player].finish_game( res_second) 
                state_list = game_state.state.tolist()
                if res_first : 
                    results.append((first_piece, state_list ))
                elif res_second : 
                    results.append((second_piece, state_list))
                else : 
                    results.append( (0, state_list) )

                break

            player_order[second_player].act( game_state )
            print ('State after player 2')
            print (game_state.state)

            if game_state.end() : 
                res_first = game_state.get_result(first_piece)
                res_second = game_state.get_result(second_piece)
                player_order[first_player].finish_game( res_first ) 
                player_order[second_player].finish_game( res_second) 
                state_list = game_state.state.tolist()
                if res_first : 
                    results.append(( first_piece, state_list))
                elif res_second : 
                    results.append((second_piece, state_list))
                else : 
                    results.append( (0 , state_list))
                break


            
    
    ofile = open( 'results.json', 'w' )
    json.dump( results, ofile )
    ofile.close()
    print (results)


if __name__ == '__main__' : 

    main(  )
