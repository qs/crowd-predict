SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '407519338285-8tfusg5fhrk2iunem6p41qbibq7k1ujt.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'ifc2xmi4-ZDRMsuLwqBRj9mt'

def includeme(config):
    config.registry.settings.update(SOCIAL_AUTH_KEYS)
