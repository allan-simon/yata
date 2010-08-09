from graph.base import Graph
from itertools import count
import sys


class GrammarTagger:

    def __init__(self, graph):
        self._structure_graph = graph;

    @property
    def structureGraph(self):
        return self._structure_graph;


    def tag(self,tagsList):
        taggingGraph = Graph();
        taggingList =[]
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
                
                #we add the rule Node which current node can be part of
                newTopNode = taggingGraph.add_node( newTopNodeName , **topNode.data );
                #only for style
                newTopNode.color = 'green';
                newTopNode.shape = "box";
                newTopNode.rule_id = topNode.name;
                newTopNode.connected = False;
                

                # now we had the non-connected terminal of the rule
                j = 0;
                for outgoingEdge in topNode.outgoing:
                    if edge.order == outgoingEdge.order:
                        currentEdge = taggingGraph.add_edge(
                            newConnectorName,
                            newTopNodeName,
                            label = edge.order,
                            order = edge.order,
                            is_directed=False,
                        );
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
            taggingList.append(connectorsList);
        self.export_graph(taggingGraph, 1);
        self.validate_rule(taggingGraph, taggingList);
        self.export_graph(taggingGraph, 2);
        self.fusion_rule(taggingGraph, taggingList);
        self.export_graph(taggingGraph, 3);
        self.validate_rule(taggingGraph, taggingList);
        self.export_graph(taggingGraph, 4);
        self.remove_non_connected_rule(taggingGraph, taggingList);
        self.export_graph(taggingGraph, 5);
        self.remove_impossible_rule(taggingGraph, taggingList);
        self.export_graph(taggingGraph, 6);


    def export_graph(self, taggingGraph, step) :
        
        #print(taggingList);
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

       

    # stage 2 validate rule having all its node connected
    def validate_rule(self, taggingGraph, taggingList):
        print()
        print()
        print("stage 2");
        print()
        print()
        for position in taggingList:
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

    # stage 3 fusion same occurence of a rule which different
    # connected and unconnected atom
    def fusion_rule(self,taggingGraph, taggingList):
        print()
        print()
        print("stage 3");
        print()
        print()
        i = 0;
        for position in taggingList:
            for ruleInstance in position: 
                lastConnected = 0;
                ruleNode = taggingGraph[ruleInstance];
                # if the node already have all its item connected
                # then we already know no fusion is possible
                if ruleNode.connected == True:
                    break;
                ruleId = ruleNode.rule_id;
                print(ruleInstance)
                for atomEdge in ruleNode.incoming:
                    print(atomEdge);
                    if atomEdge.start.connected == False:
                        break;
                    lastConnected +=1;
                if lastConnected != 0 :
                    nextPosition = taggingList[i+1];
                    for nextRule in nextPosition:
                        nextRuleNode = taggingGraph[nextRule];
                        if nextRuleNode.rule_id != ruleId:
                            break;
                        print("possible fusion");
                        for nextAtomEdge in nextRuleNode.incoming:
                            nextAtomNode = nextAtomEdge.start;
                            if nextAtomEdge.order < lastConnected:
                                if nextAtomNode.connected == True:
                                    break
                            else:
                                if nextAtomNode.connected == False:
                                    break
                                nextAtomNode.connected = False;
                                nextAtomNode.color = "blue";
                                
                                tempNode = ruleNode.incoming[nextAtomEdge.order].start
                                tempNode.connected = True;
                                tempNode.color = "red";



            i += 1;

    def remove_non_connected_rule(self,taggingGraph, taggingList):
        print()
        print()
        print("stage 4");
        print()
        print()

        lenTaggingList = len(taggingList);
        i = 0;
        while i < lenTaggingList:
            position = taggingList[i];
            nbrRuleInstance = len(position);
            j = 0;
            while j < nbrRuleInstance:
                ruleInstance = position[j];
                ruleNode = taggingGraph[ruleInstance];
                if ruleNode.connected:
                    j +=1
                    continue;
                #first removed rule which don't have any node connected
                #anymore
                noneConnected = True;
                for edge in ruleNode.incoming:
                    atomNode = edge.start;
                    if atomNode.connected:
                        noneConnected = False;
                        break;
                if  noneConnected :
                    for edge in ruleNode.incoming:
                        atomNode = edge.start;
                        taggingGraph.remove_edge(edge);
                        taggingGraph.remove_node(atomNode);
                    taggingGraph.remove_node(ruleNode);
                    position.remove(ruleInstance);
                    j -= 1;
                    nbrRuleInstance -= 1;
                    if not position:
                        taggingList.remove(position);
                        lenTaggingList -=1;
                        i -= 1;
                j += 1;
            i +=1

    def remove_impossible_rule(self,taggingGraph, taggingList):
        print()
        print()
        print("stage 5");
        print()
        print()
        print(taggingList)
        
        lenTaggingList = len(taggingList);
        i = 0;
        while i < lenTaggingList:
            position = taggingList[i];
            nbrRuleInstance = len(position);
            j = 0;
            while j < nbrRuleInstance:
                ruleInstance = position[j];
                ruleNode = taggingGraph[ruleInstance];
                if ruleNode.connected:
                    j +=1
                    continue;
                print(ruleInstance); 
                #then removed rule which are looking for an atom which is not present
                atomNodeFound = False;
                for edge in ruleNode.incoming:
                    atomNode = edge.start;
                    if not atomNode.connected:
                        if atomNode.category == "atom":
                            for foudNode in taggingGraph.search_nodes(type = atomNode.type, connected = True):
                                atomNodeFound = True;
                                break;
                            if not atomNodeFound:
                                break;
                if not atomNodeFound:
                    for edge in ruleNode.incoming:
                        atomNode = edge.start;
                        taggingGraph.remove_edge(edge);
                        if not atomNode.connected:
                            taggingGraph.remove_node(atomNode);
                    taggingGraph.remove_node(ruleNode);
                    position.remove(ruleInstance);
                    j -= 1;
                    nbrRuleInstance -= 1;
                    if not position:
                        taggingList.remove(position);
                        lenTaggingList -=1;
                        i -= 1;
                j += 1;
            i +=1
