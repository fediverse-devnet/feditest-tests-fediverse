import json
from hamcrest import assert_that

from feditest import test
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import WebFingerQueryResponse

@test
def accept_jrds_without_subject(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:

    test_id = server.obtain_account_identifier()
    webfinger_uri = client.construct_webfinger_uri_for(test_id)

    normal_response : WebFingerQueryResponse = client.perform_webfinger_query(test_id)

    if 'subject' in normal_response.jrd.subject():
        json_without_subject = json.loads(normal_response.jrd.as_json_string())
        json_without_subject.pop('subject')

        without_subject_response : WebFingerQueryResponse = server.override_webfinger_response(
            lambda: client.perform_webfinger_query(test_id),
            {
                test_id : json.dumps(json_without_subject)
            }
        )
        assert_that(without_subject_response.jrd.validate())