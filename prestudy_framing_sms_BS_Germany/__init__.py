from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'prestudy_framing_sms_BS_Germany'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):

    for player in subsession.get_players():
        participant = player.participant

        participant.condition_SMS = random.choice(['opt_in', 'opt_out_warten_zusagen'])
        #participant.opt_in_first = random.choice([True, False])
        print('set condition_SMS to', participant.condition_SMS)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # intention = models.StringField(
    #     choices=[
    #         [0, 'Strongly disagree'], [1, 'Disagree'], [2, 'Slightly disagree'],
    #         [3, 'Slightly agree'], [4, 'Agree'], [5, 'Strongly agree'],
    #     ],
    #     verbose_name='',
    #     widget=widgets.RadioSelectHorizontal
    # )
    intention = models.IntegerField(
        choices=[
            [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'],
        ],
        verbose_name='',
        widget=widgets.RadioSelectHorizontal,
    )
    manip1 = models.IntegerField(
        choices=[
            [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'],
        ],
        verbose_name='',
        widget=widgets.RadioSelectHorizontal
    )
    manip2 = models.IntegerField(
        choices=[
            [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'],
        ],
        verbose_name='',
        widget=widgets.RadioSelectHorizontal
    )
    manip3 = models.IntegerField(
        choices=[
            [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'],
        ],
        verbose_name='',
        widget=widgets.RadioSelectHorizontal
    )
    manip4 = models.IntegerField(
        choices=[
            [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'],
        ],
        verbose_name='',
        widget=widgets.RadioSelectHorizontal
    )
    threat_freedom = models.IntegerField(
        choices=[
            [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'],
        ],
        verbose_name='',
        widget=widgets.RadioSelectHorizontal
    )
    anger = models.IntegerField(
        choices=[
            [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'],
        ],
        verbose_name='',
        widget=widgets.RadioSelectHorizontal
    )
    understanding = models.IntegerField(
        choices=[
            [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'],
        ],
        verbose_name='',
        widget=widgets.RadioSelectHorizontal
    )
    duSie = models.IntegerField(
        choices=[
            [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'],
        ],
        verbose_name='',
        widget=widgets.RadioSelectHorizontal
    )
    treatment = models.StringField()


##### PAGES

class Consent(Page):

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 1:
            return True
        else:
            return False

    def vars_for_template(player: Player):

        return {
            'participation_fee': player.session.config['participation_fee'],
        }

class DefaultSMSPage(Page):
    form_model = 'player'
    form_fields = ['intention', 'manip3', 'manip4', 'manip1', 'manip2', 'threat_freedom', 'anger', 'understanding']

    def vars_for_template(player: Player):

        condition_SMS = player.participant.condition_SMS

        image_file = f"global/{condition_SMS}_v3.png"

        player.treatment = condition_SMS

        return dict(
            image_file=image_file,
            intro = 'Stellen Sie sich vor, Sie erhalten folgende SMS-Nachricht, die Sie zur Blutspende einlädt. <br> <b> Bitte lesen Sie die Nachricht aufmerksam durch und bewerten Sie anschließend die unten stehenden Aussagen dazu.</b> <br> <br>',
            #intro2 = 'Bitte bewerten Sie die unten stehenden Aussagen zur SMS',
            #intention_q='Inwieweit motiviert Sie diese Nachricht, Blut zu spenden?',
            intention_q='Wie wahrscheinlich ist es, dass Sie infolge dieser Nachricht Blut spenden?',
            manip3_q='Die Nachricht impliziert, dass bereits eine Auswahl für einen Blutspendetermin für mich getroffen wurde.',
            manip4_q='Die Nachricht suggeriert, dass ich mich aktiv um den Blutspendetermin bemühen muss.',
            #manip5_q='Ich habe das Gefühl, dass ein Blutspendetermin für mich vorausgewählt worden ist.',
            manip1_q = 'Die Nachricht scheint davon auszugehen, dass ich bereits vorhabe, einen Blutspendetermin wahrzunehmen.',
            #manip2_q = 'Die Nachricht impliziert, dass eine Blutspende für mich der vorgesehene nächste Schritt ist.',
            manip2_q='Die Nachricht impliziert, dass eine Blutspende für mich bereits vorgesehen ist.',
            threat_freedom_q='Die Nachricht hat versucht, mich unter Druck zu setzen.',
            anger_q='Die Nachricht hat mich genervt.',
            understanding_q='Ich habe klar verstanden, was die Nachricht sagen wollte.',
        )


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Consent,
                 DefaultSMSPage,
                 ]
