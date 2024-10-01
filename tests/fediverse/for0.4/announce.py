"""
Tests that a note by actor A can be announced by an actor B on a different Fediverse Node
and the announce is seen by actor C that is following B.

To not complicate constellation setup and stay with two Nodes, we have actors A and C on the same Node.
"""

from datetime import datetime

from feditest import AssertionFailure, InteropLevel, SpecLevel, assert_that, step, test
from feditest.protocols.fediverse import FediverseNode

@test
class AnnounceTest:
    def __init__(self,
        node1: FediverseNode,
        node2: FediverseNode
    ) -> None:
        self.node1 = node1
        self.node1_poster_actor_uri = None
        self.node1_follower_actor_uri = None

        self.node2 = node2
        self.node2_announcer_actor_uri = None

        self.note_uri = None
        self.note_content = f'Testing announce {datetime.now()}'


    @step
    def provision_actors(self):
        self.node1_poster_actor_uri = self.node1.obtain_actor_document_uri('poster')
        assert self.node1_poster_actor_uri
        print( f'XXX poster: { self.node1_poster_actor_uri }')

        self.node2_announcer_actor_uri = self.node2.obtain_actor_document_uri('announcer')
        assert self.node2_announcer_actor_uri
        print( f'XXX announcer: { self.node2_announcer_actor_uri }')

        self.node1_follower_actor_uri = self.node1.obtain_actor_document_uri('follower')
        assert self.node1_follower_actor_uri
        print( f'XXX follower: { self.node1_follower_actor_uri }')


    @step
    def follow(self):
        self.node1.make_follow(self.node1_follower_actor_uri, self.node2_announcer_actor_uri)
        self.node2.wait_until_actor_is_followed_by_actor(self.node2_announcer_actor_uri, self.node1_follower_actor_uri)
        self.node1.wait_until_actor_is_following_actor(self.node1_follower_actor_uri, self.node2_announcer_actor_uri)


    @step
    def poster_creates_note(self):
        self.note_uri = self.node1.make_create_note(self.node1_poster_actor_uri, self.note_content)
        assert self.note_uri # We expect that this works: tests the node1 Node implementation


    @step
    def booster_boosts(self):
        # This may throw an exception if node2 could not find the note
        self.node2.make_announce(self.node2_announcer_actor_uri, self.note_uri)


    @step
    def wait_until_boost_received_by_follower(self):
        try:
            received_content = self.node1.wait_until_actor_has_received_note(self.node1_follower_actor_uri, self.note_uri)

        except TimeoutError as e:
            raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, e)

        if self.note_content not in received_content:
            raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, f'Received anounce does not contain payload: "{ received_content }".')

        if self.note_content != received_content:
            raise AssertionFailure(SpecLevel.IMPLIED, InteropLevel.DEGRADED, f'Received announce modified from original: "{ received_content }".')
