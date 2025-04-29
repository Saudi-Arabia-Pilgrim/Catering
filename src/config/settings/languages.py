from django.conf import settings

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('ar', 'Arabic'),
    ('en', 'English'),
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGE = ('en', 'uz')

USE_I18N = True

LOCALE_PATHS = [
    settings.BASE_DIR / 'locale',
]