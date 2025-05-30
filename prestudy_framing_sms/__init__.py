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

def creating_session(subsession):

    # Create a list of image paths and shuffle it in place
    opt_out_images = [
        'global/opt_out_warten_bestaetigen_v2.png',
        'global/opt_out_warten_zusagen_v2.png',
        'global/opt_out_bereit_bestaetigen_v2.png',
        'global/opt_out_bereit_zusagen_v2.png'
    ]

    for player in subsession.get_players():
        participant = player.participant

        participant.opt_in_first = random.choice([True, False])

        opt_out_images_copy = opt_out_images.copy()
        random.shuffle(opt_out_images_copy)
        participant.opt_out_shuffled = opt_out_images_copy

        # random.shuffle(opt_out_images) # Important: Shuffle is not assigned to participant, because opt_out_images as a list is a mutable object! All participants will be assigned the last shuffled order!
        # participant.opt_out_shuffled = opt_out_images

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
    form_fields = ['intention', 'manip1', 'manip2', 'threat_freedom', 'anger', 'understanding']

    def vars_for_template(player: Player):

        opt_in_first = player.participant.opt_in_first

        if opt_in_first:
            if player.round_number == 1:
                image_file = 'global/opt_in_v2.png'
            else:
                image_file = player.participant.opt_out_shuffled[player.round_number - 2]
        else:
            if player.round_number == 5:
                image_file = 'global/opt_in_v2.png'
            else:
                image_file = player.participant.opt_out_shuffled[player.round_number-1]

        player.treatment = image_file.split('/')[-1].split('.')[0] # Save treatment

        return dict(
            image_file=image_file,
            intro = 'Stellen Sie sich vor, Sie erhalten folgende SMS-Nachricht, die Sie zur Blutspende einlädt. <br> <b> Bitte lesen Sie die Nachricht aufmerksam durch und bewerten Sie anschließend die unten stehenden Aussagen dazu.</b> <br> <br>',
            #intro2 = 'Bitte bewerten Sie die unten stehenden Aussagen zur SMS',
            intention_q='Inwieweit motiviert Sie diese Nachricht, Blut zu spenden?',
            manip1_q = 'Ich habe das Gefühl, dass die Nachricht davon ausgeht, dass ich bereits beabsichtige, einen Blutspendetermin wahrzunehmen.',
            manip2_q = 'Ich habe das Gefühl, dass die Nachricht impliziert, dass eine Blutspende für mich der normale bzw. vorgesehene nächste Schritt ist.',
            threat_freedom_q='Die Nachricht hat versucht, mich unter Druck zu setzen.',
            anger_q='Die Nachricht hat mich genervt.',
            understanding_q='Ich habe klar verstanden, was die Nachricht sagen wollte.',
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

        image_file = 'global/duSie_v2.png'

        return dict(
            image_file=image_file,
            intro='Stellen Sie sich vor, Sie erhalten folgende SMS-Nachrichten, die Sie zur Blutspende einladen. <br> <b> Bitte lesen Sie die Nachrichten aufmerksam durch und bewerten Sie anschließend die unten stehende Aussage dazu.</b> <br> <br>',
            duSie_q = 'Würden Sie lieber mit „Sie“ (links) oder mit „du“ (rechts) angesprochen werden?',
        )


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Consent,
                 DefaultSMSPage,
                 FormalInformal,
                 ]
