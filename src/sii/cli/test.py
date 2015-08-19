""" Testing of stuff related with SII Interactions/Validations/Document Generations/etc...
"""


def action_test(args):
    if args['auth']:
        return test_auth(args)


def test_auth(args):
    from sii.server.Seed  import Seed
    from sii.server.Token import Token

    try:
        palena_s = Seed("https://palena.sii.cl/DTEWS/CrSeed.jws?wsdl")
        palena_t = Token(palena_s, args['<key>'], args['<cert>'],
                         "https://palena.sii.cl/DTEWS/GetTokenFromSeed.jws?wsdl")
        if palena_t.message == "Token Creado":
            print("Connection with Palena: OK")
        else:
            print("Connection with Palena: FAILED ({0})".format(palena_t.message))
    except Exception as exc:
        print("Connection with Palena: ERROR ({0})".format(exc))

    try:
        maullin_s = Seed("https://maullin.sii.cl/DTEWS/CrSeed.jws?wsdl")
        maullin_t = Token(maullin_s, args['<key>'], args['<cert>'],
                          "https://maullin.sii.cl/DTEWS/GetTokenFromSeed.jws?wsdl")
        if maullin_t.message == "Token Creado":
            print("Connection with Maullin: OK")
        else:
            print("Connection with Maullin: FAILED ({0})".format(maullin_t.message))
    except Exception as exc:
        print("Connection with Maullin: ERROR ({0})".format(exc))

    return True
