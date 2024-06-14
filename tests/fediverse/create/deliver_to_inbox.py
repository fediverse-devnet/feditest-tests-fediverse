from feditest import AssertionFailure, InteropLevel, SpecLevel, step, test
from feditest.protocols.fediverse import FediverseNode


@test
class DeliverToInboxTest:
    """
    Deliver a Create of a Note to a user's inbox. Check that it returns HTTP 200 or 202, and that it's visible to the user when they search for it by the Note's id. https://www.w3.org/TR/activitypub/#delivery

    No "follow" relationship is needed
    """
    def __init__(self,
        sender_node: FediverseNode,
        receiver_node: FediverseNode
    ) -> None:
       self.sender_node = sender_node
       self.receiver_node = receiver_node

       self.post_content = "Good morning!"


    @step
    def get_actors(self):
        self.sender_actor_uri   = self.sender_node.obtain_actor_document_uri()
        self.receiver_actor_uri = self.receiver_node.obtain_actor_document_uri()


    @step
    def create_note(self):
        self.create_note_uri_on_sender_node = self.sender_node.make_create_note(self.sender_actor_uri, self.post_content, to=self.receiver_actor_uri, inbox_preference='actor')


    @step
    def test_note_received(self):
        try:
            self.create_note_uri_on_receiver_node = self.receiver_node.wait_for_object_in_inbox(self.receiver_actor_uri, self.create_note_uri_on_sender_node)
            # FIXME check for the right content

        except TimeoutError as e:
            raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, e)
