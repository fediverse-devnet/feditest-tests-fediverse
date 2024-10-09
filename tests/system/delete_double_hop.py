"""
Test double-hop delete

1. `actor-b@b.example` follows `actor-a@a.example`, `actor-c@c.example` follows `actor-b@b.example`
2. `actor-a@a.example`: `Create(Note-X)`
3. `actor-b@b.example`: receives `Create(Note-X)` and `Note-X` is now in `actor-b@b.example`'s inbox
4. `actor-b@b.example`: `Announce(Note-X)`
5. `actor-c@c.example`: receives `Announce(Note-X)`, and `Note-X` is now in `actor-c@c.example`'s inbox
6. `actor-a@a.example`: `Delete(Note-X)`
7. On `b.example` and `c.example`, `Note-X` is now inaccessible (404) or has been replaced with a tombstone

FIXME
"""
