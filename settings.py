# Configure Django App for Heroku.
import django_heroku

django_heroku.settings(locals())
TEST_RUNNER = 'django_heroku.HerokuDiscoverRunner'
