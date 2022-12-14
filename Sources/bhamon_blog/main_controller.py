import flask


class MainController:


    def home(self) -> str:
        return flask.render_template("home.html", title = "Home")
