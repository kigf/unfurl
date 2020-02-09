# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json

bitly_edge = {
    'color': {
        'color': '#E7572C'
    },
    'title': 'Bitly URL Shortener',
    'label': '🔗'
}
  

def expand_bitly_url(bitlink_id, api_key):
    # Ref: https://dev.bitly.com/v4/

    r = requests.post(
        'https://api-ssl.bitly.com/v4/expand',
        data=json.dumps({'bitlink_id': f'bit.ly/{bitlink_id}'}),
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'})

    if r.status_code == 200:
        return r.json()
    else:
        return False


def run(unfurl, node):

    if node.data_type == 'url.path':
        if 'bit.ly' in unfurl.find_preceding_domain(node):
            expanded_info = expand_bitly_url(node.value[1:], unfurl.api_keys.get('bitly'))

            node.hover = 'Bitly Short Links can be expanded via the Bitly API to show the ' \
                         '"long" URL and the creation time of the short-link.' \
                         '<a href="https://dev.bitly.com/v4/#operation/expandBitlink" ' \
                         'target="_blank">[ref]</a>'

            unfurl.add_to_queue(
                data_type='description', key=None, value=expanded_info['created_at'],
                label=f'Creation Time: {expanded_info["created_at"]}',
                hover='Short-link creation time, retrieved from Bitly API',
                parent_id=node.node_id, incoming_edge_config=bitly_edge)

            unfurl.add_to_queue(
                data_type='url', key=None, value=expanded_info['long_url'],
                label=f'Expanded URL: {expanded_info["long_url"]}', hover='Expanded URL, retrieved from Bitly API',
                parent_id=node.node_id, incoming_edge_config=bitly_edge)
