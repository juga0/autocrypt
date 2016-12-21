Autocrypt in-band key discovery
===============================

Autocrypt key discovery happens through headers of mail messages sent between mail apps. Similar to TLS's machine to machine handshake, users first need to have a cleartext mail exchange.  Subsequent mails from the receiving peer will may then be encrypted.  Mail apps show encryptability to their users at "compose-mail" time and give them a choice of encryption or cleartext, defaulting to what the other side has specified in their header.

Autocrypt key discovery is safe only against passive eavesdroppers. It is trivial for providers to perform active downgrade or man-in-the-middle attacks on Autocrypt's key discovery.  Users may, however, detect such tampering if they out-of-band verify their keys at some later point in time.  This possiblity in turn is likely to keep most providers honest or at least prevent them from performing active attacks on a massive scale.

.. contents::

Basic network protocol flow
---------------------------

Establishing encryption happens as a side effect when people send each other mail:

- A MUA always adds an ``Autocrypt:`` header to all messages it
  sends out.

- A MUA will scan incoming mails for encryption headers and associate
  the info with a canonicalized version of the ``From:`` address contained
  in the :rfc:`822` message.

- A MUA will encrypt a message if it earlier saw encryption keys for all
  recipients.

Autocrypt does not prescribe or describe encryption algorithms or key formats.  It is meant to work nicely with ordinary PGP keys, however.

Header Format
-------------

The ``Autocrypt:`` header MUST have the following format:
```
Autocrypt-ENCRYPTION: to=aaa@bbb.cc; [type=(p|...);] [prefer-encrypted=(yes|no);] key=BASE64
```

Where key includes a Base64 representation of a minimal key. For now we only support 'p' as the type, which represents a specific subset of OpenPGP (see key-formats.rst).
'prefer-encrypted' indicates that agents should default to encrypting when composing emails.
Autocrypt compatible Agents MUST include one header with a key in a Autocrypt compatible format.

"Happy path" example: 1:1 communication
---------------------------------------

Consider a blank state and a first outgoing message from Alice to Bob::

    From: alice@a.example
    To: bob@b.example
    ...

Upon sending this mail, Alice's MUA will add a header which contains her
encryption key::

    Autocrypt: to=alice@a.example; type=p; prefer-encrypted=yes; key=...

Bob's MUA will scan the incoming mail, find Alice's key and store it associated
to the ``alice@a.example`` address taken from the ``to``-attribute.
When Bob now composes a mail to Alice his MUA will find the key and signal to
Bob that the mail will be encrypted and after finalization of the mail encrypt
it.  Moreover, Bob's MUA will add its own Encryption Info::

    Autocrypt: to=bob@b.example; type=p; prefer-encrypted=yes; key=...

When Alice's MUA now scans the incoming mail from Bob it will store
Bob's key and the fact that Bob sent an encrypted mail.  Subsequently
both Alice and Bob will have their MUAs encrypt mails to each other.

If ``prefer-encrypted`` is sent as 'yes' the MUA MUST default to encrypting
the next email. If it is set as 'no' the MUA MUST default to plaintext.
If ``prefer-encrypted`` is not sent the MUA should stick to what it was doing
before. If the attribute has never been sent it's up to the MUA to decide. The
save way to go about it is to default to plaintext to make sure the recipient
can read the email.

We encourage MUA developers to propose heuristics for handling the undirected
case. We will document the best approaches to develop a shared understanding.

group mail communication (1:N)
------------------------------------------

Consider a blank state and a first outgoing message from Alice to Bob
and Carol.  Alice's MUA add a header just like in the 1:1 case so
that Bob and Carol's MUA will learn Alice's key.  After Bob and Carol
have each replied once, all MUAs will have appropriate keys for
encrypting the group communication.

It is possible that an encrypted mail is replied to in cleartext (unencrypted).
For example, consider this mail flow::

    Alice -> Bob, Carol
    Bob -> Alice, Carol
    Carol -> Alice  (not to Bob!)

Alice and Carol have now all encryption keys but Bob only has Alice's
because he never saw a mail from Carol.  Alice can now send an encrypted
mail to Bob and Carol but Bub will not be able to respond encrypted
before his MUA has seen a mail from Carol.  This is fine because Autocrypt
is about **opportunistic** encryption, i.e. encrypt if possible and
otherwise don't get in the way of users.


Loosing access to decryption key
-------------------------------------------

If Alice loses access to her decryption secret:

- she lets her MUA generate a new key

- her MUA will add an Encryption-Info header containing the new key with each mail

- receiving MUAs will replace the old key with the new key

Meanwhile, if Bob sends Alice a mail encrypted to the old key she will
not be able tor ead it.  After she responds (e.g. with "Hey, can't read
your mail") Bob's MUA will see the new key and subsequently use it.

.. todo::

    Check if we can encrypt a mime mail such that non-decrypt-capable clients
    will show a message that helps Alice to reply in the suggested way.  We don't
    want people to read handbooks before using Autocrypt so any guidance we can
    "automatically" provide in case of errors is good.

.. note::

    Unless we can get perfect recoverability (also for device loss etc.) we will
    always have to consider this "fatal" case of loosing a secret key and how
    users can deal with it.  Especially in the federated email context We do
    not think perfect recoverability is feasible.


Dowgrading / switch to a MUA without Autocrypt support
------------------------------------------------------

Alice might decide to switch to a different MUA which does not support Autocrypt.

A MUA which previously saw an Autocrypt header and/or encryption from Alice
now sees an unencrypted mail from Alice and no encryption header. This
will disable encryption to Alice for subsequent mails.


``p`` OpenPGP Based Keyformat
-----------------------------

Autocrypt pins down key formats and algorithms to reduce the requirements
for autocrypt-supporting implementations.  If OpenPGP key format is used, 
the message also uses OpenPGP Message encoding (PGP/MIME, RFC 3156)

**For New Users**

We only include a minimum key in the headers that has:

* a primary key ``Kp``

  * a uid that is the email address
  * a self signature

* one encryption subkey ``Ke``

  * a signature for the subkey by the primary key

… and nothing else. For maximum interoperability and sanity a
certificate sent by an Autocrypt-enabled agent MUST contain exactly
these five OpenPGP packets.

For the key algorithms used at a given level of support see levels.rst

**Reasoning**

*Why ed25519+cv25519*

short keys for short header lines

*why email address as uid*

 Possibilities for uid we considered:

 ======= == == == === ==
 Option  SC BC VO RvK SR
 ======= == == == === ==
 no uid            x  x
 email   x  x   x  x
 fixed         x   x  x
 hash    x      x   x x
 ======= == == == === ==

SC: self-claim. This was very important to us for usability
reasons. This restricted us to either use the email directly or
hashed.

BC: backwards compatibility

VO: valid OpenPGP

RvK: allows revocations using keyservers

SR: Spam resistant/publicly list email addresses

Using a salted hash of the email address for the uid to not list them
on keyservers would prevent the privacy issue of public mail addresses
but the key should not be uploaded in the first place.

Accidental or malicious uploading of keys with associated email
addresses should be prevented by introducing a flag at the keys that
says that keyservers shouldn't accept it.  See `issue #7
<https://github.com/autocrypt/inbome/issues/7>`_.


**For current OpenPGP users**

* What about other keys, that i have been using with other properties?
  (smart-card, RSA, ...)

  * You can still create a compatible header with a tool we will
    provide. We are targeting users who have not used pgp
    before. Nevertheless most clients will still support other key
    formats. But they are not required to.
