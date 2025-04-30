from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'prestudy_framing_sms'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5


class Subsession(BaseSubsession):
    pass

def creating_session(subsession): # Just for testing treatment allocation, will eventually me moved to create-session in baseline trials

    # Create a list of image paths and shuffle it in place
    opt_out_images = [
        'images/opt_out_warten_bestaetigen.png',
        'images/opt_out_warten_zusagen.png',
        'images/opt_out_bereit_bestaetigen.png',
        'images/opt_out_bereit_zusagen.png'
    ]

    for player in subsession.get_players():
        participant = player.participant

        participant.opt_in_first = random.choice([True, False])

        random.shuffle(opt_out_images)
        participant.opt_out_shuffled = opt_out_images
        print('set opt_out_shuffled to', participant.opt_out_shuffled)
        print('set opt_in_first to', participant.opt_in_first)


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
    form_fields = ['manip1', 'manip2', 'threat_freedom', 'anger', 'understanding', 'intention']

    def vars_for_template(player: Player):

        opt_in_first = player.participant.opt_in_first

        if opt_in_first:
            if player.round_number == 1:
                image_file = 'global/image1.png'
            else:
                image_file = player.participant.opt_out_shuffled[player.round_number - 2]
        else:
            if player.round_number == 5:
                image_file = 'global/image1.png'
            else:
                image_file = player.participant.opt_out_shuffled[player.round_number-1]


        return dict(
            image_file=image_file,
            intro = 'Stellen Sie sich vor, Sie erhalten folgende SMS-Nachricht, die Sie zur Blutspende einlädt. <br> <b> Bitte lesen Sie den Text aufmerksam durch und bewerten Sie anschließend die unten stehenden Aussagen dazu.</b> <br> <br>',
            manip1_q = 'Ich habe das Gefühl, dass die Nachricht davon ausgeht, dass ich bereits beabsichtige, einen Blutspendetermin wahrzunehmen.',
            manip2_q = 'Ich habe das Gefühl, dass die Nachricht impliziert, dass eine Blutspende für mich der normale bzw. vorgesehene nächste Schritt ist.',
            threat_freedom_q='Die Nachricht hat versucht, mich unter Druck zu setzen.',
            anger_q='Die Nachricht hat mich genervt.',
            understanding_q='Ich habe klar verstanden, was die Nachricht sagen wollte.',
            intention_q='Inwieweit motiviert Sie diese Nachricht, einen Blutspendetermin wahrzunehmen?',
        )


class FormalInformal(Page):

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 5:
            return True
        else:
            return False

    form_model = 'player'
    form_fields = ['duSie']

    def vars_for_template(player: Player):

        image_file = 'images/duSie.png'

        return dict(
            image_file=image_file,
            intro='Stellen Sie sich vor, Sie erhalten folgende SMS-Nachrichten, die Sie zur Blutspende einladen. <br> <b> Bitte lesen Sie den Text aufmerksam durch und bewerten Sie anschließend die unten stehenden Aussagen dazu.</b> <br> <br>',
            duSie_q = 'Würden Sie lieber mit „Sie“ (links) oder mit „du“ (rechts) angesprochen werden?',
        )


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Consent,
                 DefaultSMSPage,
                 FormalInformal]
