import igraph as ig
import leidenalg as la

# 从 NetworkX 转换（或直接用 igraph 构建）
# 这里以 Karate Club 为例
import networkx as nx
G_nx = nx.karate_club_graph()
G_ig = ig.Graph.from_networkx(G_nx)

# 执行 Leiden 算法
partition = la.find_partition(G_ig, la.ModularityVertexPartition)

# 获取社区分配
membership = partition.membership  # 列表，索引为节点 ID（按 igraph 节点顺序）
print(membership)

# 模块度
print("Modularity:", partition.modularity)

# 如果需要映射回 NetworkX 节点标签，注意节点顺序一致性