from graph.base import Graph
from itertools import count
from uuid import uuid4;
import sys


class GrammarTagger:

    def __init__(self, graph):
        self._structure_graph = graph;

    @property
    def structureGraph(self):
        return self._structure_graph;


    def tag(self,tagsList):
        taggingGraph = Graph();
        taggingDict =[]
        print();
        print( tagsList);
        i = 0;
        for tag in tagsList:
            print();
            print(tag) 
            connectors = self.structureGraph.search_nodes(type=tag)
            connectorsList = [];

            newConnectorName = tag + "_" + str(i) #uuid4().hex;
            for connector in connectors:
                print(connector); 
                edge = connector.outgoing[0];
                topNode = edge.other_end(connector);
                #print(connector);
                #print(topNode);
                # We add in the sentence's graph the element (connector) and the
                # group (top Node)
                newTopNodeName = topNode.name + "_" + str(i) # uuid4().hex;

                if newConnectorName not in taggingGraph:
                    connectorNode = taggingGraph.add_node( newConnectorName, **connector.data);
                    connectorNode.color = "red";
                    connectorNode.shape = "box";
                
                topNode = taggingGraph.add_node( newTopNodeName , **topNode.data );
                #only for style
                topNode.color = 'green';
                topNode.shape = "box";
                
                print(taggingGraph.add_edge(
                    newConnectorName,
                    newTopNodeName,
                    label = edge.order,
                    is_directed=False,
                ));

                ruleName = topNode.name
                category = topNode.category
                position = edge.order
                connectorsList.append(
                    (ruleName, category, position)
                );
                i += 1;
            taggingDict.append((tag,connectorsList));
 
        #print(taggingDict);
        from graph.extras import dot
        from subprocess import getstatusoutput

        # build the drawing tool
        drawer = dot.DotGenerator()

        # populate the output file
        with open('dot/tagging_graph.dot', 'w') as f:
            output = drawer.draw(taggingGraph, "tag_graph")
            f.write(output)

        getstatusoutput("dot -Tgif -o picture/tag/tagging_graph.gif -v dot/tagging_graph.dot")


    def clone_node(self, node):


        return 0;



