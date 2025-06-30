import matplotlib.pyplot as plt
import random
import math
import time

# Generar 500 puntos aleatorios
random.seed(42)
n_points = 500
points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n_points)]

# Función auxiliar para determinar la orientación de 3 puntos
def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # colineales
    return 1 if val > 0 else 2  # horario o antihorario

# 1. Algoritmo de Jarvis March (Gift Wrapping)
def jarvis_march(points):
    n = len(points)
    if n < 3:
        return points
    
    # Encontrar el punto más a la izquierda
    leftmost = min(points, key=lambda x: x[0])
    hull = []
    p = leftmost
    q = None
    
    while True:
        hull.append(p)
        q = points[0] if points[0] != p else points[1]
        
        for r in points:
            if r == p or r == q:
                continue
            # Encontrar el punto más a la "izquierda" en relación con p-q
            o = orientation(p, q, r)
            if o == 2 or (o == 0 and ((r[0] - p[0])**2 + (r[1] - p[1])**2 > (q[0] - p[0])**2 + (q[1] - p[1])**2)):
                q = r
        
        p = q
        if p == hull[0]:
            break
    
    return hull

# 2. Algoritmo de Graham Scan
def graham_scan(points):
    n = len(points)
    if n < 3:
        return points
    
    # Encontrar el punto con la coordenada y más baja (y más a la izquierda en caso de empate)
    pivot = min(points, key=lambda x: (x[1], x[0]))
    
    # Función para calcular el ángulo y distancia respecto al pivot
    def angle_distance(p):
        if p == pivot:
            return (0, 0)
        dx = p[0] - pivot[0]
        dy = p[1] - pivot[1]
        angle = math.atan2(dy, dx)
        dist = dx*dx + dy*dy
        return (angle, dist)
    
    # Ordenar los puntos por ángulo y distancia
    sorted_points = sorted(points, key=angle_distance)
    
    # Construir el hull
    hull = [pivot, sorted_points[0]]
    
    for p in sorted_points[1:]:
        while len(hull) > 1 and orientation(hull[-2], hull[-1], p) != 2:
            hull.pop()
        hull.append(p)
    
    return hull

# 3. Algoritmo QuickHull
def quickhull(points):
    if len(points) <= 2:
        return points
    
    # Encontrar los puntos extremos izquierdo y derecho
    left = min(points, key=lambda x: x[0])
    right = max(points, key=lambda x: x[0])
    
    hull = []
    
    def find_hull(points, p, q, hull):
        if not points:
            return
        
        # Encontrar el punto más lejano de la línea pq
        farthest = None
        max_distance = 0
        line_vec = (q[0] - p[0], q[1] - p[1])
        
        for point in points:
            # Calcular distancia perpendicular
            vec = (point[0] - p[0], point[1] - p[1])
            cross = abs(line_vec[0] * vec[1] - line_vec[1] * vec[0])
            if cross > max_distance:
                max_distance = cross
                farthest = point
        
        if farthest is None:
            return
        
        # Añadir el punto más lejano al hull
        hull.append(farthest)
        
        # Dividir los puntos en tres grupos
        left_points = []
        right_points = []
        for point in points:
            if point == farthest or point == p or point == q:
                continue
            if orientation(p, farthest, point) == 2:
                left_points.append(point)
            if orientation(farthest, q, point) == 2:
                right_points.append(point)
        
        # Recursión
        find_hull(left_points, p, farthest, hull)
        find_hull(right_points, farthest, q, hull)
    
    # Dividir los puntos en los que están arriba y abajo de la línea left-right
    upper_points = []
    lower_points = []
    for point in points:
        if point == left or point == right:
            continue
        o = orientation(left, right, point)
        if o == 2:
            upper_points.append(point)
        elif o == 1:
            lower_points.append(point)
    
    hull.append(left)
    find_hull(upper_points, left, right, hull)
    hull.append(right)
    find_hull(lower_points, right, left, hull)
    
    # Ordenar los puntos del hull en sentido horario
    center = (sum(p[0] for p in hull)/len(hull), sum(p[1] for p in hull)/len(hull))
    hull.sort(key=lambda p: math.atan2(p[1]-center[1], p[0]-center[0]))
    
    return hull

# 4. Algoritmo de Chan
def chan_algorithm(points):
    def convex_hull_graham(points):
        # Versión simplificada de Graham Scan para usar en Chan
        n = len(points)
        if n < 3:
            return points
        
        pivot = min(points, key=lambda x: (x[1], x[0]))
        
        def angle_distance(p):
            if p == pivot:
                return (0, 0)
            dx = p[0] - pivot[0]
            dy = p[1] - pivot[1]
            angle = math.atan2(dy, dx)
            dist = dx*dx + dy*dy
            return (angle, dist)
        
        sorted_points = sorted(points, key=angle_distance)
        hull = [pivot, sorted_points[0]]
        
        for p in sorted_points[1:]:
            while len(hull) > 1 and orientation(hull[-2], hull[-1], p) != 2:
                hull.pop()
            hull.append(p)
        
        return hull
    
    n = len(points)
    if n <= 5:
        return convex_hull_graham(points)
    
    # Parámetro m (número de subconjuntos)
    m = min(5, n)  # Podría ajustarse dinámicamente
    
    # Dividir los puntos en m subconjuntos
    subsets = [points[i::m] for i in range(m)]
    
    # Calcular el convex hull para cada subconjunto
    sub_hulls = [convex_hull_graham(subset) for subset in subsets]
    
    # Aplicar Jarvis March sobre los puntos de los sub-hulls
    # Encontrar el punto con la y más baja
    first_point = min((p for hull in sub_hulls for p in hull), key=lambda x: (x[1], x[0]))
    hull = [first_point]
    
    for _ in range(m):
        next_point = None
        for sub_hull in sub_hulls:
            for candidate in sub_hull:
                if candidate == hull[-1]:
                    continue
                if next_point is None:
                    next_point = candidate
                else:
                    o = orientation(hull[-1], next_point, candidate)
                    if o == 2 or (o == 0 and 
                                 ((candidate[0] - hull[-1][0])**2 + (candidate[1] - hull[-1][1])**2 > 
                                  (next_point[0] - hull[-1][0])**2 + (next_point[1] - hull[-1][1])**2)):
                        next_point = candidate
        if next_point == first_point:
            break
        hull.append(next_point)
    
    return hull

# Función para graficar los resultados
def plot_results(points, hull, title):
    plt.figure(figsize=(8, 6))
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    plt.scatter(x, y, color='blue', label='Puntos')
    
    if hull:
        hull.append(hull[0])  # Cerrar el polígono
        hx = [p[0] for p in hull]
        hy = [p[1] for p in hull]
        plt.plot(hx, hy, color='red', marker='o', linestyle='-', linewidth=2, label='Envoltura convexa')
    
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.show()

# Ejecutar y comparar los algoritmos
algorithms = {
    "Jarvis March": jarvis_march,
    "Graham Scan": graham_scan,
    "QuickHull": quickhull,
    "Chan": chan_algorithm
}

for name, algorithm in algorithms.items():
    start_time = time.time()
    convex_hull = algorithm(points.copy())
    end_time = time.time()
    print(f"{name} encontró {len(convex_hull)} puntos en la envolvente convexa. Tiempo: {end_time - start_time:.4f} segundos")
    plot_results(points, convex_hull.copy(), f"{name} - Envoltura Convexa")