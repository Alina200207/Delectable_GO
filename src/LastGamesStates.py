import json


class LastGamesStates:
    def __init__(self):
        self.info_about_players_last_games = dict()
        try:
            with open("lastGames.json", "r") as file:
                try:
                    self.info_about_players_last_games = json.load(file)
                except json.decoder.JSONDecodeError:
                    print("There is no info about last games.")
        except IOError:
            with open("lastGames.json", "w") as file:
                pass

    @staticmethod
    def tuple_to_str(player: str, board_size: int, move: str) -> str:
        return player + " " + str(board_size) + " " + move

    def get_last_game_of_player(self, player: str, board_size: int) -> (list[list[int]], bool):
        if (self.tuple_to_str(player, board_size, "c")) in self.info_about_players_last_games:
            return self.info_about_players_last_games[self.tuple_to_str(player, board_size, "c")], False
        elif (self.tuple_to_str(player, board_size, "p")) in self.info_about_players_last_games:
            return self.info_about_players_last_games[self.tuple_to_str(player, board_size, "p")], True
        else:
            return None

    def set_last_game_of_player(self, player: str, board_size: int, move: str, board: list[list[int]]):
        self.info_about_players_last_games[self.tuple_to_str(player, board_size, move)] = board

    def delete_last_game_of_player(self, player: str, board_size: int):
        if (self.tuple_to_str(player, board_size, "c")) in self.info_about_players_last_games:
            del self.info_about_players_last_games[self.tuple_to_str(player, board_size, "c")]
        elif (self.tuple_to_str(player, board_size, "p")) in self.info_about_players_last_games:
            del self.info_about_players_last_games[self.tuple_to_str(player, board_size, "p")]

    def save_last_games(self):
        with open("lastGames.json", "w") as file:
            print(self.info_about_players_last_games)
            json.dump(self.info_about_players_last_games, file)
