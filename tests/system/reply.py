"""
Tests that a note by actor A can be Replied by an actor B on a different Fediverse Node
and both see the Reply.
"""

from datetime import datetime

from feditest import AssertionFailure, InteropLevel, SpecLevel, assert_that, step, test
from feditest.protocols.fediverse import FediverseNode

@test
class ReplyTest:
    def __init__(self,
        leader_node: FediverseNode,
        follower_node: FediverseNode
    ) -> None:
        self.leader_node = leader_node
        self.leader_actor_uri = None

        self.follower_node = follower_node
        self.follower_actor_uri = None

        self.leader_note_uri = None
        self.follower_reply_uri = None
        self.reply_content = f'Testing follower_replies_to_note {datetime.now()}'


    @step
    def provision_actors(self):
        self.leader_actor_uri = self.leader_node.obtain_actor_document_uri()
        assert self.leader_actor_uri

        self.follower_actor_uri = self.follower_node.obtain_actor_document_uri()
        assert self.follower_actor_uri


    @step
    def leader_creates_note(self):
        self.leader_note_uri = self.leader_node.make_create_note(self.leader_actor_uri, f"Testing leader_creates_note {datetime.now()}")
        assert self.leader_note_uri # We expect that this works: tests the leader_node Node implementation


    @step
    def follower_replies_to_note(self):
        # This may throw an exception if the follower_node could not find the leader_note
        self.follower_reply_uri = self.follower_node.make_reply_note(self.follower_actor_uri, self.leader_note_uri, self.reply_content)
        assert self.follower_reply_uri # We expect that this works: tests the follower_node Node implementation


    @step
    def wait_until_reply_received_by_follower(self):
        received_content = self.follower_node.wait_until_actor_has_received_note(self.follower_actor_uri, self.follower_reply_uri)
        assert self.reply_content in received_content # We expect that this works: tests the follower_node Node implementation


    @step
    def wait_until_reply_received_by_leader(self):
        try:
            received_content = self.leader_node.wait_until_actor_has_received_note(self.leader_actor_uri, self.follower_reply_uri)

        except TimeoutError as e:
            raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, e)

        if self.reply_content not in received_content:
            raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, f'Received reply does not contain payload: "{ received_content }".')

        if self.reply_content != received_content:
            raise AssertionFailure(SpecLevel.IMPLIED, InteropLevel.DEGRADED, f'Received reply modified from original: "{ received_content }".')
