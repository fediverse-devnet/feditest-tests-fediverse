"""
Extending on #19:

    7.3
    The receiving server MUST take care to be sure that the Update is authorized to modify its object. At minimum, this may be done by ensuring that the Update and its object are of same origin.

    Deliver a Create(Note)
    Deliver an Update(Note) from a different origin
    Retrieval of said note should reflect an unchanged object
    The Update request should fail with a 4xx error.

From: https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/30

1. `actor-b@b.example` follows `actor-a@a.example`
2. `actor-a@a.example`: `Create(Note-X)`
3. `actor-b@b.example`: receives `Create(Note-X)` and `Note-X` is now in `actor-b@b.example`'s inbox
4. `actor-c@c.example`: `Update(Note-X)`
5. `actor-b@b.example`: `Note-X` is unchanged on `b.example`

FIXME
"""