from os import environ
from os import popen

SESSION_CONFIGS = [
    dict(
        name='demographics',
        display_name="demographics",
        app_sequence=['demographics'],
        num_demo_participants=6,
        use_browser_bots=False,
        oTree_version_used=popen('otree --version').read().strip()
    ),
    dict(
        name='prestudy_framing_sms',
        display_name="prestudy_framing_sms",
        app_sequence=['prestudy_framing_sms'],
        num_demo_participants=6,
        use_browser_bots=False,
        oTree_version_used=popen('otree --version').read().strip()
    ),
    dict(
        name='prestudy_framing_email',
        display_name="prestudy_framing_email",
        app_sequence=['prestudy_framing_email'],
        num_demo_participants=6,
        use_browser_bots=False,
        oTree_version_used=popen('otree --version').read().strip()
    ),
    dict(
        name='sms_survey',
        display_name="Default survey (SMS)",
        app_sequence=['prestudy_framing_sms', 'demographics'],
        num_demo_participants=6,
        use_browser_bots=False,
        oTree_version_used=popen('otree --version').read().strip()
    ),
    dict(
        name='email_survey',
        display_name="Default survey (E-Mail)",
        app_sequence=['prestudy_framing_email', 'demographics'],
        num_demo_participants=6,
        use_browser_bots=False,
        oTree_version_used=popen('otree --version').read().strip()
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=1.20, doc=""
)

PARTICIPANT_FIELDS = ['opt_out_shuffled', 'opt_in_first', 'email_shuffled']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

USE_I18N = True  # Enables the translation system

USE_L10N = True  # Enables locale-specific formatting (dates, numbers)

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True

#DEBUG = False

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo',
         display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'CG'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

SECRET_KEY = '8876387233144'

INSTALLED_APPS = ['otree']