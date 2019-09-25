from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class Kurve:
    players = {
        'red': {
            'left': '1',
            'right': 'q',
        },
        'blue': {
            'left': 'b',
            'right': 'n',
        },
    }

    def __init__(self, driver_options, verbose=False):
        self.frame_id = 0
        self.round_count = 0
        self.verbose = verbose
        self.driver = webdriver.Chrome(chrome_options=driver_options)

    def load_page(self):
        self.print('page loaded')
        self.driver.get('https://achtungkurve.com')
        self.driver.execute_script("window.localStorage.setItem('kurve.privacy-policy-accepted','yes');")
        self.driver.get('https://achtungkurve.com/headless')

    def send_key(self, key):
        actions = ActionChains(self.driver)
        actions.send_keys(key)
        actions.perform()

    def add_player(self, player_id):
        if player_id in self.players:
            self.print('add player ' + str(player_id))
            self.send_key(self.get_player_key(player_id, 'left'))
        else:
            self.print('unknown player ' + str(player_id))

    def enter_game(self):
        self.print('enter game')
        self.send_key(Keys.SPACE)

    def start_round(self):
        self.print('start round')
        self.frame_id = 0
        self.round_count = self.round_count + 1
        self.send_key(Keys.SPACE)

    def next_frame(self):
        self.send_key(Keys.ENTER)
        self.frame_id = self.frame_id + 1

    def save_screenshot(self, path):
        self.driver.save_screenshot(path)

    def close(self):
        self.driver.quit()

    def get_frame_id(self):
        return self.frame_id

    def get_player_key(self, player_id, key):
        return self.players[player_id][key]

    def get_drawn_pixels(self):
        return self.driver.execute_script("return Kurve.Field.drawnPixels;")

    def is_running(self):
        return self.driver.execute_script("return Kurve.Game.isRunning;")

    def is_game_over(self):
        return self.driver.execute_script("return Kurve.Game.isGameOver;")

    def get_running_curves(self):
        return self.driver.execute_script("return Kurve.Game.runningCurves;")

    def get_players(self):
        return self.driver.execute_script("return Kurve.Game.players;")

    def get_player_scores(self):
        scores = {}

        for player in self.get_players():
            scores[str(player['id'])] = int(player['points'])

        return scores

    def print_player_scores(self):
        printed_scores = ''

        for player, points in self.get_player_scores().items():
            printed_scores += str(player) + '=' + str(points) + ', '

        return printed_scores.rstrip(', ')

    def print(self, text):
        if self.verbose:
            print(text)
