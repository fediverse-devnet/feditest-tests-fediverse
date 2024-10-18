"""
Test single-hop delete

See also: https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/3
"""

from datetime import datetime
import time

from feditest import poll_but_not, poll_until, step, test
from feditest.protocols.fediverse import FediverseNode
from feditest.reporting import info


@test
class DeleteSingleHopTest:
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

        self.sender_node.set_auto_accept_follow(self.sender_actor_acct_uri, True)

        self.receiver_actor_acct_uri = self.receiver_node.obtain_actor_acct_uri()
        assert self.receiver_actor_acct_uri
        info(f'Receiver actor: { self.receiver_actor_acct_uri }')


    @step
    def follow(self):
        self.receiver_node.make_follow(self.receiver_actor_acct_uri, self.sender_actor_acct_uri)


    @step
    def wait_until_actor_is_followed_by_actor(self):
        time.sleep(1) # Sometimes there seems to be a race condition in Mastodon, or something like that.
                      # If we proceed too quickly, the API returns 422 "User already exists" or such
                      # in response to a search, which makes no sense.
                      # This is a Mastodon-specific workaround, but does not hurt anybody else
                      # See https://github.com/mastodon/mastodon/issues/32501

        poll_until(lambda: self.sender_node.actor_is_followed_by_actor(self.sender_actor_acct_uri, self.receiver_actor_acct_uri))


    @step
    def wait_until_actor_is_following_actor(self):
        poll_until(lambda: self.receiver_node.actor_is_following_actor(self.receiver_actor_acct_uri, self.sender_actor_acct_uri))


    @step
    def sender_creates_note(self):
        self.note_uri = self.sender_node.make_create_note(self.sender_actor_acct_uri, f"testing sender_creates_note {datetime.now()}")
        assert self.note_uri
        info(f'Note URI: { self.note_uri }')


    @step
    def wait_until_note_received(self):
        poll_until(lambda: self.receiver_node.actor_has_received_object(self.receiver_actor_acct_uri, self.note_uri))


    @step
    def delete_note(self):
        self.sender_node.delete_object(self.sender_actor_acct_uri, self.note_uri)


    @step
    def wait_until_note_disappeared(self):
        poll_until(lambda: not self.receiver_node.actor_has_received_object(self.receiver_actor_acct_uri, self.note_uri))

