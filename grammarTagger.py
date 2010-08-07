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
                    newTopNodeName
                );
                i += 1;
            taggingDict.append(connectorsList);
        self.export_graph(taggingGraph, 1);
        print(taggingDict);
        self.validate_rule(taggingGraph, taggingDict);
        self.export_graph(taggingGraph, 2);


    def export_graph(self, taggingGraph, step) :
        
        #print(taggingDict);
        from graph.extras import dot
        from subprocess import getstatusoutput

        # build the drawing tool
        drawer = dot.DotGenerator()

        # populate the output file
        name = "tagging_graph" + str(step);
        with open('dot/' + name + '.dot', 'w') as f:
            output = drawer.draw(taggingGraph, "tag_graph")
            f.write(output)

        getstatusoutput("dot -Tgif -o picture/tag/"+name+".gif -v dot/"+name+".dot")

       

    # stage 2 validate rule having all its node connectec
    def validate_rule(self, taggingGraph, taggingDict):
        print()
        print()
        print("stage 2");
        print()
        print()
        for position in taggingDict:
            for rule in position:
                ruleNode = taggingGraph[rule];
                allConnected = True;
                for edge in ruleNode.incoming:
                    atomNode = edge.start;
                    if not atomNode.connected:
                        allConnected = False;
                        break;
                if allConnected :
                    ruleNode.connected = True;
                    ruleNode.color= "red";
                print(ruleNode);
        return 0;


