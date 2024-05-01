"""
Extending on #19:

    7.3
    Unlike the client to server handling of the Update activity, this is not a partial update but a complete replacement of the object.

    Deliver a Create(Note) with an explicitly optional value (i.e. summary) defined
    Deliver an Update(Note) with that value removed (do not send it in at all)
    Retrieval of said note should reflect that the summary value has been nulled or removed.

From https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/29

FIXME
"""
