#
# Copyright 2020 Proxeem (https://www.proxeem.fr/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import argparse
from string import Template
import requests


# Host notification template
hostNotificationTemplate = """{
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "themeColor": "$color",
    "summary": "$hostname is $state",
    "sections": [{
        "activityTitle": "$hostname",
        "activitySubtitle": "Host $notificationtype",
        "activityImage": "https://www.proxeem.fr/assets/img/centreon-host-$icon.png?v=20200506",
        "facts": [{
            "name": "Host",
            "value": "$hostalias"
        }, {
            "name": "IP",
            "value": "$hostip"
        }, {
            "name": "State",
            "value": "$state"
        }, {
            "name": "Output",
            "value": "$output"
        }],
        "markdown": true
    }],
}"""


# Service notification template
serviceNotificationTemplate = """{
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "themeColor": "$color",
    "summary": "$hostname / $service is $state",
    "sections": [{
        "activityTitle": "$hostname",
        "activitySubtitle": "$service $notificationtype",
        "activityImage": "https://www.proxeem.fr/assets/img/centreon-service-$icon.png?v=20200506",
        "facts": [{
            "name": "Host",
            "value": "$hostalias"
        }, {
            "name": "IP",
            "value": "$hostip"
        }, {
            "name": "Service",
            "value": "$service"
        }, {
            "name": "State",
            "value": "$state"
        }, {
            "name": "Output",
            "value": "$output"
        }],
        "markdown": true
    }],
}"""


# UI settings
states = {
	'UNKNOWN':     { 'color': 'CDCDCD', 'icon': 'unknown' },
	'OK':          { 'color': '87BD23', 'icon': 'ok' },
	'WARNING':     { 'color': 'FF9913', 'icon': 'warning' },
	'CRITICAL':    { 'color': 'ED1C24', 'icon': 'critical' },

    'UNREACHABLE': { 'color': 'CDCDCD', 'icon': 'unreachable' },	
    'UP':          { 'color': '87BD23', 'icon': 'up' },
	'DOWN':        { 'color': 'ED1C24', 'icon': 'down' }
}


# Parse command line
parser = argparse.ArgumentParser(
	prog='msteams-notify.py',
	description = 'Microsoft Teams notification script for Centreon',
	formatter_class = lambda prog: argparse.HelpFormatter(prog, max_help_position = 64))

parser.add_argument('webhookurl', help = 'MS Teams webhook URL')
parser.add_argument('type', help = 'Notification type')
parser.add_argument('hostname', help = 'Hostname')
parser.add_argument('hostalias', help = 'Host alias')
parser.add_argument('hostip', help = 'Host IP address')
parser.add_argument('state', help = 'Service or host state')
parser.add_argument('output', help = 'Service or host output message')
parser.add_argument('--service-description', help = 'Service description', default = '', dest = 'service')
args = parser.parse_args()


# Render template
notificationTemplate = Template(serviceNotificationTemplate if (args.service != '') else hostNotificationTemplate)
notificationMessage = notificationTemplate.substitute(
	color = states[args.state]['color'],
	icon = states[args.state]['icon'],
	notificationtype = (args.type).capitalize(),
	hostname = args.hostname,
	hostalias = (args.hostalias[:35] + '...') if len(args.hostalias) > 35 else args.hostalias,
	hostip = args.hostip,
	state = args.state,
	service = args.service,
	output = ((args.output).split(': ', 1)[1]) if ((args.output).find(': ') != -1) else args.output
)


# Send notification
requestHeaders = { 'Content-type': 'application/json' }
requests.post(args.webhookurl, data = notificationMessage, headers = requestHeaders)
