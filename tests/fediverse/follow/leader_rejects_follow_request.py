"""
No issue in Github for this.

1. Both `actor-a@a.example` and `actor-b@b.example`'s Followers and Following lists do not contain each other
2. `actor-b@b.example`: `Follow(actor-a@a.example)`
3. `actor-a@a.exmaple` receives `Follow(actor-a@a.example)`
4. `actor-a@a.example`: `Reject(Follow)`
5. `actor-b@b.exmaple` receives `Reject(Follow)`
6. Both `actor-a@a.example` and `actor-b@b.example`'s Followers and Following lists do not contain each other

FIXME
"""

from feditest import step, test
from . import AbstractFollowTest

@test
class RejectsFollowTest(AbstractFollowTest):
    """
    Test that a would-be leader can reject a follow request.
    """

    @step
    def get_actors(self):
        super.get_actors()


    @step
    def get_collections(self):
        super.get_collections();


    @step
    def initially_unrelated(self):
        # Initially they are unrelated
        super.test_unrelated();


    @step
    def send_follow(self):
        self.follow_request_follower_node = self.follower_node.send_follow_activity(self.follower_actor_uri, self.leader_actor_uri, self.leader_node)


    @step
    def follow_received(self):
        self.follow_request_on_leader_node = self.leader_node.wait_for_object_in_inbox(self.follower_actor_uri, self.follow_request)


    @step
    def send_reject(self):
        self.reject_on_leader_node = self.leader_node.send_reject_activity(self.leader_actor_uri, self.follow_request_on_leader_node)


    @step
    def reject_received(self):
        self.reject_on_follower_node = self.follower_node.wait_for_object_in_inbox(self.follower_actor_uri, self.reject_on_leader_node)


    @step
    def still_unrelated(self):
        # Initially they are unrelated
        super.test_unrelated();
