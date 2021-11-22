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
        # '': {
        #     'title': "",
        #     'wikipedia': "[]()",
        #     'summary': ""
        # },
        'false equivalence': {
            'title': "False Equivalence",
            'wikipedia': "[False Equivalence](https://en.wikipedia.org/wiki/False_equivalence)",
            'summary': ">False equivalence is a logical fallacy in which an equivalence is drawn between two subjects based on flawed or false reasoning. This fallacy is categorized as a fallacy of inconsistency. Colloquially, a false equivalence is often called 'comparing apples and oranges'."
        },
        'red herring': {
            'title': 'Red Herring',
            'wikipedia': '[Red Herring](https://en.wikipedia.org/wiki/Red_herring)',
            'summary': 'A red herring is something that misleads or distracts from a relevant or important question. It may be either a logical fallacy or a literary device that leads readers or audiences toward a false conclusion. A red herring may be used intentionally, as in mystery fiction or as part of rhetorical strategies (e.g., in politics), or may be used in argumentation inadvertently.'
        },
        'appeal to pity': {
            'title': 'Appeal to Pity',
            'wikipedia': '[Appeal to Pity](https://en.wikipedia.org/wiki/Appeal_to_pity)',
            'summary': "An appeal to pity is a fallacy in which someone tries to win support for an argument or idea by exploiting his opponent's feelings of pity or guilt. It is a specific kind of appeal to emotion. The name 'Galileo argument' refers to the scientist's suffering as a result of his house arrest by the Inquisition."
        },
        'appeal to authority': {
            'title': "Appeal to Authority",
            'wikipedia': "[Appeal to Authority](https://en.wikipedia.org/wiki/Argument_from_authority)",
            'summary': "An argument from authority is a form of argument in which the opinion of an authority on a topic is used as evidence to support an argument. Some consider that it is used in a cogent form if all sides of a discussion agree on the reliability of the authority in the given context, and others consider it to always be a fallacy to cite the views of an authority on the discussed topic as a means of supporting an argument."
        },
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
        self.response += "/u/" + self.msg.author.name + " thinks you committed the [Logical Fallacy]("
        self.response += "https://en.wikipedia.org/wiki/Fallacy) of " + self.info['wikipedia'] + "\n\n"
        self.response += "**" + self.info['title'] + "** \n\n"
        self.response += self.info['summary'] + "\n\n"
        self.response += "^(\[) [^(Fallacy List)](https://github.com/ZakVanstrom/Explain-Fallacy-Bot/blob/master/fallacy_list.md) ^(|) [^(GitHub)](https://github.com/ZakVanstrom/Explain-Fallacy-Bot) ^(| v0.0.0 | Want a Fallacy added?)  [^(Contact Me)](https://www.patreon.com/zak_vanstrom?fan_landing=true) ^(\])"

    def respond_to_message(self):
        self.msg.parent().reply(self.response)
