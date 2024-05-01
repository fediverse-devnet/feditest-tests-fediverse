"""
After a Follow has been delivered (#29) and accepted (#30), deliver an Undo of the Follow to the followee's inbox. The follower actor should be removed from the followee's list of followers. https://www.w3.org/TR/activitypub/#undo-activity-inbox

From https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/25

Append to leader_accepts_follow_request.py

1. `actor-b@b.example`: `Undo(Follow)`
2. Both `actor-a@a.example` and `actor-b@b.example`'s Followers and Following lists do not contain each other

FIXME
"""