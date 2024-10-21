"""
Tests that an HTML blockquote in the content of a post is preserved.

From https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/9

NOTE: This does not work through the Mastodon API. It mangles the HTML content
to this:

<p>&lt;p&gt;A famous person once didn not say:&lt;/p&gt;<br>&lt;blockquote&gt;You must be the blockquote that you wish to see in the world.&lt;/blockquote&gt;<br>&lt;p&gt;Oh, well&lt;/p&gt;<br> <span class="h-card" translate="no"><a href="https://mastodon-2.86936.lan/@feditestadmin" class="u-url mention" rel="nofollow noopener noreferrer" target="_blank">@<span>feditestadmin@mastodon-2.86936.lan</span></a></span></p>

"""

from datetime import datetime

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

        self.note_first_line = 'A famous person once didn not say:'
        self.note_quoted_content = 'You must be the blockquote that you wish to see in the world.'
        self.note_last_line = 'Oh, well'
        self.note_content = f'''
<p>{ self.note_first_line }</p>
<blockquote>{ self.note_quoted_content }</blockquote>
<p>{ self.note_last_line }</p>
'''
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

        # all three lines are still there
        assert_that(received_content, contains_string(self.note_first_line), spec_level=SpecLevel.MUST, interop_level=InteropLevel.PROBLEM)
        assert_that(received_content, contains_string(self.note_quoted_content), spec_level=SpecLevel.MUST, interop_level=InteropLevel.PROBLEM)
        assert_that(received_content, contains_string(self.note_last_line), spec_level=SpecLevel.MUST, interop_level=InteropLevel.PROBLEM)

        # the blockquote tag is opened and closed in the right relative positions
        first_line_index = received_content.index(self.note_first_line)
        blockquote_open_index = received_content.lower().index('<blockquote>')
        quote_index = received_content.index(self.note_quoted_content)
        blockquote_close_index = received_content.lower().index('</blockquote>')
        last_line_index = received_content.index(self.note_last_line)

        assert_that(first_line_index, less_than(blockquote_open_index), spec_level=SpecLevel.IMPLIED, interop_level=InteropLevel.DEGRADED)
        assert_that(blockquote_open_index, less_than(quote_index), spec_level=SpecLevel.IMPLIED, interop_level=InteropLevel.DEGRADED)
        assert_that(quote_index, less_than(blockquote_close_index), spec_level=SpecLevel.IMPLIED, interop_level=InteropLevel.DEGRADED)
        assert_that(blockquote_close_index, less_than(last_line_index), spec_level=SpecLevel.IMPLIED, interop_level=InteropLevel.DEGRADED)

        assert_that(received_content, equal_to(self.note_content), spec_level=SpecLevel.IMPLIED, interop_level=InteropLevel.DEGRADED)
