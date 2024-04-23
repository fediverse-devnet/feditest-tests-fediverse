import json
from hamcrest import assert_that

from feditest import step
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import WebFingerQueryResponse

@step
def accept_example_response(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:

    test_id = server.obtain_account_identifier()
    overridden_jrd_json = {
       "subject" : "acct:bob@example.com",
       "aliases" :
       [
         "https://www.example.com/~bob/"
       ],
       "properties" :
       {
           "http://example.com/ns/role" : "employee"
       },
       "links" :
       [
         {
           "rel" : "http://webfinger.example/rel/profile-page",
           "href" : "https://www.example.com/~bob/"
         },
         {
           "rel" : "http://webfinger.example/rel/businesscard",
           "href" : "https://www.example.com/~bob/bob.vcf"
         }
       ]
     }
    overridden_jrd_json_string = json.dumps(overridden_jrd_json)

    webfinger_response : WebFingerQueryResponse = server.override_webfinger_response(
            lambda:
                client.perform_webfinger_query(test_id),
            {
                test_id : overridden_jrd_json_string
            }
    )
    assert_that(webfinger_response.jrd.validate())
