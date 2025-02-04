
import heapq

def dijkstra(start, graph):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    previous = {vertex: None for vertex in graph}
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Если расстояние больше, чем уже найденное, пропускаем
        if current_distance > distances[current_vertex]:
            continue
            
        for neighbor, weight in graph[current_vertex].items():
            if neighbor not in distances:
                continue
            distance = current_distance + weight

            if neighbor==start and distance<0:
                return distance,[]
            # Только если найдено меньшее расстояние
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
    return distances, previous

def reconstruct_path(previous, start, target):
    path = []
    while target is not None:
        path.append(target)
        target = previous.get(target)  # Используем get для безопасного доступа
    path.reverse()
    
    # Проверка, был ли путь найден
    if path and path[0] == start:
        return path
    else:
        return []  # Возвращаем пустой список, если путь не найден