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
            nodeName = node.getAttribute('name');
            id =node.getAttribute('id');
            for type in node.getAttribute('type').split(' '):
               
                #add top node
                tempTopNode = self.graph.add_node(
                    name= id,
                    type= nodeName,
                    shape = "box",
                    color = "red",
                    position= nodeName
                )
                #add child node and link
                order = 0;
                for child in node.childNodes:
                    if isinstance(child, Text):
                        continue
                    name = child.getAttribute('name');
                    tagName = child.tagName;
                    tempNode = self.graph.add_node(
                        name= name + tagName + str(i),
                        type = name,
                        category = tagName,
                        shape = "box",
                        color = "green"
                    )
                    i = i + 1;
                    self.graph.add_edge(
                        tempTopNode,
                        tempNode,
                        order = order,
                        label = order,
                        is_directed= False
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

      
