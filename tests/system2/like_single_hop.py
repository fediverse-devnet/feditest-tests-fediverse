from datetime import datetime

from feditest import poll_until, step, test
from feditest.protocols.fediverse import FediverseNode
from feditest.reporting import info

@test
class LikeTest:
    """
    Tests that actor B can like a note by actor A on a different Fediverse Node
    and both see the Like. Unlike works the reverse.

    https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/149
    """
    def __init__(self,
        sender_node: FediverseNode,
        receiver_node: FediverseNode
    ) -> None:
        self.sender_node = sender_node
        self.sender_actor_acct_uri = None

        self.receiver_node = receiver_node
        self.receiver_actor_acct_uri = None

        self.note_uri = None


    @step
    def provision_actors(self):
        self.sender_actor_acct_uri = self.sender_node.obtain_actor_acct_uri()
        assert self.sender_actor_acct_uri
        info(f'Sender actor: { self.sender_actor_acct_uri }')

        self.receiver_actor_acct_uri = self.receiver_node.obtain_actor_acct_uri()
        assert self.receiver_actor_acct_uri
        info(f'Receiver actor: { self.receiver_actor_acct_uri }')


    @step
    def sender_creates_note(self):
        self.note_uri = self.sender_node.make_create_note(self.sender_actor_acct_uri, f"Testing sender_creates_note {datetime.now()}")
        assert self.note_uri
        info(f'Note: { self.note_uri }')


    @step
    def receiver_likes_note(self):
        # This is the equivalent of the receiver entering the URL of the note into the search box, until it comes up on their local server,
        # and then likes it (no following involved)
        self.receiver_node.like_object(self.receiver_actor_acct_uri, self.note_uri)


    @step
    def wait_until_like_received(self):
        poll_until(lambda: self.receiver_actor_acct_uri in self.sender_node.object_likers(self.sender_actor_acct_uri, self.note_uri))


    @step
    def receiver_unlikes_note(self):
        self.receiver_node.unlike_object(self.receiver_actor_acct_uri, self.note_uri)


    @step
    def wait_until_unlike_received(self):
        poll_until(lambda: self.receiver_actor_acct_uri not in self.sender_node.object_likers(self.sender_actor_acct_uri, self.note_uri))

