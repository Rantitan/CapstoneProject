import networkx as nx
import copy

class FN_algorithm(object):
    def __init__(self, G):
        self.cloned_G = nx.Graph()
        self.cloned_G.add_edges_from(list(G.edges.data()))

        self.original_G = G
        self.max_Q = float("-inf")

        self.partition = None
        self.partition_dic = dict()

        self.community = {} # community  id : [node1, node2, .....]
        self.Node_CommunityIndex = {} # node id : community  id

        for index,node_id in enumerate(G.nodes()):
            self.community[index] = [node_id]
            self.Node_CommunityIndex[node_id] = index

    def get_partition(self):
        while len(self.community) > 1:
            det_Q = float("-inf")
            max_edge = None

            for edge in self.cloned_G.edges():
                index_i = self.Node_CommunityIndex[edge[0]]
                index_j = self.Node_CommunityIndex[edge[1]]

                # Don't consider the edges that have been divided into the same community
                if index_i == index_j: continue

                # Calculate the det_Q of two communities
                cur_Q = self.cal_det_Q(self.community[index_i], self.community[index_j])

                # Find and merge the two communities with the largest increase in Q value to merge
                if cur_Q > det_Q:
                    det_Q = cur_Q
                    max_edge = edge

            if max_edge is None: break

            # Merge two communities
            index_i = self.Node_CommunityIndex[max_edge[0]]
            index_j = self.Node_CommunityIndex[max_edge[1]]
            self.community[index_i].extend(self.community[index_j])
            for node in self.community[index_j]:
                self.Node_CommunityIndex[node] = index_i

            del self.community[index_j]
            # Community i and j have been merged,
            # thus the edges in the merged community can be removed to
            # reduce subsequent traversal
            self.cloned_G.remove_edge(max_edge[0], max_edge[1])

            # Find the division method with the largest Q value
            components = copy.deepcopy(list(self.community.values()))
            cur_Q = self.cal_Q(components)
            if cur_Q > self.max_Q:
                self.max_Q = cur_Q
                self.partition = components

        for index in range(len(self.partition)):
            for node_id in self.partition[index]:
                self.partition_dic[node_id] = index

        return self.partition_dic

    def cal_det_Q(self, partition_i, partition_j):
        m = len(list(self.original_G.edges()))

        a_i = 0
        for node in partition_i:
            a_i += len(list(self.original_G.neighbors(node)))
        a_i = a_i / float(2 * m)

        a_j = 0
        for node in partition_j:
            a_j += len(list(self.original_G.neighbors(node)))
        a_j = a_j / float(2 * m)

        e_ij = 0
        for i in range(len(partition_i)):
            for j in range(len(partition_j)):
                if self.original_G.has_edge(partition_i[i], partition_j[j]):
                    e_ij += 1

        e_ij = e_ij / float(2 * m)
        return 2 * (e_ij - a_i * a_j)

    def cal_Q(self,components):
        m = len(list(self.original_G.edges()))
        a = []
        e = []

        for community in components:
            t = 0
            for node in community:
                t += len(list(self.original_G.neighbors(node)))
            a.append(t / float(2 * m))

        for community in components:
            t = 0
            for i in range(len(community)):
                for j in range(len(community)):
                    if i != j:
                        if self.original_G.has_edge(community[i], community[j]):
                            t += 1

            e.append(t / float(2 * m))

        q = 0
        for ei, ai in zip(e, a):
            q += (ei - ai ** 2)

        return q
