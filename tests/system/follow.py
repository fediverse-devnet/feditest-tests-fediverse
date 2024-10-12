"""
Tests that actors on two different Fediverse Nodes can:
* follow each other
* followers receive posts by the followed actor,
* and unfollow each other
* and not receive posts by the followed actor any more.
"""

from datetime import datetime

from feditest import AssertionFailure, InteropLevel, SpecLevel, step, test
from feditest.nodedrivers import TimeoutException
from feditest.protocols.fediverse import FediverseNode

@test
class FollowTest:
    def __init__(self,
        leader_node: FediverseNode,
        follower_node: FediverseNode
    ) -> None:
        self.leader_node = leader_node
        self.leader_actor_uri = None
        self.leader_node.set_auto_accept_follow(True)

        self.follower_node = follower_node
        self.follower_actor_uri = None

        self.leader_note_while_following_uri = None
        self.leader_note_after_unfollow_uri = None


    @step
    def provision_actors(self):
        self.leader_actor_uri = self.leader_node.obtain_actor_document_uri()
        assert self.leader_actor_uri

        self.follower_actor_uri = self.follower_node.obtain_actor_document_uri()
        assert self.follower_actor_uri


    @step
    def follow(self):
        self.follower_node.make_follow(self.follower_actor_uri, self.leader_actor_uri)


    @step
    def wait_until_actor_is_followed_by_actor(self):
        self.leader_node.wait_until_actor_is_followed_by_actor(self.leader_actor_uri, self.follower_actor_uri)


    @step
    def wait_until_actor_is_following_actor(self):
        self.follower_node.wait_until_actor_is_following_actor(self.follower_actor_uri, self.leader_actor_uri)


    @step
    def leader_creates_note_while_following(self):
        self.leader_note_while_following_uri = self.leader_node.make_create_note(self.leader_actor_uri, f"Testing leader_creates_note_while_following {datetime.now()}")
        assert self.leader_note_while_following_uri


    @step
    def wait_until_note_received(self):
        self.follower_node.wait_until_actor_has_received_note(self.follower_actor_uri, self.leader_note_while_following_uri)


    @step
    def unfollow(self):
        self.follower_node.make_follow_undo(self.follower_actor_uri, self.leader_actor_uri)


    @step
    def wait_until_actor_is_unfollowed_by_actor(self):
        self.leader_node.wait_until_actor_is_unfollowed_by_actor(self.leader_actor_uri, self.follower_actor_uri)


    @step
    def wait_until_actor_is_unfollowing_actor(self):
        self.follower_node.wait_until_actor_is_unfollowing_actor(self.follower_actor_uri, self.leader_actor_uri)


    @step
    def leader_creates_note_after_unfollow(self):
        self.leader_note_after_unfollow_uri = self.leader_node.make_create_note(self.leader_actor_uri, f"Testing leader_creates_note_after_unfollow {datetime.now()}")
        assert self.leader_note_after_unfollow_uri


    @step
    def wait_until_timeoutd(self):
        try :
            self.follower_node.wait_until_actor_has_received_note(self.follower_actor_uri, self.leader_note_after_unfollow_uri, max_wait=5)
            raise AssertionFailure(SpecLevel.IMPLIED, InteropLevel.PROBLEM, "Received Note from leader after unfollowing")
        except TimeoutException as e:
            pass # Correct
