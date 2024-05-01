"""
Double-hop rely attached to the original post and intermediate post

1. `actor-b@b.example` follows `actor-a@a.example`, `actor-c@c.example` follows `actor-b@b.example`
2. `actor-a@a.example`: `Create(Note-X)`
3. `actor-b@b.example`: receives `Create(Note-X)` and `Note-X` is now in `actor-b@b.example`'s inbox
4. `actor-b@b.example`: `Announce(Note-X)`
5. `actor-c@c.example`: receives `Announce(Note-X)`, and `Note-X` is now in `actor-c@c.example`'s inbox
6. `actor-c@c.example`: `Create(Note-Y)` with `inReplyTo(Note-X)`
7. `actor-a@a.example` and `actor-b@b.example`: both receive `Create(Note-Y)`, responds with HTTP 2xx
6. On `a.example` and `b.example`, `Note-Y` is now shown as rely to `Note-X`

FIXME
"""