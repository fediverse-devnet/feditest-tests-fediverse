from feditest import test
from feditest.protocols.fediverse import FediverseNode


@test
def follow(
        to_be_leader_node:   FediverseNode,
        to_be_follower_node: FediverseNode
) -> None:
    """
    Have an account on one node follow another account on another node.
    Make sure the follower or following collections are correct on both
    sides.
    """

    leader_actor_uri   = to_be_leader_node.obtain_actor_document_uri()
    follower_actor_uri = to_be_follower_node.obtain_actor_document_uri()

    # We only work with identifiers because that way, there is no requirement that a node actually makes
    # data available to the test itself
    leader_actor_followers_collection_uri = to_be_leader_node.obtain_followers_collection_uri(leader_actor_uri)
    leader_actor_following_collection_uri = to_be_leader_node.obtain_following_collection_uri(leader_actor_uri)
    follower_actor_followers_collection_uri = to_be_follower_node.obtain_followers_collection_uri(follower_actor_uri)
    follower_actor_following_collection_uri = to_be_follower_node.obtain_following_collection_uri(follower_actor_uri)

    # So far, the two actors are unrelated on both nodes
    to_be_leader_node.assert_not_member_of_collection_at(follower_actor_uri, leader_actor_followers_collection_uri)
    to_be_leader_node.assert_not_member_of_collection_at(follower_actor_uri, leader_actor_following_collection_uri)
    to_be_follower_node.assert_not_member_of_collection_at(leader_actor_uri, follower_actor_followers_collection_uri)
    to_be_follower_node.assert_not_member_of_collection_at(leader_actor_uri, follower_actor_following_collection_uri)

    # Now relate them
    to_be_follower_node.make_a_follow_b(follower_actor_uri, leader_actor_uri, to_be_leader_node)

    # The follow relationship has been established on both sides
    to_be_leader_node.assert_member_of_collection_at(follower_actor_uri, leader_actor_followers_collection_uri)
    to_be_leader_node.assert_not_member_of_collection_at(follower_actor_uri, leader_actor_following_collection_uri)
    to_be_follower_node.assert_not_member_of_collection_at(leader_actor_uri, follower_actor_followers_collection_uri)
    to_be_follower_node.assert_member_of_collection_at(leader_actor_uri, follower_actor_following_collection_uri)
