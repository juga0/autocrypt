from experiments import generate_autocrypt, gpg_utils


# def test_generate_reply(datadir, gpg, smtpserver):
#     with datadir.open("rsa2048-simple-to-bot.eml") as fp:
#         reply_msg = generate_reply(gpg, fp)
#     assert reply_msg["To"] == "Alice <alice@testsuite.autocrypt.org>"
#     assert reply_msg["From"] == "bot@autocrypt.org"
#     assert reply_msg["Autocrypt"]
#
#     host, port = smtpserver.addr[:2]
#
#     send_reply(host, port, reply_msg)
#
#     assert len(smtpserver.outbox) == 1


def test_generate_Autocrypt_header(datadir):
    key = gpg_utils.key_from_file(datadir.join('alice_pubkey.asc'))
    uid = 'alice@testsuite.autocrypt.org'
    keybase64 = gpg_utils.key_base64(key)
    autocrypt_header = \
        generate_autocrypt.generate_Autocrypt_header(
            keybase64, uid
        )
    assert autocrypt_header == "to=%(uid)s; key=%(key)s\n" %\
        {'uid': uid, 'key': keybase64}


def test_generate_email(datadir):
    key = gpg_utils.key_from_file(datadir.join('alice_pubkey.asc'))
    sender = 'alice@testsuite.autocrypt.org'
    keybase64 = gpg_utils.key_base64(key)
    keyfp = gpg_utils.key_fp(key)
    recipient = 'bot@autocrypt.org'
    subject = 'This is an example Autocrypt Email'
    autocrypt_header =  \
        generate_autocrypt.generate_Autocrypt_header(
            keybase64, sender)
    msg = generate_autocrypt.generate_email(keybase64, keyfp)
    assert msg["To"] == recipient
    assert msg["From"] == sender
    assert msg["Subject"] == subject
    assert msg["Autocrypt"] == autocrypt_header
    assert msg.get_payload() == keyfp



def test_send_email(datadir):
    from email.parser import Parser
    with datadir.open("alice_mail.txt") as fp:
        msg = Parser().parsestr(fp.read())
    r = generate_autocrypt.send_email(msg, recipient='root@localhost')
    assert r == None
