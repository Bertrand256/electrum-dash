import re


ELECTRUM_VERSION = '4.1.7.2' # version of the client package
APK_VERSION = '4.1.7.2'      # read by buildozer.spec

PROTOCOL_VERSION = '1.4.2'   # protocol version requested

# The hash of the mnemonic seed must begin with this
SEED_PREFIX      = '01'      # Standard wallet


def seed_prefix(seed_type):
    if seed_type == 'standard':
        return SEED_PREFIX
    raise Exception(f"unknown seed_type: {seed_type}")


VERSION_PATTERN = re.compile('^([^A-Za-z]+).*')  # simpliified PEP440 versions


def is_release():
    v = VERSION_PATTERN.match(ELECTRUM_VERSION).group(1)
    return v == ELECTRUM_VERSION
