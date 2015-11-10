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

"""A simple CSV uploader client for the GCI API.

Usage:
  ./csv_uploader --apikey abc123 tasks.csv

Note:
 This uploader will attempt to upload all tasks in the file.  If you run it
 more than once on a file, you will end up with duplicate tasks.

"""

import argparse
import csv

import requests
import client as gciclient


argparser = argparse.ArgumentParser(description='GCI CSV Task Uploader.')
argparser.add_argument('--apikey', type=str, nargs='?', required=True,
                       help='api key')
argparser.add_argument('--url', type=str, nargs='?', required=True,
                       default='https://codein.withgoogle.com',
                       help='server url')
argparser.add_argument('--publish', action='store_true',
                       help='publish uploaded tasks')
argparser.add_argument('-v', '--verbose', action='store_true',
                       help='enable verbose logging')
argparser.add_argument('--debug', action='store_true',
                       help='enable debug request logging')
argparser.add_argument('files', nargs=argparse.REMAINDER,
                       help='csv file to upload')

FLAGS = argparser.parse_args()


def upload(client, filename):
  """Creates new tasks for each line in the csv pointed to by filename.

  Args:
    client: A GCIAPIClient to form and make the requests.
    filename: A string filename containing the csv encoded tasks.

  Raises:
    none
  """
  with open(filename, 'rb') as csvfile:
    taskreader = csv.DictReader(csvfile)

    for task in taskreader:
      t = task
      t['status'] = 2 if FLAGS.publish else 1
      t['mentors'] = task['mentors'].split(',')
      t['categories'] = task['categories'].split(',')
      t['tags'] = task['tags'].split(',')
      t['is_beginner'] = (
          True if task['is_beginner'].lower() in ['yes', 'true', '1']
          else False)
      t['time_to_complete_in_days'] = int(task['time_to_complete_in_days'])
      t['max_instances'] = int(task['max_instances'])

      try:
        t = client.NewTask(t)
        if FLAGS.verbose:
          print '\t'.join(['OK', str(t['id']), t['name'], ''])
      except requests.exceptions.HTTPError as e:
        if FLAGS.verbose:
          print '\t'.join(['ERROR', '', t['name'], e.response.text])


def main():
  client = gciclient.GCIAPIClient(
      auth_token=FLAGS.apikey,
      url_prefix=FLAGS.url,
      debug=FLAGS.debug)

  for filename in FLAGS.files:
    upload(client, filename)


if __name__ == '__main__':
  main()
