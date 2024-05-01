"""
Accept signature from the creator of the note.

1. `actor-b@b.example` follows `actor-a@a.example`
2. Deliver `Create(Note-X)` to `actor-b@b.example` where `Note-X` has an `actor` of `actor-a@a.example` and no `attributedTo` and where the request is validly signed by the key of `actor-a@a.example`
3. `Note-X` appears in the inbox of `actor-b@b.example`

FIXME
"""