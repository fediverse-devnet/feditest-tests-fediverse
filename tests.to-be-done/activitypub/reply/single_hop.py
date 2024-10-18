from feditest import assert_that, poll_until, step, test
from feditest.protocols.fediverse import FediverseNode


@test
class ReplyTest:
    """
    Test that replies on a post.
    """
    def __init__(self,
        leader_node:   FediverseNode,
        follower_node: FediverseNode
    ) -> None:
       self.leader_node = leader_node
       self.follower_node = follower_node

       self.post_content = "Nothing much happening."
       self.reply_content = "Join us here, we are having fun!"


    @step
    def get_actors(self):
        self.leader_actor_uri   = self.leader_node.obtain_actor_document_uri()
        self.follower_actor_uri = self.follower_node.obtain_actor_document_uri()


    @step
    def setup_follow(self):
        self.follower_node_node.make_a_follow_b(self.follower_actor_uri, self.leader_actor_uri, self.leader_node)


    @step
    def leader_creates_note(self):
        self.post_uri_on_leader_node = self.leader_node.make_create_note(self.leader_actor_uri, self.post_content)


    @step
    def note_in_follower_inbox(self):
        self.post_uri_on_follower_node = self.follower_node.wait_for_object_in_inbox(self.follower_actor_uri, self.post_uri_on_leader_node)
        # FIXME check for the right content


    @step
    def follower_creates_reply(self):
        self.reply_uri_on_follower_node = self.follower_node.make_reply(self.follower_actor_uri, self.reply_content)


    @step
    def reply_isreply_on_follower_node(self):
        # FIXME: decide on SpecLevel, InteropLevel for these assertions
        assert_that(self.follower_node.is_reply_to( self.reply_uri_on_follower_node, self.post_uri_on_follower_node))
        # FIXME check for the right content


    @step
    def leader_received_reply(self):
        self.leader_node.wait_for_object_in_inbox(self.reply_uri_on_follower_node)
        # FIXME check for the right content
