"""
Deliver a Create of a Note to a user's inbox. Check that it returns HTTP 200 or 202, and that it's visible to the user when they search for it by the Note's id. https://www.w3.org/TR/activitypub/#delivery

From https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/14

1. `actor-b@b.example` follows `actor-a@a.example`
2. `actor-a@a.example`: `Create(Note-X)` and deliver it to `actor-b@b.example`'s personal inbox
3. `b.example` has received a message of `Create(Note-X)` and responded with HTTP 200 or 202.

FIXME
"""