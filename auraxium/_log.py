import logging


class RedactingFilter(logging.Filter):
    """Custom logging filter for removing sensitive data from logs.

    To use, instantiate this class with one or more strings to redact:

        logger = logging.getLogger('auraxium')
        logger.addFilter(RedactingFilter(['password', 'token'])

    """

    def __init__(self, secrets: list[str] | str, *args: str) -> None:
        super().__init__()
        if isinstance(secrets, str):
            secrets = [secrets]
        secrets.extend(args)
        self._secrets = secrets

    def filter(self, record: logging.LogRecord) -> bool:
        for secret in self._secrets:
            # Remove any sensitive data from the message itself
            record.msg = record.msg.replace(secret, 'REDACTED')
            # Also remove it from any arguments (used for lazy formatting)
            rec_args = record.args
            if isinstance(rec_args, tuple):
                record.args = tuple(arg.replace(secret, 'REDACTED')
                                    if isinstance(arg, str) else arg
                                    for arg in rec_args)
        return True
