from flask_restful import Resource
import gwcomm as comm

lg = comm.logger(__name__)


class modlogin():
    """Login class

    Functions:
        reg -- Registration
        check -- Check login
    """

    def __init__(self, owner=None):
        import gwpd as pdfx

        owner = comm.sysconf.get(
            "srv_id", "SYSTEM") if owner == None else owner
        self.__usr_pwd = pdfx.pdvw("usr_pwd", path="./conf/data/auth", owner=owner)
        if len(self.__usr_pwd.get()) == 0:
            lg.warning("No account")
            pwd = comm.sysconf.get("srv_sct", "P@ssw0rd")
            if owner != "" and pwd != "":
                lg.warning("Init super user for registration")
                rtn = self.reg(
                    {"usr_cde": owner, "usr_name": "Super Account", "password": pwd, "acl": -1})
                if not(rtn):
                    lg.error("Save fail - Super account")

    def reg(self, data):
        """Registration function

        Arguments:
            data {dict} -- {"usr_cde", "usr_name", "password"}

        Returns:
            bool -- True - success, False - fail
        """
        from datetime import datetime
        obj = self.__usr_pwd
        rtn, _ = obj.insert(data)
        if not(rtn):
            lg.error("insert fail")
            return rtn
        rtn, _ = obj.save()
        return rtn

    def check(self, usr_cde, password):
        """Check login

        Arguments:
            usr_cde {string} -- User Code
            password {string} -- Password

        Returns:
            bool -- True - success, False - fail
            list -- DataFrame
        """
        rtn = self.__usr_pwd.get(
            filter={"usr_cde": usr_cde, "password": password})
        return False if rtn == [] else True, rtn
