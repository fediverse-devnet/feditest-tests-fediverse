"""
Replies are propagated across the comment tree

Note: I don't think this is what is currently implemented, but I argue it should be, otherwise the Fediverse remains incomprehensible to people

1. `actor-b1@b1.example` follows `actor-a@a.example`, `actor-b2@b2.example` follows `actor-a@a.example`, `actor-c1@c1.example` follows `actor-b1@b1.example`
2. `actor-a@a.example`: `Create(Note-X)`
3. `actor-b1@b1.example` and `actor-b2@b2.example`: both receive `Create(Note-X)` and `Note-X` are now in their inboxes
4. `actor-b1@b1.example`: `Announce(Note-X)`
5. `actor-c1@c1.example`: receives `Announce(Note-X)`, and `Note-X` is now in `actor-c1@c1.example`'s inbox
6. `actor-b2@b2.example`: `Create(Note-Y)` with `inReplyTo(Note-X)`
7. `actor-a@a.example`, `actor-b1@b1.example` and `actor-c1@c1.example`: all receive `Create(Note-Y)`, respond with HTTP 2xx
6. On `a.example`, `b1.example`, `b2.example` and `c1.example`, `Note-Y` is now shown as reply to `Note-X`

FIXME -- create this after single_hop and double_hop work.

"""