#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
#           Copyright 2018 Dept. CSE SUSTech
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#
# --------------------------------------------------------------------------
#                         Don't Remove Authors Info                        |
# --------------------------------------------------------------------------


__author__ = 'Suraj Singh Bisht                  '  # Name Of Author
__credit__ = '[]                                 '  # Contributers Name
__contact__ = 'surajsinghbisht054@gmail.com       '  # Email
__copyright__ = 'Copyright 2018 Suraj Singh Bisht   '  # Copyright
__license__ = 'Apache 2.0                         '  # LICENSE
__Update__ = '2018-01-11 12:00:29.991758         '  # Last Update
__version__ = '0.1                                '  # Version
__maintainer__ = 'Suraj Singh Bisht                  '  # Project Current Maintainer
__status__ = 'Production                         '  # Project Status


# TODO: complete this

import socket
import struct

from ..samples import utils

UDP_STRUCTURE_FMT = '!HHHH'

class UDPPacket:
    def __init__(self,
                 dport=80,
                 sport=65535,
                 dst='127.0.0.1',
                 src=utils.get_ip(),  # '192.168.1.101',
                 data=''
                 ):
        self.dport = dport
        self.sport = sport
        self.src_ip = src
        self.dst_ip = dst
        self.data = data
        self.raw = None
        self.create_udp_feilds()
        self.assemble_udp_feilds()
        # self.calculate_chksum()
        # self.reassemble_udp_feilds()

    def assemble_udp_feilds(self):
        self.raw = struct.pack('!HHHH',  # Data Structure Representation
                               self.sport,  # Source Port
                               self.dport,  # Destination Port
                               self.udp_len,  # Total Length
                               self.udp_chksum,  # UDP
                             )

        self.calculate_chksum()  # Call Calculate CheckSum
        return

    def reassemble_udp_feilds(self):
        self.raw = struct.pack(UDP_STRUCTURE_FMT,
                               self.udp_src,
                               self.udp_dst,
                               self.udp_len,
                               socket.htons(self.udp_chksum)
                               )
        return

    def calculate_chksum(self):
        src_addr = socket.inet_aton(self.src_ip)
        dest_addr = socket.inet_aton(self.dst_ip)
        placeholder = 0
        protocol = socket.IPPROTO_UDP
        self.udp_len = len(self.raw) + len(self.data)

        psh = struct.pack('!4s4sBBH',
                          src_addr,
                          dest_addr,
                          placeholder,
                          protocol,
                          self.udp_len
                          )

        psh = ''.join([psh, self.raw, self.data])

        self.udp_chksum = self.chksum(psh)

        self.reassemble_udp_feilds()

        return

    def chksum(self, msg):
        s = 0  # Binary Sum

        # loop taking 2 characters at a time
        for i in range(0, len(msg), 2):
            if (i + 1) < len(msg):
                a = ord(msg[i])
                b = ord(msg[i + 1])
                s = s + (a + (b << 8))
            elif (i + 1) == len(msg):
                s += ord(msg[i])
            else:
                raise Exception("Something Wrong here")

        s = (s >> 16) + (s & 0xffff)
        # One's Complement
        s = s + (s >> 16)
        s = ~s & 0xffff

        return s

    def create_udp_feilds(self):

        # ---- [ Source Port ]
        self.udp_src = self.sport

        # ---- [ Destination Port ]
        self.udp_dst = self.dport

        # ---- [ Header Length ]
        self.udp_len = 16

        # ---- [ UDP CheckSum ]
        self.udp_chksum = 0

        return
