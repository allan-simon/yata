
class Word :
    def __init__(self):
        self._lemme = None;
        self._flection = "";
        self._kind = None;
        self._attributes = {};

    def __string__(self):
        self._lemme;

    @property
    def lemme(self):
        return self._lemme;

    @lemme.setter
    def lemme(self, lemme):
        self._lemme = lemme;

    @property
    def kind(self):
        return self._kind;

    @kind.setter
    def kind(self, kind):
        self._kind = kind;

    @property
    def flection(self):
        return self._flection;

    @flection.setter
    def flection(self, flection):
        self._flection = flection;

    @property
    def attributes(self):
        return self._attributes;

    def add_attribute(self, name, value):
        self.attribute[name] = value;

    def lemme_node_name(self):
        # TODO improve to avoid duplicate
        return self.lemme + "_" + self.kind + "_lemme";
