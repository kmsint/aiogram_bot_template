from fluentogram import TranslatorRunner


def get_lang_buttons(
    locales: list[str], i18n: TranslatorRunner
) -> list[tuple[str, str]]:
    buttons = []
    for i, locale in enumerate(locales, 1):
        buttons.append((i18n.get("{}-lang".format(locale)), str(i)))
    return buttons
