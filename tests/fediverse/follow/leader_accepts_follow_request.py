"""
After #23, accept the follow on behalf of the user who received it. Check that the service deliver an Accept back to the inbox of the actor of the Follow. https://www.w3.org/TR/activitypub/#follow-activity-inbox , https://www.w3.org/TR/activitypub/#accept-activity-inbox

From https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/24

1. Both `actor-a@a.example` and `actor-b@b.example`'s Followers and Following lists do not contain each other
2. `actor-b@b.example`: `Follow(actor-a@a.example)`
3. `actor-a@a.exmaple` receives `Follow(actor-a@a.example)`
4. `actor-a@a.example`: `Accept(Follow)`
5. `actor-b@b.exmaple` receives `Accept(Follow)`
6. `actor-a@a.example`'s Followers now contains `actor-b@b.example`, and `actor-b@b.example`'s Following now contains `actor-a@a.example`.

FIXME
"""