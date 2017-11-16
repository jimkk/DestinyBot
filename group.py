class group():
    name = ""
    created_by = 0
    members = []
    size = 0

    def __init__(self, name, created_by_id, created_by_name, size):
        self.name = name
        self.created_by = created_by_id
        self.size = size
        self.members.append((created_by_id, created_by_name))
    
    def add_member(self, member_id, member_name):
        self.members.append((member_id, member_name))

    def remove_member(self, member_id):
        for member in self.members:
            if member[0] == member_id:
                self.members.remove(member)