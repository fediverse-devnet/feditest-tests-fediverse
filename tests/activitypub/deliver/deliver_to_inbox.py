from datetime import datetime

from feditest import AssertionFailure, InteropLevel, SpecLevel, step, test
from feditest.protocols.fediverse import FediverseNode


@test
class DeliverToInboxTest:
    """
    Deliver a Create of a Note to a user's inbox. Check that it returns HTTP 200 or 202, and
    that it's visible to the user when they search for it by the Note's id.
    https://www.w3.org/TR/activitypub/#delivery

    No "follow" relationship is needed
    """
    def __init__(self,
        sender_node: FediverseNode,
        receiver_node: FediverseNode
    ) -> None:
       self.sender_node = sender_node
       self.receiver_node = receiver_node

       self.post_content = f'Good morning at { datetime.now() }!'
       self.leader_note_uri = None


    @step
    def get_actors(self):
        self.sender_actor_uri = self.sender_node.obtain_actor_document_uri('sender-nofollow')
        assert self.sender_actor_uri

        self.receiver_actor_uri = self.receiver_node.obtain_actor_document_uri('receiver-nofollow')
        assert self.receiver_actor_uri


    @step
    def create_note(self):
        self.leader_note_uri = self.create_note_uri_on_sender_node = self.sender_node.make_create_note(
            self.sender_actor_uri,
            self.post_content,
            [ self.receiver_actor_uri ] )
        assert self.leader_note_uri


    @step
    def test_note_received(self):
        try:
            received_content = self.create_note_uri_on_receiver_node = self.receiver_node.wait_until_actor_has_received_note(self.receiver_actor_uri, self.leader_note_uri)
            # <p>Good morning! <span class="h-card" translate="no"><a href="https://mastodon-1.1234.lan/@feditestadmin" class="u-url mention" rel="nofollow noopener noreferrer" target="_blank">@<span>feditestadmin@mastodon-1.1234.lan</span></a></span></p>

        except TimeoutError as e:
            raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, e)

        if self.post_content not in received_content:
            raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, f'Received message does not contain payload: "{ received_content }".')

        if self.post_content != received_content:
            raise AssertionFailure(SpecLevel.IMPLIED, InteropLevel.DEGRADED, f'Received message modified from original: "{ received_content }".')
