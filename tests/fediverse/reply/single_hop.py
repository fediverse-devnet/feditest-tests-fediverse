"""
Deliver a Note with inReplyTo of an existing Note to a user's inbox. Check that it returns HTTP 2xx, is visible to the target user, and appears attached to the inReplyTo Note.

See also: https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/16

1. `actor-b@b.example` follows `actor-a@a.example`
2. `actor-a@a.example`: `Create(Note-X)`
3. `actor-b@b.example`: receives `Create(Note-X)` and `Note-X` is now in `actor-b@b.example`'s inbox
4. `actor-b@b.example`: `Create(Note-Y)` with `inReplyTo(Note-X)`
5. `actor-a@a.example`: receives `Create(Note-Y)`, responds with HTTP 2xx
6. On `a.example`, `Note-Y` is now shown as reply to `Note-X`

FIXME
"""

