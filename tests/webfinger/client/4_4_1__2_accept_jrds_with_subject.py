import json
from hamcrest import assert_that

from feditest import step
from feditest.protocols.web.traffic import ParsedUri
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import WebFingerQueryResponse

@step
def accept_jrds_with_subject(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:

    test_id = server.obtain_existing_account_identifier()
    webfinger_uri : ParsedUri = client.construct_webfinger_uri_for(test_id)

    normal_response : WebFingerQueryResponse = client.perform_webfinger_query(test_id)

    if 'subject' not in normal_response.jrd.subject():
        json_with_subject = json.loads(normal_response.jrd.as_json_string())
        json_with_subject['subject'] = 'acct:foo@example.com'

        with_subject_response = server.override_webfinger_response(
            lambda:
                client.perform_webfinger_query(test_id),
            {
                test_id : json.dumps(json_with_subject)
            }
        )
        assert_that(with_subject_response.jrd.validate())