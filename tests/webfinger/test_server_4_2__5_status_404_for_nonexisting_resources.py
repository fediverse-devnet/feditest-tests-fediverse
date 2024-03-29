"""
See annotated WebFinger specification, test 4.2/5
"""

from hamcrest import assert_that, equal_to

from feditest import step
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer

@step
def status_404_for_nonexisting_resources(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_id = server.obtain_non_existing_account_identifier();

    try:
        test_result = client.perform_webfinger_query_for(test_id)

        assert_that(False, 'No exception when performing WebFinger query on non-existing resource')

    except WebFingerClient.UnknownResourceException as e:
        assert_that(e.http_response.status_code, equal_to(404))
