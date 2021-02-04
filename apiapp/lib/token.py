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


def get_identity(request):
    from flask_restplus import abort
    token = request.headers.get("Authorization")
    identity, _ = decode_token(token=token)
    owner = identity.get("usr_cde", None)
    acl = identity.get("acl", 0)
    if isinstance(acl, str):
        acl = int(acl)
    return owner, acl


def check_acl(acl, reqacl):
    from flask_restplus import abort
    if acl < reqacl:
        abort(401, msg=f"ACL not enough - required {reqacl}")
        return False
    return True
