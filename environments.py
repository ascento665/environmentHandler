from abc import abstractmethod
import boto3

sns = boto3.client('sns')

# TODO send image too
def notify_app():
    print 'notifying app'
    response = sns.publish(
        TargetArn='arn:aws:sns:eu-west-1:572634146544:endpoint/APNS_SANDBOX/Kevin/c6de9f8c-4410-3878-958a-21c2a328c565',
        MessageStructure='json',
        Message={ 'APNS_SANDBOX': '{ "aps": { "alert": { "title": "intruder?", "body": "you tell me!" }, "mutable-content": 1 } }' }
    )
    print response

class EnvironmentBase(object):
    """
    Base class for an environment containing the state transition functions.
    each transition function should take no arguments and return the name (string)
    of the resulting environment
    """

    def __init__(self, name, light):
        """
        Arguments
        ---------
        name (string): name of the environment
        light (class HueWrapper): a hue light object
        """

        self.name = name
        self.light = light
        self.transitions = {
            'good_guy_entering': self.good_guy_entering,
            'bad_guy_entering': self.bad_guy_entering,
            'leaving_house': self.leaving_house,
            'requesting_dance_mode': self.requesting_dance_mode,
            'requesting_romantic_mode': self.requesting_romantic_mode
        }

    def activate_environment(self, name):
        if name == 'off':
            self.light.set_mode(0)

        elif name == 'normal':
            self.light.set_color(0, 255, 0)

        elif name == 'intruder':
            self.light.set_color(255, 0, 0)

        else:
            raise Exception(
                '[EnvironmentBase.activate_environment] unknown environment')
        return name

    @abstractmethod
    def good_guy_entering(self):
        print('gg entering THIS SHOULD NEVER BE CALLED')
        pass

    @abstractmethod
    def bad_guy_entering(self):
        print('bg entering THIS SHOULD NEVER BE CALLED')
        pass

    @abstractmethod
    def leaving_house(self):
        print('THIS SHOULD NEVER BE CALLED')
        pass

    @abstractmethod
    def requesting_dance_mode(self):
        print('THIS SHOULD NEVER BE CALLED')
        pass

    @abstractmethod
    def requesting_romantic_mode(self):
        print('THIS SHOULD NEVER BE CALLED')
        pass


class EnvironmentOff(EnvironmentBase):
    """
    the off environment (is active when nobody is in the room)
    """

    def __init__(self, light):
        super(EnvironmentOff, self).__init__('off', light)

    def good_guy_entering(self):
        # turn hue on and green
        return self.activate_environment('normal')

    def bad_guy_entering(self):
        notify_app()
        # turn hue on and red
        return self.activate_environment('off')

    def leaving_house(self):
        return self.activate_environment('alarm')

    def requesting_dance_mode(self):
        return self.activate_environment('dance')

    def requesting_romantic_mode(self):
        return self.activate_environment('romantic')


class EnvironmentNormal(EnvironmentBase):
    """
    the normal environment (is active when an authorized person is in the room)
    """

    def __init__(self, light):
        super(EnvironmentNormal, self).__init__('normal', light)

    def good_guy_entering(self):
        # turn hue on and green
        return self.activate_environment('normal')

    def bad_guy_entering(self):
        notify_app()
        # turn hue on and red
        return self.activate_environment('normal')

    def leaving_house(self):
        return self.activate_environment('alarm')

    def requesting_dance_mode(self):
        return self.activate_environment('dance')

    def requesting_romantic_mode(self):
        return self.activate_environment('romantic')


class EnvironmentIntruder(EnvironmentBase):
    """
    the intruder environment (is active when a non authorized person is in the room)
    """

    def __init__(self, light):
        super(EnvironmentIntruder, self).__init__('intruder', light)

    def good_guy_entering(self):
        # turn hue on and green
        return self.activate_environment('normal')

    def bad_guy_entering(self):
        # turn hue on and red
        return self.activate_environment('intruder')

    def leaving_house(self):
        return self.activate_environment('alarm')

    def requesting_dance_mode(self):
        return self.activate_environment('dance')

    def requesting_romantic_mode(self):
        return self.activate_environment('romantic')


class EnvironmentDance(EnvironmentBase):
    """
    the intruder environment (is active when a non authorized person is in the room)
    """

    def __init__(self, light):
        super(EnvironmentDance, self).__init__('dance', light)

    def good_guy_entering(self):
        # turn hue on and green
        return self.activate_environment('dance')

    def bad_guy_entering(self):
        # turn hue on and red
        return self.activate_environment('dance')

    def leaving_house(self):
        return self.activate_environment('alarm')

    def requesting_dance_mode(self):
        return self.activate_environment('dance')

    def requesting_romantic_mode(self):
        return self.activate_environment('romantic')


class EnvironmentRomantic(EnvironmentBase):
    """
    the intruder environment (is active when a non authorized person is in the room)
    """

    def __init__(self, light):
        super(EnvironmentRomantic, self).__init__('romantic', light)

    def good_guy_entering(self):
        # turn hue on and green
        return self.activate_environment('intruder')

    def bad_guy_entering(self):
        # turn hue on and red
        return self.activate_environment('intruder')

    def leaving_house(self):
        return self.activate_environment('alarm')

    def requesting_dance_mode(self):
        return self.activate_environment('dance')

    def requesting_romantic_mode(self):
        return self.activate_environment('romantic')
