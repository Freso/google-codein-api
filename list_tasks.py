# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""List all tasks for your Organization via the GCI API."""

import argparse
import re

import client as gciclient


argparser = argparse.ArgumentParser(description='GCI CSV Task Uploader.')
argparser.add_argument('--apikey', type=str, nargs='?', required=True,
                       help='api key')
argparser.add_argument('--url', type=str, nargs='?',
                       default='https://codein.withgoogle.com',
                       help='server url')
argparser.add_argument('--debug', action='store_true',
                       help='enable debug request logging')

FLAGS = argparser.parse_args()


def main():
  client = gciclient.GCIAPIClient(
      auth_token=FLAGS.apikey,
      url_prefix=FLAGS.url,
      debug=FLAGS.debug)

  next_page = 1
  while next_page > 0:
    tasks = client.ListTasks(page=next_page)
    for t in tasks['results']:
      print '\t'.join([str(t['id']), t['name']])

    next_page = 0
    if tasks['next']:
      result = re.search(r'page=(\d+)', tasks['next'])
      if result:
        next_page = result.group(1)


if __name__ == '__main__':
  main()
