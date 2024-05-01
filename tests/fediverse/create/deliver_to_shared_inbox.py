"""
Same as #14, but delivered to a user's sharedInbox. https://www.w3.org/TR/activitypub/#shared-inbox-delivery

See also: https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/15

1. `actor-b@b.example` follows `actor-a@a.example`. `actor-b@b.example` declares a shared inbox whose endpoint is on the same host `b.example`.
2. `actor-a@a.example`: `Create(Note-X)` an deliver it to `actor-b@b.example`'s shared inbox
3. `b.example` has received a message of `Create(Note-X)` and responded with HTTP 200 or 202.

FIXME
"""