class Task:
    def __init__(s, idx, deadline, name, description):
        s.idx = idx
        s.deadline = deadline
        s.name = name
        s.description = description

    @staticmethod
    def fictive():
        return Task(-1, None, None, None)
