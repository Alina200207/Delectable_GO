import sqlite3


class Database:
    """
    Allows working with database
    """
    def __init__(self):
        self.base = sqlite3.connect('info_about_players.db')
        self.cur = self.base.cursor()
        self.base.execute('CREATE TABLE IF NOT EXISTS players(player_name PRIMARY KEY, game_count, win_game_count, '
                     'general_points_count)')
        self.base.commit()

    def update_info_about_player(self, player_name, win, person_score):
        """
        Updates info about player in database.

        :param player_name: name of the player
        :param win: 1 if player won and 0 otherwise
        :param person_score: number of points earned by player in the current game
        """
        info = self.cur.execute('SELECT * FROM players WHERE player_name=?', (player_name,))
        if not info.fetchone():
            self.cur.execute('INSERT INTO players VALUES(?, ?, ?, ?)', (player_name, 1, win, person_score,))
        else:

            self.cur.execute('UPDATE players SET game_count=game_count + ?, win_game_count=win_game_count + ?, '
                        'general_points_count=general_points_count + ? WHERE player_name=?',
                        (1, win, person_score, player_name,))
        self.base.commit()

    def close_database(self):
        """
        Closes database.
        """
        self.base.close()
