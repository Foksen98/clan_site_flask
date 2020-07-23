from flask_script import Manager
from app.create_app import app
from app.main import main as main_blueprint
from dateutil.parser import parse


app.register_blueprint(main_blueprint)
manager = Manager(app)


@app.template_filter('date')
def _jinja2_filter_datetime(date, format):
    if date :
        return parse(date).strftime(format)


if __name__ == '__main__':
	manager.run()
