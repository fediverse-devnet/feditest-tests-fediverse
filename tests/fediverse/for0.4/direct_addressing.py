# https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/147
#
# Basically the same as https://github.com/fediverse-devnet/feditest/blob/develop/tests.unit/feditest/node_with_mastodon_api.py but with two nodes



"""
Tests that a note by actor A is delivered to an actor B on a different Fediverse Node if
* B does not follow A
* but A addresses the note to B
"""

from datetime import datetime

from feditest import AssertionFailure, InteropLevel, SpecLevel, step, test
from feditest.protocols import TimeoutException
from feditest.protocols.fediverse import FediverseNode

@test
class SendNoteToTest:
    def __init__(self,
        sender_node: FediverseNode,
        receiver_node: FediverseNode
    ) -> None:
        self.sender_node = sender_node
        self.sender_actor_uri = None

        self.receiver_node = receiver_node
        self.receiver_actor_uri = None

        self.sender_note_uri = None


    @step
    def provision_actors(self):
        self.sender_actor_uri = self.sender_node.obtain_actor_document_uri()
        assert self.sender_actor_uri

        self.receiver_actor_uri = self.receiver_node.obtain_actor_document_uri()
        assert self.receiver_actor_uri


    @step
    def sender_creates_note(self):
        self.sender_note_uri = self.sender_node.make_create_note(
            self.sender_actor_uri,
            f"Testing sender_creates_note {datetime.now()}",
            deliver_to=[ self.receiver_actor_uri ])
        assert self.sender_note_uri


    @step
    def wait_until_note_received(self):
        self.receiver_node.wait_until_actor_has_received_note(self.receiver_actor_uri, self.sender_note_uri)
