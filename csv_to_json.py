import pandas as pd
import numpy as np
import FN
import networkx as nx
import json
import re
import sys
import community as community_louvain

class Conversion_script:
    def __init__(self,edge_path,node_path,json_path):
        self.G = nx.Graph()

        self.edge_path = edge_path
        self.node_path = node_path
        self.json_path = json_path

        self.nodes = []
        self.node_details_dic = dict() # node_id : node details

        self.edges = []

        self.node_hashmap = dict() # actual node id : node id begins from 1
        self.partition_dic = dict() # node id : partition id
        self.json_lst = []

    def load_data(self):
        edges_dataFrame = pd.read_csv(self.edge_path)
        nodes_dataFrame = pd.read_csv(self.node_path)

        edge_cols = list(edges_dataFrame.columns)
        if "Source" not in edge_cols  or "Target" \
                not in edge_cols or "Weight" not in edge_cols:
            print("Invalid column name exists in edges dataset.")
            sys.exit()


        edge_time_interval = [list(map(int,re.findall(r'[1-9]+\.?[0-9]*',s)))
                              for s in list(edges_dataFrame["TimeInterval"])]

        for i in range(len(edges_dataFrame)):
            self.edges.append((edges_dataFrame.iloc[i]["Source"],
                               edges_dataFrame.iloc[i]["Target"],
                               {"weight":edges_dataFrame.iloc[i]["Weight"],
                                "startYear":edge_time_interval[i][0],
                                "endYear":edge_time_interval[i][1]}))

        self.G.add_edges_from(self.edges)

        node_cols = list(nodes_dataFrame.columns)

        if "ID" not in node_cols or "Label" not in node_cols:
            print("Invalid column name exists in nodes dataset.")
            sys.exit()

        hasRecord = True
        if "Records" not in node_cols:
            hasRecord = False

        node_time_interval = [list(map(int,re.findall(r'[1-9]+\.?[0-9]*',s)))
                              for s in list(nodes_dataFrame["TimeInterval"])]

        for i in range(len(nodes_dataFrame)):
            node_id = nodes_dataFrame.iloc[i]["ID"]
            node_name = nodes_dataFrame.iloc[i]["Label"]
            node_record = nodes_dataFrame.iloc[i]["Records"] if hasRecord else 1
            temp = {"label":node_name,
                    "record":node_record,
                    "startYear":node_time_interval[i][0],
                    "endYear":node_time_interval[i][1]}

            self.nodes.append((node_id,temp))
            self.node_details_dic[node_id] = temp

        self.G.add_nodes_from(self.nodes)
        print("Number of edges: {}, Number of nodes: {}".format(
            len(self.G.edges.data()),len(self.G.nodes.data())))

    def get_nodeMap(self):
        count = 1
        nodes = list(self.G.nodes.data())
        for node in nodes:
            node_id = node[0]
            self.node_hashmap[node_id] = count
            count += 1

    def community_detection(self,choice):
        print("Execute the community detection...")
        if choice == 1:
            print("You have chosen the Fast Newman algorithm")
            fn = FN.FN_algorithm(self.G)
            self.partition_dic = fn.get_partition()

        elif choice == 2:
            print("You have chosen the Fast unfolding algorithm")
            input_resolution = eval(input("Please enter the resolution: "))
            flag = "weight" if input("Do you want to consider the weight? (y/n): ") == "y" \
                else "None"
            self.partition_dic = \
                community_louvain.best_partition(self.G,weight=flag,
                                                 resolution=input_resolution,
                                                 random_state=40)
        print("Succeed")
        print("Totally {} communities are detected".format(str(len(np.unique(list(self.partition_dic.values()))))))

    def to_json(self):
        print("Writing the information to json...")
        # creat the root node information
        root_partition_index = self.partition_dic[self.nodes[0][0]] + 1
        self.json_lst.append({"id":self.node_hashmap[self.nodes[0][0]],
                              "name":self.nodes[0][1]['label'],
                              "size":self.nodes[0][1]['record'],
                              "group":root_partition_index,
                              "startYear":self.nodes[0][1]['startYear'],
                              "endYear":self.nodes[0][1]['endYear']})

        for edge_index in range(0 , len(self.edges)):
            temp_dic = dict()
            current_node = self.edges[edge_index][1]
            parent_node = self.edges[edge_index][0]
            temp_dic["id"] = self.node_hashmap[current_node]
            temp_dic["name"] = self.node_details_dic[current_node]["label"]
            temp_dic["parent"] = self.node_hashmap[parent_node]
            temp_dic["size"] = self.node_details_dic[current_node]["record"]
            partition_index = self.partition_dic[current_node] + 1
            temp_dic["group"] = partition_index
            temp_dic["weight"] = self.edges[edge_index][2]["weight"]
            temp_dic["startYear"] = self.node_details_dic[current_node]["startYear"]
            temp_dic["endYear"] = self.node_details_dic[current_node]["endYear"]

            self.json_lst.append(temp_dic)

        jsonData = json.dumps(self.json_lst,indent=4)
        fileObject = open(self.json_path, "w")
        fileObject.write(jsonData)
        print("Succeed")
        fileObject.close()

if __name__ == "__main__":
    myTool = Conversion_script("./dataset/Edges.csv",
                               "./dataset/Nodes.csv",
                               "./processed data/Radial_Tree_data.json")
    myTool.load_data()
    myTool.get_nodeMap()
    myTool.community_detection(choice=2)
    myTool.to_json()
