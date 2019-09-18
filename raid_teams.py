from raid_team import RaidTeam

class RaidTeams:
    filepath = None
    teams = [] #Is a list of RaidTeam objects
    def __init__(self,filepath:str):
        #load saved teams from file into team objects.
        self.load_teams(filepath)

    def save_teams(self,filepath):
        s_teams = self.teams.__dict__
        pass

    def load_teams(self,filepath):
        pass

    def create_team(self,team_name:str,team_max:int):
        new_team = RaidTeam(len(self.teams),team_name,team_max)
        if new_team.team_name not in self.teams:
            self.teams.append(new_team)
            return True
        else:
            return False