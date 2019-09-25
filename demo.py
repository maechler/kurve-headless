from selenium import webdriver
from kurveheadless.kurve import Kurve

options = webdriver.ChromeOptions()
options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
options.add_argument('window-size=1200x800')
options.add_argument('headless')

kurve = Kurve(options)

try:
    kurve.load_page()
    kurve.add_player('red')
    kurve.add_player('blue')
    kurve.enter_game()

    turn_left = False
    turn_right = False

    while not kurve.is_game_over():
        kurve.start_round()

        while kurve.is_running():
            if turn_left:
                kurve.send_key(kurve.get_player_key('red', 'left'))
            elif turn_right:
                kurve.send_key(kurve.get_player_key('red', 'right'))

            if kurve.get_frame_id() > 50:
                turn_left = True

            if kurve.get_frame_id() > 150:
                turn_left = False
                turn_right = True

            if kurve.get_frame_id() > 200:
                turn_right = False

            kurve.next_frame()

        print('round ' + str(kurve.round_count) + ': ' + kurve.print_player_scores())

        kurve.save_screenshot('out/screenshot_' + str(kurve.round_count) + '.png')

    winner = ''
    winnerPoints = 0
    for player, points in kurve.get_player_scores().items():
        if points > winnerPoints:
            winner = player
            winnerPoints = points

    print('Game over, the winner is: ' + winner)

    kurve.close()
except:
    kurve.close()