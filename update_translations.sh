#!/bin/bash

find . -name "*.py" | xargs xgettext --from-code=UTF-8 -o locale/messages.pot

for lang in locale/*; do
    if [ -d "$lang/LC_MESSAGES" ]; then
        msgmerge -U "$lang/LC_MESSAGES/messages.po" locale/messages.pot
    fi
done

for lang in locale/*; do
    if [ -d "$lang/LC_MESSAGES" ]; then
        msgfmt -o "$lang/LC_MESSAGES/messages.mo" "$lang/LC_MESSAGES/messages.po"
    fi
done

echo "Localization updated and compiled!"
