import json


# @unittest.skipIf(not is_linux, 'preview_question only runs under Linux.') FIXME
def testPreviewQuestion(test_client, test_user_1):
    src = """
.. activecode:: preview_test1

   Hello World
   ~~~~
   print("Hello World")

"""
    test_user_1.login()

    kwargs = dict(code=json.dumps(src))
    test_client.post("ajax/preview_question", data=kwargs)
    print(test_client.text)
    res = json.loads(test_client.text)

    assert "id=preview_test1" in res
    assert 'print("Hello World")' in res
    assert "textarea>" in res
    assert 'div data-component="activecode"' in res


def test_Donations(test_client, test_user_1):
    test_user_1.login()
    res = ajaxCall(test_client, "save_donate")
    assert res == None

    res = ajaxCall(test_client, "did_donate")
    assert res["donate"] == True


def test_NonDonor(test_client, test_user_1):
    test_user_1.login()
    res = ajaxCall(test_client, "did_donate")
    assert not res["donate"]


def ajaxCall(client, funcName, **kwargs):
    """
    Call the funcName using the client
    Returns json.loads(funcName())
    """
    client.post("ajax/" + funcName, data=kwargs)
    print(client.text)
    if client.text != "None":
        return json.loads(client.text)
