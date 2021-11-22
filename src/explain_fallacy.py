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
            'summary': "False equivalence is a logical fallacy in which an equivalence is drawn between two subjects based on flawed or false reasoning. This fallacy is categorized as a fallacy of inconsistency. Colloquially, a false equivalence is often called 'comparing apples and oranges'."
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
        'ad hominem': {
            'title': "Ad Hominem",
            'wikipedia': "[Ad Hominem](https://en.wikipedia.org/wiki/Ad_hominem)",
            'summary': "Ad hominem refers to a rhetorical strategy where the speaker attacks the character, motive, or some other attribute of the person making an argument rather than attacking the substance of the argument itself. The most common form of ad hominem is 'A makes a claim x, B asserts that A holds a property that is unwelcome, and hence B concludes that argument x is wrong'."
        },
        'ignoratio elenchi': {
            'title': "Ignoratio Elenchi",
            'wikipedia': "[Ignoratio Elenchi](https://en.wikipedia.org/wiki/Irrelevant_conclusion)",
            'summary': "An irrelevant conclusion, (ignoratio elenchi) is the informal fallacy of presenting an argument that may or may not be logically valid and sound, but (whose conclusion) fails to address the issue in question."
        },
        'thought terminating cliche': {
            'title': "Thought Terminating Cliche",
            'wikipedia': "[Thought Terminating Cliche](https://en.wikipedia.org/wiki/Thought-terminating_cliché)",
            'summary': "A thought-terminating cliché is a form of loaded language, commonly used to quell cognitive dissonance. Depending on context in which a phrase (or cliché) is used, it may actually be valid and not qualify as thought-terminating; it does qualify as such when its application intends to dismiss dissent or justify fallacious logic."
        },
        'appeal to tradition': {
            'title': "Appeal to Tradition",
            'wikipedia': "[Appeal to Tradition](https://en.wikipedia.org/wiki/Appeal_to_tradition)",
            'summary': "Appeal to tradition is an argument in which a thesis is deemed correct on the basis of correlation with past or present tradition. The appeal takes the form of 'this is right because we've always done it this way.'"
        },
        'just world': {
            'title': "Just World",
            'wikipedia': "[Just World](https://en.wikipedia.org/wiki/Just-world_hypothesis)",
            'summary': "The just-world fallacy is the cognitive bias that assumes that 'people get what they deserve' – that actions will have morally fair and fitting consequences for the actor. For example, the assumptions that noble actions will eventually be rewarded and evil actions will eventually be punished fall under this hypothesis. In other words, the just-world hypothesis is the tendency to attribute consequences to—or expect consequences as the result of— either a universal force that restores moral balance or a universal connection between the nature of actions and their results. This belief generally implies the existence of cosmic justice, destiny, divine providence, desert, stability, and/or order."
        },
        'google effect': {
            'title': "Google Effect",
            'wikipedia': "[Google Effect](https://en.wikipedia.org/wiki/Google_effect)",
            'summary': "The Google effect (digital amnesia) is the tendency to forget information that can be found readily online by using Internet search engines."
        },
        'composition': {
            'title': "Composition",
            'wikipedia': "[Composition](https://en.wikipedia.org/wiki/Fallacy_of_composition)",
            'summary': "The fallacy of composition arises when one infers that something is true of the whole from the fact that it is true of some part of the whole. A trivial example might be: 'This tire is made of rubber, therefore the vehicle of which it is a part is also made of rubber.'"
        },
        'chiller than thou': {
            'title': "Chiller than Thou",
            'wikipedia': "[Chiller than Thou](https://en.wikipedia.org/wiki/Self-righteousness)",
            'summary': "Self-righteousness is a feeling or display of (usually smug) moral superiority derived from a sense that one's beliefs, actions, or affiliations are of greater virtue than those of the average person. Self-righteous individuals are often intolerant of the opinions and behaviors of others. A self-righteous person might express disinterest in seeking an unselfish or objective standard of right and wrong, independently of how they interact with other people."
        },
        'holier than thou': {
            'title': "Holier Than Thou",
            'wikipedia': "[Holier Than Thou](https://en.wikipedia.org/wiki/Self-righteousness)",
            'summary': "Self-righteousness is a feeling or display of (usually smug) moral superiority derived from a sense that one's beliefs, actions, or affiliations are of greater virtue than those of the average person. Self-righteous individuals are often intolerant of the opinions and behaviors of others. A self-righteous person might express disinterest in seeking an unselfish or objective standard of right and wrong, independently of how they interact with other people."
        },
        'dunning kruger': {
            'title': "Dunning Kruger",
            'wikipedia': "[Dunning Kruger](https://en.wikipedia.org/wiki/Dunning–Kruger_effect)",
            'summary': "The Dunning–Kruger effect is a hypothetical cognitive bias stating that people with low ability at a task overestimate their own ability, and that people with high ability at a task underestimate their own ability."
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
        self.response += "**" + self.info['title'] + "** \n\n>"
        self.response += self.info['summary'] + "\n\n"
        self.response += "^(\[) [^(Fallacy List)](https://github.com/ZakVanstrom/Explain-Fallacy-Bot/blob/master/fallacy_list.md) ^(|) [^(GitHub)](https://github.com/ZakVanstrom/Explain-Fallacy-Bot) ^(| v0.0.0 | Want a Fallacy added?)  [^(Contact Me)](https://www.patreon.com/zak_vanstrom?fan_landing=true) ^(\])"

    def respond_to_message(self):
        self.msg.parent().reply(self.response)
