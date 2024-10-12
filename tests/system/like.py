# https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/149
#
# Two nodes
# A creates Notes X
# B access Note X
# B Likes X
# A receives the like
# B undoes the Like
# On A the post is not Liked any more


"""
Tests that a note by actor A can be Liked by an actor B on a different Fediverse Node
and both see the Like.
"""

from datetime import datetime

from feditest import step, test
from feditest.protocols.fediverse import FediverseNode

@test
class LikeTest:
    def __init__(self,
        leader_node: FediverseNode,
        follower_node: FediverseNode
    ) -> None:
        self.leader_node = leader_node
        self.leader_actor_uri = None

        self.follower_node = follower_node
        self.follower_actor_uri = None

        self.leader_note_uri = None
        self.follower_note_uri = None


    @step
    def provision_actors(self):
        self.leader_actor_uri = self.sender_node.obtain_actor_document_uri()
        assert self.leader_actor_uri

        self.follower_actor_uri = self.receiver_node.obtain_actor_document_uri()
        assert self.follower_actor_uri


    @step
    def leader_creates_note(self):
        self.leader_note_uri = self.leader_node.make_create_note(self.leader_actor_uri, f"Testing leader_creates_note {datetime.now()}")
        assert self.leader_note_uri


    @step
    def follower_accesses_note(self):
        self.follower_note_uri = self.follower_node.access_note(self.follower_actor_uri, self.leader_note_uri)


    @step
    def follower_likes_note(self):
        self.follower_node.like_note(self.follower_actor_uri, self.follower_note_uri)


    @step
    def wait_until_note_received(self):
        self.leader_node.wait_until_actor_has_received_note(self.leader_actor_uri, self.follower_note_uri)
