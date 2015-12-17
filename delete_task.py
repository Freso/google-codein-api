#!/usr/bin/python2
# Copyright 2015 MetaBrainz Foundation Inc. All rights reserved.
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

"""Delete a GCI task via the GCI API."""

import argparse
import re

import client as gciclient


argparser = argparse.ArgumentParser(description='GCI Task Deleter.')
argparser.add_argument('--apikey', type=str, nargs='?', required=True,
                       help='api key')
argparser.add_argument('--url', type=str, nargs='?',
                       default='https://codein.withgoogle.com',
                       help='server url')
argparser.add_argument('--debug', action='store_true',
                       help='enable debug request logging')
argparser.add_argument('--task', type=int, nargs='+', required=True,
                       help='the task(s) to delete')
# TODO: Add --force option to skip asking

FLAGS = argparser.parse_args()


def get_task_info(task_data):
    string = '{name} <https://codein.withgoogle.com/dashboard/tasks/{id}/>'
    return string.format(name=task_data['name'], id=task_data['id'])


def main():
    client = gciclient.GCIAPIClient(
      auth_token=FLAGS.apikey,
      url_prefix=FLAGS.url,
      debug=FLAGS.debug)

    user_query = 'Are you sure you want to delete this task? (N/y) '

    for task_id in FLAGS.task:
        task_data = client.GetTask(task_id)
        print '\nTASK: ' + get_task_info(task_data)
        user_response = raw_input(user_query)
        if user_response in ('Y', 'y'):
            deletion = client.DeleteTask(task_id)
            if not deletion:
                print 'Task deleted. Copy this Python data structure in ' +\
                      'case you change your mind and want to recreate it:'
                print task_data
            else:
                print 'Task deletion failed:'
                print deletion
        else:
            print 'Skipping the task.'

if __name__ == '__main__':
    main()
