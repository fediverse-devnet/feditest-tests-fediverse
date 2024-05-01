"""
Accept signature from the actor listed as isAttributedTo

1. `actor-b@b.example` follows `actor-a@a.example`
2. Deliver `Create(Note-X)` to `actor-b@b.example` where `Note-X` has an `actor` of `actor-a@a.example`, and `attributedTo` of `actor-c@c.example` and where the request is validly signed by the key of `actor-c@c.example`
3. `Note-X` appears in the inbox of `actor-b@b.example`

FIXME
"""