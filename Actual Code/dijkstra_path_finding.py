import heapq

graph = {
    "SP": {"LB2": 75, "LB3": 75},
    "LB2": {"SP": 75, "LB3": 75, "LB1": 30},
    "LB3": {"SP": 75, "LB2": 75, "LB4": 30},
    "LB1": {"LB2": 30, "AL": 70},
    "LB4": {"LB3": 30, "BL": 70},
    "AL": {"LB1": 70, "LJ": 205},
    "BL": {"LB4": 70, "LJ": 205},
    "LJ": {"AL": 205, "BL": 205, "UJ": 140},
    "UJ": {"LJ": 140, "AU": 80, "BU": 80},
    "AU": {"UJ": 80},
    "BU": {"UJ": 80},
}

directions = {
    ("SP", "LB2"): "W", ("LB2", "SP"): "E",
    ("SP", "LB3"): "E", ("LB3", "SP"): "W",
    ("LB2", "LB1"): "W", ("LB1", "LB2"): "E",
    ("LB3", "LB4"): "E", ("LB4", "LB3"): "W",
    ("LB1", "AL"): "N", ("AL", "LB1"): "S",
    ("LB4", "BL"): "N", ("BL", "LB4"): "S",
    ("AL", "LJ"): "N", ("LJ", "AL"): "S",
    ("BL", "LJ"): "N", ("LJ", "BL"): "S",
    ("LJ", "UJ"): "N", ("UJ", "LJ"): "S",
    ("UJ", "AU"): "W", ("AU", "UJ"): "E",
    ("UJ", "BU"): "E", ("BU", "UJ"): "W",
}


def dijkstra(graph, start, goal):
    queue = [(0, start)]
    dist = {n: float("inf") for n in graph}
    prev = {n: None for n in graph}
    dist[start] = 0

    while queue:
        d, node = heapq.heappop(queue)
        if node == goal:
            break
        if d > dist[node]:
            continue
        for nbr, w in graph[node].items():
            nd = d + w
            if nd < dist[nbr]:
                dist[nbr] = nd
                prev[nbr] = node
                heapq.heappush(queue, (nd, nbr))

    # reconstruct path
    path = []
    n = goal
    while n:
        path.insert(0, n)
        n = prev[n]
    return path, dist[goal]