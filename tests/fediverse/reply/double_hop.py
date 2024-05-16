from feditest import step, test, HardAssertionFailure
from feditest.protocols.fediverse import FediverseNode


@test
class ReplyDoubleHopTest:
    """
    Test that replies on a boosted post make it to the booster and the poster.
    """
    def __init__(self,
        leader_node:   FediverseNode,
        middle_node:   FediverseNode,
        follower_node: FediverseNode
    ) -> None:
       self.leader_node = leader_node
       self.middle_node = middle_node
       self.follower_node = follower_node

       self.post_content = "Nothing much happening."
       self.reply_content = "Join us here, we are having fun!"


    @step
    def get_actors(self):
        self.leader_actor_uri   = self.leader_node.obtain_actor_document_uri()
        self.middle_actor_uri   = self.middle_node.obtain_actor_document_uri()
        self.follower_actor_uri = self.follower_node.obtain_actor_document_uri()


    @step
    def setup_follow(self):
        self.middle_node.make_a_follow_b(self.middle_actor_uri, self.leader_actor_uri, self.leader_node)
        self.follower_node.make_a_follow_b(self.follower_actor_uri, self.middle_actor_uri, self.middle_node)


    @step
    def leader_creates_note(self):
        self.post_uri_on_leader_node = self.leader_node.make_create_note(self.leader_actor_uri, self.post_content)


    @step
    def note_in_middle_inbox(self):
        try:
            self.post_uri_on_middle_node = self.middle_node.wait_for_object_in_inbox(self.middle_actor_uri, self.post_uri_on_leader_node)
            # FIXME check for the right content

        except TimeoutError as e:
            raise HardAssertionFailure(e)


    @step
    def middle_creates_announce(self):
        self.announce_uri_on_middle_node = self.middle_node.make_announce_object(self.middle_actor_uri, self.post_uri_on_middle_node)


    @step
    def announce_in_follower_inbox(self):
        try:
            self.announce_uri_on_follower_node = self.middle_node.wait_for_object_in_inbox(self.announce_uri_on_middle_node)
            # FIXME check for the right content

        except TimeoutError as e:
            raise HardAssertionFailure(e)


    @step
    def follower_creates_reply(self):
        self.reply_uri_on_follower_node = self.follower_node.make_reply(self.follower_actor_uri, self.reply_content)


    @step
    def middle_received_reply(self):
        self.middle_node.wait_for_object_in_inbox(self.reply_uri_on_follower_node)


    @step
    def leader_received_reply(self):
        self.leader_node.wait_for_object_in_inbox(self.reply_uri_on_follower_node)
