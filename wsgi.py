activate_this = '/deploy/project/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# give wsgi the application
from app import create_app
application = create_app()

if __name__ == '__main__':
    application.run()