"""
Same as previous, but with a shared inbox on a different host (`actor-b@b.example`'s shared inbox is on `c.example`)

Note: We assume that if this test passes, other activities can also be delivered via
a sharedInbox on a different host.

FIXME

This may not be a separate test. We could run deliver_to_inbox, but with a Node whose shared inbox
is on a different host. FIXME?
"""