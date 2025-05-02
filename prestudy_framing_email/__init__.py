from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'prestudy_framing_email'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
    NUM_QUESTIONS = 5
    EST_DURATION = 10

class Subsession(BaseSubsession):
    pass

def creating_session(subsession):

    # Create a list of image paths and shuffle it in place
    email_images = [
        'global/email_opt_in.png',
        'global/email_opt_out.png',
        'global/email_opt_out_ease.png',
        'global/email_opt_out_endowment.png',
        'global/email_opt_out_endorsement.png'
    ]

    for player in subsession.get_players():
        participant = player.participant
        random.shuffle(email_images)
        participant.email_shuffled = email_images
        print('set email_shuffled to', participant.email_shuffled)


class Group(BaseGroup):
    pass

class Player(BasePlayer):
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
    ease = models.IntegerField(
        choices=[
            [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'],
        ],
        verbose_name='',
        widget=widgets.RadioSelectHorizontal
    )
    endowment = models.IntegerField(
        choices=[
            [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7'],
        ],
        verbose_name='',
        widget=widgets.RadioSelectHorizontal
    )
    endorsement = models.IntegerField(
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

        return dict(
            participation_fee = player.session.config['participation_fee'],
            num_q = C.NUM_QUESTIONS,
            dur = C.EST_DURATION,
        )

class DefaultEmailPage(Page):
    form_model = 'player'
    form_fields = ['intention', 'manip1', 'manip2', 'ease', 'endowment', 'endorsement', 'threat_freedom', 'anger', 'understanding']

    def vars_for_template(player: Player):

        image_file = player.participant.email_shuffled[player.round_number - 1]

        player.treatment = image_file.split('/')[-1].split('.')[0]  # Save treatment

        return dict(
            image_file=image_file,
            intro='Stellen Sie sich vor, Sie erhalten folgende E-Mail-Nachricht, die Sie zur Blutspende einlädt. <br> <b> Bitte lesen Sie die Nachricht aufmerksam durch und bewerten Sie anschließend die unten stehenden Aussagen dazu.</b> <br> <br>',
            # intro2 = 'Bitte bewerten Sie die unten stehenden Aussagen zur SMS',
            intention_q='Inwieweit motiviert Sie diese Nachricht, Blut zu spenden?',
            manip1_q='Ich habe das Gefühl, dass die Nachricht davon ausgeht, dass ich bereits beabsichtige, einen Blutspendetermin wahrzunehmen.',
            manip2_q='Ich habe das Gefühl, dass die Nachricht impliziert, dass eine Blutspende für mich der normale bzw. vorgesehene nächste Schritt ist.',
            ease_q='Inwieweit vermittelt die Nachricht das Gefühl, dass ein Blutspendetermin einfach zu buchen ist?',
            endowment_q = 'Inwieweit vermittelt die Nachricht das Gefühl, dass dieser Blutspendetermin Ihnen gehört?',
            endorsement_q = 'Inwieweit vermittelt die Nachricht das Gefühl, dass jetzt eine gute Zeit für einen Blutspendetermin ist?',
            threat_freedom_q='Die Nachricht hat versucht, mich unter Druck zu setzen.',
            anger_q='Die Nachricht hat mich genervt.',
            understanding_q='Ich habe klar verstanden, was die Nachricht sagen wollte.',
        )

class ResultsWaitPage(WaitPage):
    pass

class Results(Page):
    pass

page_sequence = [Consent,
                 DefaultEmailPage,
                 ]
