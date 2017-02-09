from experiments import gpg_utils


def test_generate_rsa_key():
    key = gpg_utils.generate_rsa_key('alice@testsuite.autocrypt.org')
    uid = key.userids[0]
    assert uid.email == ''
    assert uid.name == 'alice@testsuite.autocrypt.org'
    # key.key_algorithm
    # key.encrypt
    # key.from_file
    # key.sign
    # key.verify


def test_key_from_file():
    pass


def test_export_key_to_file():
    pass


def test_export_pubkey_to_file():
    pass
