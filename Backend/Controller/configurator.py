#
#   Desc:   Interface for configuration-objects. These objects 
#           are managing all values of the controller, that can be stored 
#           outside in a configuration-file.
#
class Configurator:

    def __init__(self):
        raise NotImplementedError

    #
    #   Desc:   Initialize the Pinger.
    #
    #   @result
    #           Returns a managedPinger with registered BasePingers.
    #
    def initializePinger(self):
        raise NotImplementedError

#
#   Desc:   Takes a yaml-file with all configuration-properties
#
class YmlConfigurator(Configurator):

    #
    #   Desc:   Cronstructor
    #
    #   @param filename
    #           Type String. Specifies the file with the configuration 
    #           properties.
    #
    #   @throws FileNotFoundError 
    #           if file from parameter filename is not found
    #
    def __init__(self, filename):
        # TODO Check file exists
        # TODO Load File
        raise NotImplementedError

    #
    #   see Configurator.initializePinger
    #
    def initializePinger(self):
        #TODO implement
        raise NotImplementedError
