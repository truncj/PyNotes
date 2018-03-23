class ReleaseIssue(object):

    def __init__(self, id, key, summary, description, assignee, link):
        self.id = id
        self.key = key
        self.summary = summary
        self.description = description
        self.assignee = assignee
        self.link = link
