import json
import urllib
from decimal import Decimal

import boto3
from environments import (EnvironmentAlarm, EnvironmentDance,
                          EnvironmentIntruder, EnvironmentNormal,
                          EnvironmentOff, EnvironmentRomantic)
from events import Events
from hue_wrapper_v1 import HueWrapperV1 as HueWrapper

s3 = boto3.resource('s3')

# ------------ Helper Functions ---------------


def environment_handler(event, environments, bucket, key):
    """
    main event handling function of state machine

    Arguments
    ---------
    event (enum class Events): the event which occured

    Returns
    -------
    void
    """

    # load the currently active environment from a json in s3
    state_object = s3.Object('asc-user-db', 'state-info/state.json')
    file_content = state_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    # returns a string containing the name
    old_active_env_name = json_content['active_env']

    # call the transition function form the currently active environment
    new_active_env_name = environments[old_active_env_name].transitions[event.name](
        bucket, key)

    # update the active state and save to json in s3
    json_content['active_env'] = new_active_env_name
    state_object.put(Body=bytes(json.dumps(
        json_content, indent=2).encode('utf-8')))

    # logging
    print('[environment_handler] changed env from {} to {} after event {}'.format(
        old_active_env_name, new_active_env_name, event.name))

    return


def lambda_handler(event, context):
    '''
    handles events and changes environments accordingly
    '''

    # extract event from payload
    print('incoming event', event)

    bucket = 'None'
    key = 'None'

    try:
        bucket = event['bucket']
        key = event['key']
    except Exception as e:
        pass

    event = Events[event['event']]

    try:
        # prepare environment handler
        # SETUP add more environments here
        light = HueWrapper()
        environments = {
            'off': EnvironmentOff(light),
            'normal': EnvironmentNormal(light),
            'intruder': EnvironmentIntruder(light),
            'alarm': EnvironmentAlarm(light),
            'dance': EnvironmentDance(light),
            'romantic': EnvironmentRomantic(light),
        }

        # handle event with state transitions
        environment_handler(event, environments, bucket, key)

    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e
