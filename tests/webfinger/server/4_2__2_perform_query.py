from hamcrest import none, not_none

from feditest import hard_assert_that, test
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.utils import wf_error

@test
def normal_query(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    Perform a normal, simple query on an existing account.
    """
    test_id = server.obtain_account_identifier()

    webfinger_response = client.perform_webfinger_query(test_id)

    hard_assert_that(
            webfinger_response.exc,
            none(),
            wf_error(webfinger_response))

    hard_assert_that(
            webfinger_response.jrd,
            not_none(),
            wf_error(webfinger_response))

    try:
        webfinger_response.jrd.validate()

    except Exception as e:
        hard_assert_that(False, wf_error(webfinger_response))
