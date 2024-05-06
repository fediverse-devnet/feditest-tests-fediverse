"""
After #23, accept the follow on behalf of the user who received it. Check that the service deliver an Accept back to the inbox of the actor of the Follow. https://www.w3.org/TR/activitypub/#follow-activity-inbox , https://www.w3.org/TR/activitypub/#accept-activity-inbox

From https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/24
"""

from feditest import step, test
from . import AbstractFollowTest


@test
class AcceptFollowTest(AbstractFollowTest):
    """
    Test that an Actor can follow another.
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
    def setup_follow(self):
        self.follower_node_node.make_a_follow_b(self.follower_actor_uri, self.leader_actor_uri, self.leader_node)


    @step
    def now_related(self):
        # The follow relationship has been established on both sides
        super.test_following()

