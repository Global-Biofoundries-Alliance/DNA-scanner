#
#   Der ComparisonService ist das allgemeine Interface. Es geht darum hier Prozessfälle abzudecken,
#   welche die Funktionen des Vergleichs (Upload, Matrix, Filtern) ... abbildet.
#   Es muss nicht umbedingt für einen Endpunkt in routes eine Methode geben. Eventuell kann man
#   z.B. an einem Endpunkt 2 methoden verwenden, welche eventuell in anderen ENdpunkten auch 
#   verwendet werden.
#
#   Review könnte später z.B: in einem ReviewService umgesetzt werden.
#
#   Allgemeines Beispiel:
#       \setFilter -> changeFilter() 
#       \resultsByFilter -> changeFilter() -> getResults()
#

# TODO war jetzt noch nicht ganz durchdacht. wurde erstmal nur schnell hingeworfen.

class ComparisonService:

    def __init__(self, configurator, sessionManager):
        raise NotImplementedError

    def setSequences(self, fileName):
        raise NotImplementedError

    def changeFilter(self):
        raise NotImplementedError


# TODO implement
class DefaultComparisonService(Controller):
    
    def __init__(self, configurator, sessionManager):
        pass
