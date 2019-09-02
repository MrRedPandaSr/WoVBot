class Event:
    def __init__(self,id,name,start_date,end_date,max=None,description="",status=0,players=None):
        self.id = id
        self.event_name = name
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.max = max
        self.status = 0 #0=reigstered, 1=active, 2=completed 3=cancelled
        self.players = players
        if players == None:
            self.players = []
        
        
    def start_event(self):
        self.satus = 1

    def finish_event(self):
        self.status = 2

    def cancel_event(self):
        self.status = 3

    def get_players(self):
        return self.players

    def view_event(self):
        pass
