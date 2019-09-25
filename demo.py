from selenium import webdriver
from kurveheadless.kurve import Kurve
import argparse


def run_demo(binary_location):
    options = webdriver.ChromeOptions()
    options.binary_location = binary_location
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
        winner_points = 0
        for player, points in kurve.get_player_scores().items():
            if points > winner_points:
                winner = player
                winner_points = points

        print('Game over, the winner is: ' + winner)

        kurve.close()
    except:
        kurve.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--binary_location', help='The location of your chrome headless binaries.', type=str, default='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')

    args = parser.parse_args()

    run_demo(args.binary_location)
