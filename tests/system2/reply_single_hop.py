from datetime import datetime

from hamcrest import contains_string, equal_to

from feditest import AssertionFailure, InteropLevel, SpecLevel, assert_that, poll_until, step, test
from feditest.protocols.fediverse import FediverseNode
from feditest.reporting import info


@test
class ReplyTest:
    """
    Tests that actor B can reply to a note by actor A on a different Fediverse Node and both see the reply.

    https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/128
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
        self.note_content = None
        self.reply_uri = None
        self.reply_content = None

        self.content_received_by_sender = None
        self.content_received_by_receiver = None


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
        self.note_content = f'Testing sender_creates_note { datetime.now() }'
        self.note_uri = self.sender_node.make_create_note(self.sender_actor_acct_uri, self.note_content)
        assert self.note_uri
        info(f'Note: { self.note_uri }')


    @step
    def receiver_replies_to_note(self):
        # This is the equivalent of the receiver entering the URL of the note into the search box, until it comes up on their local server,
        # and then replies to it (no following involved)
        self.reply_content = f'Testing follower_replies_to_note { datetime.now() }'
        self.reply_uri = self.receiver_node.make_reply_note(self.receiver_actor_acct_uri, self.note_uri, self.reply_content)
        assert self.reply_uri
        info(f'Note: { self.reply_uri }')


    @step
    def wait_until_reply_received_by_receiver(self):
        poll_until(lambda: self.reply_uri in self.receiver_node.direct_replies_to_object(self.receiver_actor_acct_uri, self.note_uri))
        self.content_received_by_receiver = self.receiver_node.note_content(self.receiver_actor_acct_uri, self.reply_uri)


    @step
    def wait_until_reply_received_by_sender(self):
        poll_until(lambda: self.reply_uri in self.sender_node.direct_replies_to_object(self.sender_actor_acct_uri, self.note_uri))
        self.content_received_by_sender = self.sender_node.note_content(self.sender_actor_acct_uri, self.reply_uri)

        assert_that(self.content_received_by_receiver, equal_to(self.content_received_by_sender), spec_level=SpecLevel.IMPLIED, interop_level=InteropLevel.DEGRADED)

        assert_that(self.content_received_by_receiver, contains_string(self.reply_content), spec_level=SpecLevel.MUST, interop_level=InteropLevel.PROBLEM)
        assert_that(self.content_received_by_receiver, equal_to(self.reply_content), spec_level=SpecLevel.IMPLIED, interop_level=InteropLevel.DEGRADED)

