SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '343166873157-g7ildme8enpp10ii864hsu1lf1kdmcc4.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '7hzdw279O63IdwyCud6V5ytI'

def includeme(config):
    config.registry.settings.update(SOCIAL_AUTH_KEYS)
