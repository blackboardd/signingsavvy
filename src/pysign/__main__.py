import logging

if __name__ == "__main__":
    def __init__(self, loglevel):
        level = getattr(logging, loglevel.upper(), None)
        if not isinstance(level, int):
            raise ValueError(f"Bad log level: {level}")
