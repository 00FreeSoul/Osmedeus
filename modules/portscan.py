import os
import glob
import socket
import time
import json
from core import execute
from core import slack
from core import utils

from libnmap.parser import NmapParser
from libnmap.reportjson import ReportDecoder, ReportEncoder


class PortScan(object):
    """docstring for PortScan"""

    def __init__(self, options):
        utils.print_banner("Port Scanning")
        utils.make_directory(options['WORKSPACE'] + '/portscan')
        self.module_name = self.__class__.__name__
        self.options = options
        slack.slack_noti('status', self.options, mess={
            'title':  "{0} | {1}".format(self.options['TARGET'], self.module_name),
            'content': 'Start Port Scanning for {0}'.format(self.options['TARGET'])
        })
        self.initial()

        utils.just_waiting(self.module_name)
        # self.result_parsing()
        # self.conclude()
        slack.slack_noti('good', self.options, mess={
            'title':  "{0} | {1}".format(self.options['TARGET'], self.module_name),
            'content': 'Start Port Scanning for {0}'.format(self.options['TARGET'])
        })

    def initial(self):
        # self.create_ip_result()
        self.masscan()

    # just for the masscan

    def create_ip_result(self):
        utils.print_good('Create IP for list of domain result')
        cmd = '$PLUGINS_PATH/massdns/bin/massdns -r $PLUGINS_PATH/massdns/lists/resolvers.txt -t A -o S -w $WORKSPACE/subdomain/massdns-IP-$OUTPUT.txt $WORKSPACE/subdomain/final-$OUTPUT.txt'

        cmd = utils.replace_argument(self.options, cmd)
        output_path = utils.replace_argument(
            self.options, '$WORKSPACE/subdomain/massdns-IP-$OUTPUT.txt')
        std_path = utils.replace_argument(
            self.options, '$WORKSPACE/subdomain/std-massdns-IP-$OUTPUT.std')
        execute.send_cmd(cmd, output_path, std_path, self.module_name)

        utils.just_waiting(self.module_name, seconds=5)

        # matching IP with subdomain
        main_json = utils.reading_json(utils.replace_argument(
            self.options, '$WORKSPACE/$COMPANY.json'))
        with open(output_path, 'r') as i:
            data = i.read().splitlines()
        ips = []
        for line in data:
            if " A " in line:
                subdomain = line.split('. A ')[0]
                ip = line.split('. A ')[1]
                ips.append(ip)
                for i in range(len(main_json['Subdomains'])):
                    if subdomain == main_json['Subdomains'][i]['Domain']:
                        main_json['Subdomains'][i]['IP'] = ip

        final_ip = utils.replace_argument(
            self.options, '$WORKSPACE/subdomain/final-IP-$OUTPUT.txt')

        with open(final_ip, 'w+') as fip:
            fip.write("\n".join(str(ip) for ip in ips))

        utils.just_write(utils.replace_argument(
            self.options, '$WORKSPACE/$COMPANY.json'), main_json, is_json=True)

    def masscan(self):
        utils.print_good('Starting masscan')

        main_json = utils.reading_json(utils.replace_argument(
            self.options, '$WORKSPACE/$COMPANY.json'))
        main_json['Modules'][self.module_name] = []

        if self.options['SPEED'] == 'slow':
            ip_list = [x.get("IP")
                       for x in main_json['Subdomains'] if x.get("IP") is not None] + main_json['IP Space']

        elif self.options['SPEED'] == 'quick':
            ip_list = [x.get("IP")
                       for x in main_json['Subdomains'] if x.get("IP") is not None]


        # Scan every 5 IP at time Increse if you want
        for part in list(utils.chunks(ip_list, 5)):
            for ip in part:
                cmd = 'sudo masscan --rate 10000 -p0-65535 {0} -oJ $WORKSPACE/portscan/{0}-masscan.json --wait 0'.format(
                    ip)

                cmd = utils.replace_argument(self.options, cmd)
                output_path = utils.replace_argument(
                    self.options, '$WORKSPACE/portscan/{0}-masscan.gnmap'.format(ip))
                std_path = utils.replace_argument(
                    self.options, '$WORKSPACE/portscan/std-{0}-masscan.gnmap.std'.format(ip))
                execute.send_cmd(cmd, '', '', self.module_name)

            # check if previous task done or not every 30 second
            while not utils.checking_done(module=self.module_name):
                time.sleep(20)

            # update main json
            main_json['Modules'][self.module_name] += utils.checking_done(
                module=self.module_name, get_json=True)

