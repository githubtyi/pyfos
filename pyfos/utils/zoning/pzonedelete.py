#!/usr/bin/env python3

# Copyright 2017 Brocade Communications Systems, Inc.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may also obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""

:mod:`pzonedelete` - PyFOS util for specific Zoning use case.
***********************************************************************************
The :mod:`pzonedelete` provides for specific Zoning use case.

This module is a standalone script and API that can be used to delete
existing Peer Zone(s).

* inputs:
    * -L=<login>: Login ID. If not provided, interactive
        prompt will request one.
    * -P=<password>: Password. If not provided, interactive
        prompt will request one.
    * -i=<IP address>: IP address
    * -n=<zonename>: string name of an existing Peer Zone.
    * -f=<VFID>: VFID or -1 if VF is disabled. If unspecified,
        VFID of 128 is assumed.

* outputs:
    * Python dictionary content with RESTCONF response data

"""

import pyfos.pyfos_auth as pyfos_auth
import pyfos.pyfos_zone as pyfos_zone
import sys
import pyfos.utils.brcd_zone_util as brcd_zone_util
import pyfos.utils.brcd_util as brcd_util

isHttps = "0"


def usage():
    print("usage:")
    print('pzonedelete.py -i <ipaddr> -n <name>')


def pzonedelete(session, zones):
    """Delete an existing Peer Zone(s)

    Example usage of the method::

        zones = [
                    {
                        "zone-name": name,
                        "zone-type": pyfos_zone.ZONE_TYPE_PEER,
                    }
               ]
        result = pzonedelete(session, zones)

    :param session: session returned by login
    :param zones: an array of zone and new members
    :rtype: dictionary of return status matching rest response

    *use cases*

        1. Delete an existing Peer Zone(s)

    """

    new_defined = pyfos_zone.defined_configuration()
    new_defined.set_zone(zones)
    result = new_defined.delete(session)
    return result


def __pzonedelete(session, name):
    zones = [
                {
                    "zone-name": name,
                    "zone-type": pyfos_zone.ZONE_TYPE_PEER
                }
            ]
    return pzonedelete(session, zones)


def main(argv):
    inputs = brcd_util.generic_input(argv, usage)

    session = pyfos_auth.login(inputs["login"], inputs["password"],
                               inputs["ipaddr"], isHttps)
    if pyfos_auth.is_failed_login(session):
        print("login failed because",
              session.get(pyfos_auth.CREDENTIAL_KEY)
              [pyfos_auth.LOGIN_ERROR_KEY])
        usage()
        sys.exit()

    brcd_util.exit_register(session)

    vfid = None
    if 'vfid' in inputs:
        vfid = inputs['vfid']

    if vfid is not None:
        pyfos_auth.vfid_set(session, vfid)

    brcd_zone_util.zone_name_func(session, inputs, usage, __pzonedelete)

    pyfos_auth.logout(session)


if __name__ == "__main__":
    main(sys.argv[1:])
