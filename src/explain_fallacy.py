import re

# relation = {
#  fallacy:'fallacy_name',
#  message_content:'This is the message that was supposed to contain a logical fallacy'
# }


def start_handling(app, msg):
    handler = ExplainFallacy(app, msg)
    handler.handle_request()


class ExplainFallacy:
    fallacy_dict = {
        'false equivalence': {
            'title': "False Equivalence",
            'wikipedia': "[False Equivalence](https://en.wikipedia.org/wiki/False_equivalence)",
            'summary': ">False equivalence is a logical fallacy in which an equivalence is drawn between two subjects based on flawed or false reasoning. This fallacy is categorized as a fallacy of inconsistency. Colloquially, a false equivalence is often called 'comparing apples and oranges'."
        }
    }
    response = ""
    fallacy = ""
    info = None

    def __init__(self, app, msg):
        self.app = app
        self.reddit = app['reddit']
        self.msg = msg

    def handle_request(self):
        if self.msg.parent.__str__() == "Submission":
            print("Parent shouldn't be a submission. Must have parent Comment!")
            return

        parsed = re.findall('/u/explain-fallacy ?([a-z, ]+)', self.msg.body.lower())
        if len(parsed) == 0:
            print('Parsed length must be greater than 0')
            return

        fallacy = parsed[0]
        if fallacy not in self.fallacy_dict:
            print("Requested Fallacy not found in the Fallacy_Dict")
            return

        self.info = self.fallacy_dict[fallacy]
        if len(self.info) == 0:
            return

        self.build_response()
        if len(self.response) == 0:
            print("Valid response not found")
            return

        self.respond_to_message()

    def build_response(self):
        self.response += "Redditor /u/" + self.msg.author.name + " thinks you committed the [Logical Fallacy]("
        self.response += "https://en.wikipedia.org/wiki/Fallacy) of " + self.info['wikipedia']

    def respond_to_message(self):
        self.msg.parent().reply(self.response)
