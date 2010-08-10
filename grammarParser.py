from xml.dom.minidom import parse,Text
from inflecter import Inflecter
from graph.base import Graph

import sys


class GrammarParser:

    def __init__(self, lang):
        self._lang = lang;
        self._doml = parse(lang +"/grammar.xml");
        self._graph = Graph();
        

    # Define language of the dictionnary
    @property
    def lang(self):
        return self._lang;

    @lang.setter
    def lang(self, lang):
        self._lang = lang;

    # In memory representation of the grammar.xml
    @property
    def doml(self):
        return self._doml;

    @doml.setter
    def doml(self, doml):
        self._doml = doml;


    # Graph representation of the grammar
    @property
    def graph(self):
        return self._graph;

    
    def parse_doml(self):
        allNodes = self.doml.getElementsByTagName('node');
        i = 0;
        for node in allNodes:
            nodeType = node.getAttribute('type');
            id =node.getAttribute('id');
            positionRule = node.getAttribute('position');
            category = node.getAttribute('category');
            #add top node
            tempTopNode = self.graph.add_node(
                name = id,
                rule_id= id,
                type= nodeType,
                shape = "box",
                color = "red",
                category = category,
                position = positionRule
            )
            #add child node and link
            order = 0;
            for child in node.childNodes:
                if isinstance(child, Text):
                    continue
                typeChild = child.getAttribute('type');
                categoryChild = child.getAttribute('category');
                isAtom = (child.tagName == "atom") ;
                tempNode = self.graph.add_node(
                    name= typeChild + child.tagName + str(i),
                    type = typeChild,
                    isAtom = isAtom,
                    category = categoryChild,
                    shape = "box",
                    color = "green"
                )
                i = i + 1;
                self.graph.add_edge(
                    tempTopNode,
                    tempNode,
                    order = order,
                    label = order,
                );

                order = order + 1;
        self.export_graph();

    def export_graph(self):
        from graph.extras import dot
        from subprocess import getstatusoutput

        # build the drawing tool
        drawer = dot.DotGenerator()

        # populate the output file
        with open('dot/grammar_graph.dot', 'w') as f:
            output = drawer.draw(self.graph, "grammar_graph")
            f.write(output)

        getstatusoutput("dot -Tgif -o picture/grammar/grammar_graph.gif -v dot/grammar_graph.dot")

      
