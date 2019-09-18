class RaidTeam:

    def __init__(self,team_id:int,team_name:str,team_max:int,players:list=None):
        self.team_id = team_id
        self.team_name = team_name
        self.team_max = team_max
        if players is None:
            self.players = []
        else:
            self.players = players


    def add_player(self,player):
        if player not in self.players and len(self.players) != self.team_max:
            self.players.append(player)
            return True
        else:
            return False

    def remove_player(self,player):
        if player in self.players:
            self.players.remove(player)
            return True
        else:
            return False