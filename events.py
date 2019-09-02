import json
from event import Event

class Events:
    def __init__(self, filepath):
        self.filepath = filepath
        self.events = self.load_events()

    def load_events(self):
        try:
            with open(self.filepath,'r') as f:
                events = json.load(f)
                result = []
                for event in events:
                    #Need to update result to event details.
                    levent = Event(event['id'],event['event_name'],event['start_date'],event['end_date'],event['max'],event['description'],event['status'],event['players'])
                    result.append(levent)
                return result
        except(IOError,IndexError):
            print('Failed to load event data.')

    def save_events(self):
        with open(self.filepath,'w') as f:
            nevents = []
            for event in self.events:
                event_dict = event.__dict__
                nevents.append(event_dict)
            json.dump(nevents,f)

    def add_event(self,name,start_date,end_date,max=None,description=""):
        new_event = Event(len(self.events),name,start_date,end_date,max,description)
        self.events.append(new_event)
        self.save_events()
        return new_event.id

    def join_event(self,event_id,player):
        event = self.find_event(event_id)
        if len(event.players) < event.max:
            if player not in event.players:
                event.players.append(player)
                self.save_events()

    def leave_event(self,event_id,player):
        event = self.find_event(event_id)
        if player in event.players:
            event.players.remove(player)
            self.save_events()

    #Helper function to select event in list.
    def find_event(self,event_id):
        for event in self.events:
            if event.id == event_id:
                return event

    
  
    