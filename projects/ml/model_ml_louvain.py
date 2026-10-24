import networkx as nx
import community as community_louvain
import matplotlib.pyplot as plt

# 构建图（示例）
G = nx.karate_club_graph()

# 执行 Louvain 算法
partition = community_louvain.best_partition(G)

# partition 是一个字典：{node: community_id}
print(partition)

# 计算模块度
modularity = community_louvain.modularity(partition, G)
print("Modularity:", modularity)

# 可视化（可选）
pos = nx.spring_layout(G)
colors = [partition[node] for node in G.nodes()]
nx.draw(G, pos, node_color=colors, cmap=plt.cm.tab20)
plt.show()