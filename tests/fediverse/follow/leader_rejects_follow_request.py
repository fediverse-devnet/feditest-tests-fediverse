"""
1. Both `actor-a@a.example` and `actor-b@b.example`'s Followers and Following lists do not contain each other
2. `actor-b@b.example`: `Follow(actor-a@a.example)`
3. `actor-a@a.exmaple` receives `Follow(actor-a@a.example)`
4. `actor-a@a.example`: `Reject(Follow)`
5. `actor-b@b.exmaple` receives `Reject(Follow)`
6. Both `actor-a@a.example` and `actor-b@b.example`'s Followers and Following lists do not contain each other

FIXME
"""
