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
                    connectorNode.connected = True;
                
                newTopNode = taggingGraph.add_node( newTopNodeName , **topNode.data );
                #only for style
                newTopNode.color = 'green';
                newTopNode.shape = "box";
                newTopNode.connected = False;
                
                currentEdge = taggingGraph.add_edge(
                    newConnectorName,
                    newTopNodeName,
                    label = edge.order,
                    order = edge.order,
                    is_directed=False,
                );
                # now we had the non-connected terminal of the rule
                j = 0;
                for outgoingEdge in topNode.outgoing:
                    if currentEdge.order == outgoingEdge.order:
                        j += 1;
                        continue
                    
                    unconnectedAtom = outgoingEdge.other_end(topNode);
                    tempNodeName = unconnectedAtom.name + "_" + str(j) + str(i);
                    unconnectedTagNode = taggingGraph.add_node(tempNodeName, **unconnectedAtom.data)
                    unconnectedTagNode.color = "blue";
                    unconnectedTagNode.shape = "box";
                    unconnectedTagNode.connected = False;

                    taggingGraph.add_edge(
                        tempNodeName,
                        newTopNodeName,
                        label = outgoingEdge.order,
                        order = outgoingEdge.order,
                        is_directed = False
                    )

                    j += 1;

                ruleName = topNode.name
                category = topNode.category
                position = edge.order
                connectorsList.append(
                    (ruleName, category, position)
                );
                i += 1;
            taggingDict.append((tag,connectorsList));
        self.export_graph(taggingGraph, 1);

    def export_graph(self, taggingGraph, step) :
        
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

       

