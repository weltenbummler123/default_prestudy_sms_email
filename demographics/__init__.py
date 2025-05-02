from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'demographics'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1



class Subsession(BaseSubsession):
    pass

# ''' ONLY WHEN TESTING ON ITS OWN'''
# def creating_session(subsession):
#     for player in subsession.get_players():
#         participant = player.participant
#         participant.progress = 1


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    ## Demographics
    age = models.IntegerField(
        verbose_name='Wie alt sind Sie?',
        min=18, max=100,
    )
    gender = models.StringField(
        choices=['Weiblich', 'Männlich', 'Divers', 'Keine Angabe'],
        verbose_name='Was ist Ihr Geschlecht?',
        widget=widgets.RadioSelect
    )
    live = models.StringField(
        choices=['Ja', 'Nein'],
        widget=widgets.RadioSelect
    )
    grow_up = models.StringField(
        choices=['Ja', 'Nein'],
        widget=widgets.RadioSelect
    )
    region = models.StringField(
        verbose_name='',
    )
    # region = models.StringField(
    #     label="In welchem Bundesland wohnen Sie?",
    #     choices=[
    #         'Burgenland',
    #         'Kärnten',
    #         'Niederösterreich',
    #         'Oberösterreich',
    #         'Salzburg',
    #         'Steiermark',
    #         'Tirol',
    #         'Vorarlberg',
    #         'Wien',
    #         'Ich wohne nicht in Österreich.'
    #     ],
    #     widget=widgets.Dropdown,
    # )
    donate_blood_ever = models.StringField(
        choices=['Ja', 'Nein'],
        widget=widgets.RadioSelect
    )
    donate_blood_last_2_years = models.StringField(
        choices=['Ja', 'Nein'],
        widget=widgets.RadioSelect
    )
    # born = models.StringField()
    # income_ladder = models.IntegerField(
    #     choices=[i for i in range(1, 11)],
    #     blank=True,
    #     label="Where would you place yourself on this ladder?"
    # )
    # education = models.StringField(
    #     choices=[
    #         "Keine formale Bildung",
    #         "Primarstufe (ca. 5–12 Jahre)",
    #         "Sekundarstufe I (ca. 12–15 Jahre)",
    #         "Sekundarstufe II (ca. 15–18 Jahre)",
    #         "Postsekundäre, nicht-tertiäre Bildung (z.B. Berufsausbildung)",
    #         "Bachelor oder gleichwertiger Abschluss",
    #         "Master oder gleichwertiger Abschluss",
    #         "Doktorgrad (PhD) oder gleichwertiger Abschluss",
    #     ],
    #     verbose_name='Was ist der höchste Bildungsabschluss, den Sie abgeschlossen haben?',
    #     widget=widgets.RadioSelect
    # )
    rural = models.StringField(
        choices=["Einer ländlichen Gegend oder einem Dorf",
                 "Einer kleinen oder mittelgroßen Stadt",
                 "Einer Großstadt",],
        verbose_name='Würden Sie sagen, Sie leben in ...?',
        widget=widgets.RadioSelect
    )

    ## Comment field
    # question_box = models.LongStringField(
    #     verbose_name='Could you tell us, in your own words, what the study was about?'
    # )
    comment_box = models.LongStringField(
        verbose_name='Wenn Sie weitere Anmerkungen zur Studie haben, teilen Sie uns diese bitte im Feld unten mit.',
        blank = True  # Optional: allow it to be empty if no donation is made
    )


########### PAGES ############

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender','live', 'grow_up', 'region', 'rural', 'donate_blood_ever', 'donate_blood_last_2_years']

    def error_message(self, values):
        # 'values' is a dictionary like {'age': 25}
        if values['age'] is not None:  # Check if a value was entered
            if values['age'] < 0:
                # Return a dictionary mapping field name to error message
                return {'age': 'Das Alter muss größer oder gleich 0 sein.'}
            if values['age'] > 100:
                return {'age': 'Das Alter muss kleiner oder gleich 100 sein.'}

    def vars_for_template(player: Player):

        return {
            'live_question': f"Wohnen Sie in Österreich?",
            'region_question': "In welchem Bundesland wohnen Sie?",
            'grow_up_question': f"Sind Sie in Österreich aufgewachsen?",
            'donate_blood_ever_question': f"Haben Sie schon einmal Blut gespendet?",
            'donate_blood_last_2_years_question': f"Haben Sie in den letzten 2 Jahren Blut gespendet?",
        }

    # def before_next_page(player: Player, timeout_happened):


# class Ladder(Page):
#     form_model = 'player'
#     form_fields = ['income_ladder']
#
#     @staticmethod
#     def vars_for_template(player: Player):
#         return dict(
#             ladder_values=list(range(10, 0, -1)),  # From 10 to 1
#         )
#
#     def before_next_page(player: Player, timeout_happened):

class CommentBox(Page):
    form_model = 'player'
    form_fields = ['comment_box']



class Payment(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    def vars_for_template(player: Player):
        return {
            'participation_fee': player.session.config['participation_fee'],
        }


class ProlificLink(Page):
    """
    This page redirects pp to prolific automatically with a javascript (don't forget to put paste the correct link!).
    There is a short text, the completion code and the link in case it is not automatic.
    """
    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == C.NUM_ROUNDS:
            return True


page_sequence = [Demographics,
                 CommentBox,
                 Payment,
                 ProlificLink]
