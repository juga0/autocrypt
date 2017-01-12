Introducing Autocrypt: E-Mail Encryption for Everyone
=====================================================

**If users ask how they can secure their e-mail the answer
should be as simple as: use an Autocrypt-enabled mail app!**

**Why improve e-mail?** E-Mail has been declared dead many times but
refuses to die. It remains the largest open federated identity and
messaging eco-system, anchors the web, mobiles and continues to relay
sensitive information between people and organisations. It has
problems but do you prefer the proprietary, easy-to-track mobile phone
number system to become the single source of digital identification?

**Why a new approach to e-mail encryption?**  Encrypted e-mail has been
around for decades, but has failed to see wide adoption outside of
specialist communities, in large part because of difficulties with user
experience and certification models.  Autocrypt first aims to provide
convenient encryption that is neither perfect nor as secure as
traditional e-mail encryption, but is convenient enough for
much wider adoption.

The social Autocrypt approach
------------------------------

The Autocrypt project is driven by a diverse group of mail app developers,
hackers and researchers who are willing to take fresh approaches, learn from
past mistakes, and collectively aim to increase the overall encryption
of e-mail in the net.  The group effort was born and named "Autocrypt"
on December 17th 2016 by ~20 people during a 5-day meeting at the
OnionSpace in Berlin. It's a dynamic, fun process which is open to
new people, influences and contributions.  See :doc:`contact channels
and upcoming events <contact>` on how you may talk with us and who
"we" are currently.


The technical Autocrypt approach
--------------------------------------

Autocrypt uses regular e-mail messages between people to piggyback
necessary information to allow encrypting subsequent messages; it
adds a new ``Autocrypt`` e-mail header for transfering public keys and
driving encryption behaviour. By default, key management is not visible
to users. See :doc:`features` for more technical and UI cornerstones.

We are following this approach step-by-step using different "Levels"
of implementation compliance.  Driven by usability concerns, we are
refining and implementing :doc:`Level 0 <level0>` in several mail apps
during Spring 2017.  If you are interested to help please :doc:`join our
channels and look at where we meet next <contact>`.

See :doc:`contents` for an index of all docs and discussion results so far.
