import config


def print_verbose(message: str):
    if config.verbose:
        print(
            "==========================================================================================")
        print(message)
