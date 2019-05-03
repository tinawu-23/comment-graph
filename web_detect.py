#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
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

"""Demonstrates web detection using the Google Cloud Vision API.

Example usage:
  python web_detect.py https://goo.gl/X4qcB6
  python web_detect.py ../detect/resources/landmark.jpg
  python web_detect.py gs://your-bucket/image.png
"""
# [START full_tutorial]

# Authentification
# export GOOGLE_APPLICATION_CREDENTIALS="/home/laylalaisys/Desktop/test0-57468f06f134.json"

# [START imports]
import argparse     # allow the application to accept input filenames as arguments
import io           # for reading from files

import json

# Imports the Google Cloud client library
from google.cloud import vision         # for accessing the Vision API
from google.cloud.vision import types   # for constructing requests
# [END imports]

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    return True

def store_json(id, myjson):
    filename='./webDetectionJson/'+id+'.json'
    with open( filename, 'w') as f:
        f.write(json.dumps(myjson))

def construct_list(annotations):
    # entity = [{"id":1, "score":10}, {"id":2, "score":20}]
    # fully = [{"url":"http"}, {"url":"https"}]
    # test = [{"entity":entity, "fully":fully}]
    web_entities = []
    pages_with_matching_images = []
    full_matching_images = []
    partial_matching_images = []
    webDetectionList = []

    if annotations.web_entities:                # print web_entites
        for entity in annotations.web_entities:
            web_entities.append({"entity_id":entity.entity_id, "score":entity.score, "description": entity.description})
    
    if annotations.pages_with_matching_images:  # print pages_with_matching_images
        for page in annotations.pages_with_matching_images:
            pages_with_matching_images.append({"url":page.url})

    if annotations.full_matching_images:        # print full_matching_images
        for image in annotations.full_matching_images:
            full_matching_images.append({"url":image.url})

    if annotations.partial_matching_images:     # print partial_matching_images
        for image in annotations.partial_matching_images:
            partial_matching_images.append({"url":image.url})

    webDetectionList.append({"web_entities":web_entities, "pages_with_matching_images":pages_with_matching_images,"full_matching_images":full_matching_images, "partial_matching_images":partial_matching_images})
    
    return webDetectionList

def annotate(path): # constructing the request
    """Returns web annotations given the path to an image."""
    # [START get_annotations]
    # Instantiates a client
    client = vision.ImageAnnotatorClient()  # create an ImageAnnotaorClient instance as the client

    if path.startswith('http') or path.startswith('gs:'):   # constructs an Image object from either a URL
        image = types.Image()
        image.source.image_uri = path

    else:                                                   # constructs an Image object from a local file
        # Loads the image into memory
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    # Performs web detection on the image 
    response = client.web_detection(image=image)
    web_detection = response.web_detection                  # passes the Image object to the web_detection method of the client
    # [END get_annotations]

    return web_detection    # returns the annotations


def report(annotations):
    """Prints detected features in the provided web annotations."""
    # [START print_annotations]
    if annotations.web_entities:                # print web_entites
        print ('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))

    if annotations.pages_with_matching_images:  # print pages_with_matching_images
        print('\n{} Pages with matching images retrieved'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if annotations.full_matching_images:        # print full_matching_images
        print ('\n{} Full Matches found: '.format(
               len(annotations.full_matching_images)))

        for image in annotations.full_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.partial_matching_images:     # print partial_matching_images
        print ('\n{} Partial Matches found: '.format(
               len(annotations.partial_matching_images)))

        for image in annotations.partial_matching_images:
            print('Url  : {}'.format(image.url))
    # [END print_annotations]


if __name__ == '__main__':  # running the application
    # [START run_web]
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    path_help = str('The image to detect, can be web URI, '
                    'Google Cloud Storage, or path to local file.')
    parser.add_argument('--u', help=path_help)  # image_url
    parser.add_argument('--id')                 # image_id
    args = parser.parse_args()                  # parse the passed-in argument that specifies the URL of the Web image

    # get the result of web detection
    # web_detection_result = annotate(args.image_url)
    # print the result of web detection
    # report(web_detection_result)  

    # entity = [{"id":1, "score":10}, {"id":2, "score":20}]
    # fully = [{"url":"http"}, {"url":"https"}]
    # test = [{"entity":entity, "fully":fully}]
    # store_json(test)
    store_json(args.id, construct_list(annotate(args.u)))
    # [END run_web]
# [END full_tutorial]