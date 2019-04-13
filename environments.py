from abc import abstractmethod


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
            'bad_guy_entering': self.bad_guy_entering
        }

    def activate_environment(self, name):
        if name == 'off':
            self.light.set_mode(0)
            self.light.set_color(0, 0, 0)

        elif name == 'normal':
            self.light.set_mode(1)
            self.light.set_color(0, 255, 0)

        elif name == 'intruder':
            self.light.set_mode(1)
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
        # turn hue on and red
        return self.activate_environment('intruder')


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
        # turn hue on and red
        return self.activate_environment('normal')


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
