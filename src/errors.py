class NameTooShortError(ValueError):
    pass


def validate(name):
    if len(name) < 10:
        return NameTooShortError(name)
