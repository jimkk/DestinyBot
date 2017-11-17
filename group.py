from datetime import datetime

class group():
    name = ""
    type = 0
    created_by = 0
    time = None
    members = []
    size = 0

    def __init__(self, name, created_by_id, created_by_name, time, size):
        self.name = name
        self.created_by = created_by_id
        self.time = time
        self.size = size
        self.members.append((created_by_id, created_by_name))

    def add_member(self, member_id, member_name):
        self.members.append((member_id, member_name))

    def remove_member(self, member_id):
        for member in self.members:
            if member[0] == member_id:
                self.members.remove(member)

    def type_name(self):
        if self.type == 0:
            return 'Raid'
        elif self.type == 1:
            return 'Trials of the Nine'
        elif self. type == 2:
            return 'Nightfall'
        else:
            return 'Unknown Group Type'