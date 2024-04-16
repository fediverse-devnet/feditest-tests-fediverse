import json
from hamcrest import assert_that, calling, is_not, raises

from feditest import step
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import WebFingerQueryResponse

def test_one(
        client: WebFingerClient,
        server: WebFingerServer,
        overridden_jrd_json : dict
) -> None:
    test_id = server.obtain_existing_account_identifier()
    overridden_jrd_json['subject'] = test_id
    overridden_jrd_json_string = json.dump(overridden_jrd_json)

    webfinger_response : WebFingerQueryResponse = server.override_webfinger_response( 
            lambda:
                client.perform_webfinger_query(test_id),
            {
                test_id : overridden_jrd_json_string
            }
    )
    assert_that(calling(webfinger_response.jrd.validate()), is_not(raises(Exception)))
    
    
@step
def must_accept_empty_document(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    All the elements are optional, so it follows that the document can be empty.
    """
    test_one(client, server, {} )


@step
def must_accept_empty_links_array(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_one(client, server, { 'links' : [] } )


@step
def must_accept_empty_aliases_array(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_one(client, server, { 'aliases' : [] } )


@step
def must_accept_long_aliases_array(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_one(client, server, { 'aliases' : [ f"alias-{i}" for i in range(0, 100) ] } )


@step
def must_accept_empty_properties_object(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_one(client, server, { 'properties' : {} } )


@step
def must_accept_long_properties_object(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    props = {}
    for i in range(0, 100):
        props[f'acct:user-{i}@host{i}.example.com'] = f'val-{i}'
        props[f'https://host{i}.example.com'] = f'val-{i}'

    test_one(client, server, { 'properties' : props } )


@step
def must_accept_long_links_array(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_one(client, server, { 'links' : [ {
        "rel" : f"https://host-{ i }.example.com/some/where"
    } for i in range(0, 100) ] } )


@step
def must_accept_long_titles_array_in_link(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    languages = (
        'af',
        'af-NA',
        'af-ZA',
        'agq',
        'agq-CM',
        'ak',
        'ak-GH',
        'am',
        'am-ET',
        'ar',
        'ar-001',
        'ar-AE',
        'ar-BH',
        'ar-DJ',
        'ar-DZ',
        'ar-EG',
        'ar-EH',
        'ar-ER',
        'ar-IL',
        'ar-IQ',
        'ar-JO',
        'ar-KM',
        'ar-KW',
        'ar-LB',
        'ar-LY',
        'ar-MA',
        'ar-MR',
        'ar-OM',
        'ar-PS',
        'ar-QA',
        'ar-SA',
        'ar-SD',
        'ar-SO',
        'ar-SS',
        'ar-SY',
        'ar-TD',
        'ar-TN',
        'ar-YE',
        'as',
        'as-IN',
        'asa',
        'asa-TZ',
        'ast',
        'ast-ES',
        'az',
        'az-Cyrl',
        'AZC',
        'az-Latn',
        'AZE',
        'bas',
        'bas-CM',
        'be',
        'be-BY',
        'bem',
        'bem-ZM',
        'bez',
        'bez-TZ',
        'bg',
        'bg-BG',
        'bgc',
        'bgc-IN',
        'bho',
        'bho-IN',
        'bm',
        'bm-ML',
        'bn',
        'bn-BD',
        'bn-IN',
        'bo',
        'bo-CN',
        'bo-IN',
        'br',
        'br-FR',
        'brx',
        'brx-IN',
        'bs',
        'bs-Cyrl',
        'BSC',
        'bs-Latn',
        'BSB',
        'ca',
        'ca-AD',
        'ca-ES',
        'ca-FR',
        'ca-IT',
        'ccp',
        'ccp-BD',
        'ccp-IN',
        'ce',
        'ce-RU',
        'ceb',
        'ceb-PH',
        'cgg',
        'cgg-UG',
        'chr',
        'chr-US',
        'ckb',
        'ckb-IQ',
        'ckb-IR',
        'cs',
        'cs-CZ',
        'cv',
        'cv-RU',
        'cy',
        'cy-GB',
        'da',
        'da-DK',
        'da-GL',
        'dav',
        'dav-KE',
        'de',
        'de-AT',
        'de-BE',
        'de-CH',
        'de-DE',
        'de-IT',
        'de-LI',
        'de-LU',
        'dje',
        'dje-NE',
        'doi',
        'doi-IN',
        'dsb',
        'dsb-DE',
        'dua',
        'dua-CM',
        'dyo',
        'dyo-SN',
        'dz',
        'dz-BT',
        'ebu',
        'ebu-KE',
        'ee',
        'ee-GH',
        'ee-TG',
        'el',
        'el-CY',
        'el-GR',
        'en',
        'en-001',
        'en-150',
        'en-AE',
        'en-AG',
        'en-AI',
        'en-AS',
        'en-AT',
        'en-AU',
        'en-BB',
        'en-BE',
        'en-BI',
        'en-BM',
        'en-BS',
        'en-BW',
        'en-BZ',
        'en-CA',
        'en-CC',
        'en-CH',
        'en-CK',
        'en-CM',
        'en-CX',
        'en-CY',
        'en-DE',
        'en-DG',
        'en-DK',
        'en-DM',
        'en-ER',
        'en-FI',
        'en-FJ',
        'en-FK',
        'en-FM',
        'en-GB',
        'en-GD',
        'en-GG',
        'en-GH',
        'en-GI',
        'en-GM',
        'en-GU',
        'en-GY',
        'en-HK',
        'en-IE',
        'en-IL',
        'en-IM',
        'en-IN',
        'en-IO',
        'en-JE',
        'en-JM',
        'en-KE',
        'en-KI',
        'en-KN',
        'en-KY',
        'en-LC',
        'en-LR',
        'en-LS',
        'en-MG',
        'en-MH',
        'en-MO',
        'en-MP',
        'en-MS',
        'en-MT',
        'en-MU',
        'en-MV',
        'en-MW',
        'en-MY',
        'en-NA',
        'en-NF',
        'en-NG',
        'en-NL',
        'en-NR',
        'en-NU',
        'en-NZ',
        'en-PG',
        'en-PH',
        'en-PK',
        'en-PN',
        'en-PR',
        'en-PW',
        'en-RW',
        'en-SB',
        'en-SC',
        'en-SD',
        'en-SE',
        'en-SG',
        'en-SH',
        'en-SI',
        'en-SL',
        'en-SS',
        'en-SX',
        'en-SZ',
        'en-TC',
        'en-TK',
        'en-TO',
        'en-TT',
        'en-TV',
        'en-TZ',
        'en-UG',
        'en-UM',
        'en-US',
        'ZZZ',
        'en-VC',
        'en-VG',
        'en-VI',
        'en-VU',
        'en-WS',
        'en-ZA',
        'en-ZM',
        'en-ZW' )
    
    titles = {}
    for lang in languages:
        titles[lang] = f'Text for { lang }'
    
    test_one(client, server, { 'links' : [ {
        "rel" : f"https://host.example.com/some/where",
        "titles" : titles } ] })
