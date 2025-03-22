import os
import gettext

# Localization setup
locale = 'ru'
locale_dir = os.path.join(os.path.dirname(__file__), "locale")
gettext.bindtextdomain("messages", locale_dir)
gettext.textdomain("messages")
lang = gettext.translation('messages', localedir=locale_dir, languages=[locale])
lang.install()

_ = lang.gettext  # Translation function