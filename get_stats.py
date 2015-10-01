#!/usr/bin/env python
# Copyright (c) 2013 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

'''
== Description:

This script will demonstrate an API call against a Qumulo REST server.
It will first obtain authentication credentials from the server, and
then use them in the subsequent call.

== Script Usage:

SCRIPTNAME.py --host ip_address|hostname [options]

=== Required:

[-i | --ip | --host] ip|hostname    An ip address or hostname of a node in
                                        the cluster; use 'localhost' when
                                        running directly on the node

=== Options:

[-u | --user] username              Use 'username' for authentication
                                        (defaults to 'admin')
[-p | --pass] password            Use 'password' for authentication
                                        (defaults to 'admin')
[-P | --port] number                Use 'number' for the API server port
                                        (defaults to 8000)

-h | --help                         Print out the script usage/help

=== Examples:

- Run the script against a remote node
SCRIPTNAME.py --host 192.168.194.333

- Run the script against the localhost
SCRIPTNAME.py --host localhost

- Run the script against a remote node as a non-admin user
SCRIPTNAME.py --host localhost --user new_user --pass new_password

'''

# Import python libraries
import getopt
import sys

# Import Qumulo REST libraries
# Leaving in the 'magic file path' for customers who want to run these scripts
# from cust_demo as before
import qumulo.lib.auth
import qumulo.lib.request
import qumulo.rest

#### Classes
class FileStatsCommand(object):
    ''' class wrapper for REST API cmd so that we can new them up in tests '''
    def __init__(self, argv=None):
        self.port = 8000
        self.user = 'admin'
        self.passwd = 'admin'
        self.host = 'music' 
        self.demo_var = None
        self.connection = None
        self.creds = None

        if argv:

            opts = {}
            try:
                opts, _ = getopt.getopt(argv[1:], "hi:p:P:u:V:",\
                                        ["help", "host=", "ip=", "user=", \
                                        "pass=", "port="])

            except getopt.GetoptError, msg:
                print msg
                print __doc__

            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print __doc__
                    sys.exit(0)
                elif opt in ("--ip", "-i", "--host"):
                    self.host = arg
                elif opt in ("--port", "-P"):
                    self.port = arg
                elif opt in ("--user", "-u"):
                    self.user = arg
                elif opt in ("--pass", "-p"):
                    self.passwd = arg
                else:
                    print "Unrecognized option %s\n" % opt
                    print __doc__
                    sys.exit(1)

    def login(self):
        '''Obtain credentials from the REST server'''
        self.connection = None
        self.creds = None

        try:
            # Create a connection to the REST server
            self.connection = qumulo.lib.request.Connection(\
                                self.host, int(self.port))

            # Provide username and password to retreive authentication tokens
            # used by the credentials object
            login_results, _ = qumulo.rest.auth.login(\
                    self.connection, None, self.user, self.passwd)

            # Create the credentials object which will be used for
            # authenticating rest calls
            self.creds = qumulo.lib.auth.Credentials.\
                    from_login_response(login_results)
        except Exception, excpt:
            print "Error connecting to the REST server: %s" % excpt
            print __doc__
            sys.exit(1)




    def get_stats(self):
        ''' Create directory from the provided demo_var param using fs '''
        ## Make the API call
        try:
            stats = qumulo.rest.fs.read_fs_stats(self.connection, self.creds)
        except qumulo.lib.request.RequestError, excpt:
            print "Error: %s" % excpt
            sys.exit(1)

        return stats


### Main subroutine
def main():
    ''' Main entry point '''
    command = FileStatsCommand(sys.argv)
    command.login()
    stats = command.get_stats()
    print stats


# Main
if __name__ == '__main__':
    main()
