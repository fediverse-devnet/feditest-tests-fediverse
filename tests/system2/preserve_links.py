"""
Make sure that all hyperlinks in a note are still present on the receiving node. They may be rearranged (details tbd)

FIXME
"""

from hamcrest import contains_string, equal_to, less_than

from feditest import assert_that, poll_until, step, test, InteropLevel, SpecLevel
from feditest.protocols.fediverse import FediverseNode
from feditest.reporting import info


@test
class PreserveBlockquoteTest:
    def __init__(self,
        sender_node: FediverseNode,
        receiver_node: FediverseNode
    ) -> None:
        self.sender_node = sender_node
        self.sender_actor_acct_uri = None

        self.receiver_node = receiver_node
        self.receiver_actor_acct_uri = None

        self.urls_in_note = [
            'https://feditest.org/',
            'https://www.w3.org/TR/activitypub/'
        ]
        self.note_first_line = 'Here are some links: '
        self.note_content = self.note_first_line + ' '.join(self.urls_in_note)
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
        self.note_uri = self.sender_node.make_create_note(
            self.sender_actor_acct_uri,
            self.note_content,
            deliver_to=[ self.receiver_actor_acct_uri ])
        assert self.note_uri
        info(f'Note: { self.note_uri }')


    @step
    def wait_until_note_received(self):
        received_content = poll_until(lambda: self.receiver_node.actor_has_received_object(self.receiver_actor_acct_uri, self.note_uri))
        info(f'Received content: "{ received_content }"')

        for url in self.urls_in_note:
            assert_that(received_content, contains_string(url), spec_level=SpecLevel.MUST, interop_level=InteropLevel.PROBLEM)
