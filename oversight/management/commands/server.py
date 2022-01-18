import sys
from importlib.metadata import version

import gunicorn.app.base
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.management.color import color_style


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict(
            [
                (key, value)
                for key, value in self.options.items()
                if key in self.cfg.settings and value is not None
            ]
        )
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "addrport",
            nargs="?",
            type=str,
            default="0.0.0.0:8000",
            help="Optional port number, or ipaddr:port",
        )

    def handle(self, *args, **options):
        style = color_style()
        call_command("migrate")

        addrport = options["addrport"]
        if addrport.isnumeric():
            addrport = f"0.0.0.0:{addrport}"

        options = {
            "workers": 4,
            "accesslog": "-",
            "disable_redirect_access_to_syslog": True,
            "preload_app": True,
            "bind": addrport,
        }

        from oversight.wsgi import application

        v = version("oversight")
        print(style.SUCCESS(f"oversight (v{v}) setup done, starting webserver..."))
        sys.stdout.flush()
        sys.stderr.flush()

        StandaloneApplication(application, options).run()
