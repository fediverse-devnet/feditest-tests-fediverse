"""
"""

from hamcrest import assert_that, is_not, has_item
from feditest import step
from feditest.protocols.fediverse import FediverseNode

@step
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

    # FIXME
    # leader_actor_existing = to_be_leader_node.instantiate_actor_from_actor_uri(leader_actor_uri)
    # assert_that(leader_actor_existing.followers, is_not(has_item(follower_actor_uri)))

    # follower_actor_existing = to_be_follower_node.instantiate_actor_from_actor_uri(follower_actor_uri)
    # assert_that(follower_actor_existing.following, is_not(has_item(leader_actor_uri)))

    to_be_follower_node.make_a_follow_b(follower_actor_uri, leader_actor_uri, to_be_leader_node)

    # leader_actor_new = to_be_leader_node.instantiate_actor_from_actor_uri(leader_actor_uri)
    # assert_that(leader_actor_new.followers, has_item(follower_actor_uri)))

    # follower_actor_new = to_be_follower_node.instantiate_actor_from_actor_uri(follower_actor_uri)
    # assert_that(follower_actor_new.following, has_item(leader_actor_uri))
