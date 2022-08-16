class Task:
    def __init__(s, idx, deadline, description):
        s.idx = idx
        s.deadline = deadline
        s.description = description

    @staticmethod
    def fictive():
        return Task(-1, None, None)
