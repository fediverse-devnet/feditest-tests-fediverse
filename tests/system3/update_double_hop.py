import time

from feditest import poll_but_not, poll_until, step, test
from feditest.protocols.fediverse import FediverseNode
from feditest.reporting import info


@test
class UpdateDoubleHopTest:
    """
    Test double-hop update.
    """
    def __init__(self,
        node1: FediverseNode,
        node2: FediverseNode,
        node3: FediverseNode
    ) -> None:
        self.node1 = node1
        self.node1_actor_acct_uri = None

        self.node2 = node2
        self.node2_actor_acct_uri = None

        self.node3 = node3
        self.node3_actor_acct_uri = None

        self.note_uri = None
        self.original_content = "The original note"
        self.updated_content = "The note, now all new and improved"


    @step
    def provision_actors(self):
        self.node1_actor_acct_uri = self.node1.obtain_actor_acct_uri()
        assert self.node1_actor_acct_uri
        info(f'Node1 actor: { self.node1_actor_acct_uri }')

        self.node1.set_auto_accept_follow(self.node1_actor_acct_uri, True)

        self.node2_actor_acct_uri = self.node2.obtain_actor_acct_uri()
        assert self.node2_actor_acct_uri
        info(f'Node2 actor: { self.node2_actor_acct_uri }')

        self.node2.set_auto_accept_follow(self.node2_actor_acct_uri, True)

        self.node3_actor_acct_uri = self.node3.obtain_actor_acct_uri()
        assert self.node3_actor_acct_uri
        info(f'Node3 actor: { self.node3_actor_acct_uri }')


    @step
    def follow(self):
        self.node2.make_follow(self.node2_actor_acct_uri, self.node1_actor_acct_uri)
        self.node3.make_follow(self.node3_actor_acct_uri, self.node2_actor_acct_uri)


    @step
    def wait_until_actors_are_followed(self):
        time.sleep(1) # Sometimes there seems to be a race condition in Mastodon, or something like that.
                      # If we proceed too quickly, the API returns 422 "User already exists" or such
                      # in response to a search, which makes no sense.
                      # This is a Mastodon-specific workaround, but does not hurt anybody else
                      # See https://github.com/mastodon/mastodon/issues/32501

        poll_until(lambda: self.node1.actor_is_followed_by_actor(self.node1_actor_acct_uri, self.node2_actor_acct_uri))
        poll_until(lambda: self.node2.actor_is_followed_by_actor(self.node2_actor_acct_uri, self.node3_actor_acct_uri))


    @step
    def wait_until_actors_are_following(self):
        poll_until(lambda: self.node2.actor_is_following_actor(self.node2_actor_acct_uri, self.node1_actor_acct_uri))
        poll_until(lambda: self.node3.actor_is_following_actor(self.node3_actor_acct_uri, self.node2_actor_acct_uri))


    @step
    def sender_creates_note(self):
        self.note_uri = self.node1.make_create_note(self.node1_actor_acct_uri, self.original_content)
        assert self.note_uri
        info(f'Note URI: { self.note_uri }')


    @step
    def wait_until_note_received(self):
        poll_until(lambda: self.node2.actor_has_received_object(self.node2_actor_acct_uri, self.note_uri))


    @step
    def update_note(self):
        self.node1.update_note(self.node1_actor_acct_uri, self.note_uri, self.updated_content)


    @step
    def wait_until_update_received(self):
        poll_until(lambda: self.updated_content in self.node2.note_content(self.node2_actor_acct_uri, self.note_uri))
        poll_until(lambda: self.updated_content in self.node3.note_content(self.node3_actor_acct_uri, self.note_uri))
