from feditest.protocols.fediverse import FediverseNode

class AbstractFollowTest:
    """
    Collects functionality common to "follow" tests.

    Do not mark anything as @test or @step here, otherwise the sequence of here vs subclass is unclear.
    """
    def __init__(self,
        leader_node:   FediverseNode,
        follower_node: FediverseNode
    ) -> None:
       self.leader_node = leader_node
       self.follower_node = follower_node


    def get_actors(self):
        self.leader_actor_uri   = self.leader_node.obtain_actor_document_uri()
        self.follower_actor_uri = self.follower_node.obtain_actor_document_uri()


    def get_collections(self):
        # We only work with identifiers because that way, there is no requirement that a node actually makes
        # data available to the test itself
        self.leader_actor_followers_collection_uri = self.leader_node.obtain_followers_collection_uri(self.leader_actor_uri)
        self.leader_actor_following_collection_uri = self.leader_node.obtain_following_collection_uri(self.leader_actor_uri)
        self.follower_actor_followers_collection_uri = self.follower_node.obtain_followers_collection_uri(self.follower_actor_uri)
        self.follower_actor_following_collection_uri = self.follower_node.obtain_following_collection_uri(self.follower_actor_uri)


    def test_unrelated(self):
        # FIXME: decide on SpecLevel, InteropLevel for these assertions
        self.leader_node.assert_not_member_of_collection_at(self.follower_actor_uri, self.leader_actor_followers_collection_uri)
        self.leader_node.assert_not_member_of_collection_at(self.follower_actor_uri, self.leader_actor_following_collection_uri)
        self.follower_node.assert_not_member_of_collection_at(self.leader_actor_uri, self.follower_actor_followers_collection_uri)
        self.follower_node.assert_not_member_of_collection_at(self.leader_actor_uri, self.follower_actor_following_collection_uri)


    def test_following(self):
        # FIXME: decide on SpecLevel, InteropLevel for these assertions
        self.leader_node.assert_member_of_collection_at(self.follower_actor_uri, self.leader_actor_followers_collection_uri)
        self.leader_node.assert_not_member_of_collection_at(self.follower_actor_uri, self.leader_actor_following_collection_uri)
        self.follower_node.assert_not_member_of_collection_at(self.leader_actor_uri, self.follower_actor_followers_collection_uri)
        self.follower_node.assert_member_of_collection_at(self.leader_actor_uri, self.follower_actor_following_collection_uri)