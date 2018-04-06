from datetime import datetime


def timestamp_onlydigit():
    return ''.join(filter(lambda x: x.isdigit(), str(datetime.now())))