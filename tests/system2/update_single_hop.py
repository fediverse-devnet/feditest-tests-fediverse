# https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/151
#
# Two nodes
# A creates Note X
# B accesses Note X
# A updates X -> X'
# B accesses its local copy. It is now X'

from datetime import datetime

from hamcrest import contains_string, equal_to

from feditest import assert_that, poll_until, step, test, InteropLevel, SpecLevel
from feditest.protocols.fediverse import FediverseNode
from feditest.reporting import info


@test
class UpdateTest:
    def __init__(self,
        sender_node: FediverseNode,
        receiver_node: FediverseNode
    ) -> None:
        self.sender_node = sender_node
        self.sender_actor_acct_uri = None

        self.receiver_node = receiver_node
        self.receiver_actor_acct_uri = None

        self.note_content1 =  f"Note with original content"
        self.note_content2 =  f"Note with updated content"
        self.note_uri = None
        self.note_received_content1 = None
        self.note_received_content2 = None


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
        self.note_uri = self.sender_node.make_create_note(
            self.sender_actor_acct_uri,
            self.note_content1,
            deliver_to=[ self.receiver_actor_acct_uri ])
        assert self.note_uri
        info(f'Note: { self.note_uri }')


    @step
    def wait_until_note_received(self):
        self.note_received_content1 = poll_until(lambda: self.receiver_node.actor_has_received_object(self.receiver_actor_acct_uri, self.note_uri))
        info(f'Received original content: "{ self.note_received_content1 }"')

        # We do not check that the note is unmodified, only that the content is somewhere in the note
        assert_that(self.note_received_content1, contains_string(self.note_content1), spec_level=SpecLevel.MUST, interop_level=InteropLevel.PROBLEM)


    @step
    def sender_updates_note(self):
        self.sender_node.update_note(self.sender_actor_acct_uri, self.note_uri, self.note_content2)


    def _different_now(self):
        current_content = self.receiver_node.access_note(self.receiver_actor_acct_uri, self.note_uri)
        if current_content != self.note_received_content1:
            return current_content
        return None

    @step
    def wait_until_note_updated(self):
        self.note_received_content2 = poll_until(lambda: self._different_now())
        info(f'Received updated content: "{ self.note_received_content2 }"')

        # We do not check that the note is unmodified, only that the content is somewhere in the note
        assert_that(self.note_received_content2, contains_string(self.note_content2), spec_level=SpecLevel.MUST, interop_level=InteropLevel.PROBLEM)
