def decode_token(token):
    """Decode token to identity

    Arguments:
        token {string} -- Bearer token

    Returns:
        dict -- Identity
        string -- token
    """
    import jwt
    import re
    import gwcomm as comm
    token = re.sub("Bearer ", "", token)
    identity = jwt.decode(token, comm.sysconf.get(
        "secret_key")).get("identity", {})
    return identity, token
