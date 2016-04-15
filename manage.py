#!/usr/bin/env python
import os
import sys

# import dotenv

if __name__ == "__main__":
    # dotenv.read_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proqodpy.settings")
    os.environ.setdefault(
        "SECRET_KEY", "5(15ds+i2+\%ik6z&!yer+ga9m=e\%jcqiz_5wszg)r-z!2--b2d")
    os.environ.setdefault("DB_NAME", "proqod")

    os.environ.setdefault("DB_USER", "")
    os.environ.setdefault("DB_PASS", "")
    os.environ.setdefault("DB_SERVICE", "")
    os.environ.setdefault("DB_PORT", "5432")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
