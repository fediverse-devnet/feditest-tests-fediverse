"""
Don't accept Create by the wrong actor

Similar to #30: when you get a Create, you should check that the object's attributedTo is the same actor that owns the key used in the activity's signature, usually an HTTP Signature.

Background: https://www.w3.org/wiki/SocialCG/ActivityPub/Authentication_Authorization

See also: https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/32

1. `actor-b@b.example` follows `actor-a@a.example`
2. `actor-a@a.example`: `Create(Note-X)`, signed by `actor-c@c.example` and sent to `actor-b@b.example`'s personal inbox
3. `a.example` ignores `Note-X`

FIXME
"""