"""
Deliver a Follow activity with object pointing to an existing user. Check that that user receives a notification of the follow request.

From https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/23

FIXME
"""

from feditest import step, test
from . import AbstractFollowTest

@test
class ReceivesFollowTest(AbstractFollowTest):
    """
    Test that a would-be leader receives a follow request.
    """

    @step
    def get_actors(self):
        super().get_actors()


    @step
    def get_collections(self):
        super().get_collections();


    @step
    def initially_unrelated(self):
        # Initially they are unrelated
        super().test_unrelated();


    @step
    def send_follow(self):
        self.follow_request_follower_node = self.follower_node.send_follow_activity(self.follower_actor_uri, self.leader_actor_uri, self.leader_node)


    @step
    def follow_received(self):
        self.follow_request_on_leader_node = self.leader_node.wait_for_object_in_inbox(self.follower_actor_uri, self.follow_request)


    @step
    def still_unrelated(self):
        # Initially they are unrelated
        super().test_unrelated();
