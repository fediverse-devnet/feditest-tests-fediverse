"""
Test diamond delete

1. `actor-b1@b1.example` follows `actor-a@a.example`, `actor-b2@b2.example` follows `actor-a@a.example`, `actor-c@c.example` follows `actor-b1@b1.example` and `actor-b2@b2.example`
2. `actor-a@a.example`: `Create(Note-X)`
3. `actor-b1@b1.example` and `actor-b2@b2.example`: both receive `Create(Note-X)` and `Note-X` is now in `actor-b1@b1.example`'s and `actor-b2@b2.example`'s inboxes
4. `actor-b1@b1.example`: `Announce(Note-X)` and `actor-b2@b2.example`: `Announce(Note-X)`
5. `actor-c@c.example`: receives `Announce(Note-X)` at least once, and `Note-X` is now in `actor-c@c.example`'s inbox in a single copy
6. `actor-a@a.example`: `Delete(Note-X)`
7. On `b1.example`, `b2.example` and `c.example`, `Note-X` is now inaccessible (404) or has been replaced with a tombstone

FIXME: this should delete the Note but also the Announce's?

FIXME
"""
