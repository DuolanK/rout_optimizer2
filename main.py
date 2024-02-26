import math

# Функция для вычисления расстояния между двумя точками на плоскости
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2['from']
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Функция для нахождения расстояний между каждым курьером и всеми заказами
def find_courier_order_distances(orders, couriers):
    courier_order_distances = []

    # Цикл по каждому курьеру
    for courier_id, courier_coordinates in couriers.items():
        distances = []

        # Цикл по каждому заказу
        for order_id, order_coordinates in orders.items():
            distance = calculate_distance(courier_coordinates, order_coordinates)
            distances.append((order_id, distance))

        # Сортируем расстояния от курьера до заказов по возрастанию
        distances.sort(key=lambda x: x[1])

        assigned_orders = []

        # Выбираем один заказ с минимальным расстоянием для каждого курьера
        for order_id, distance in distances:
            assigned_orders.append((order_id, distance))
            if len(assigned_orders) == 1:
                del orders[order_id]  # Убираем уже назначенный заказ
                break  # Берем только один заказ для курьера

        courier_order_distances.append((courier_id, assigned_orders))

    # Сортируем курьеров по минимальному пути к первому заказу
    courier_order_distances.sort(key=lambda x: x[1][0][1])

    return courier_order_distances

# Листы:
orders = {
    'Order1': {'from': (56.7500, 37.6200), 'to': (56.7150, 37.6250), 'price': 10},
    'Order2': {'from': (55.7412, 37.6156), 'to': (56.7150, 37.6250), 'price': 10},
    'Order3': {'from': (55.7522, 37.6221), 'to': (56.7150, 37.6250), 'price': 10},
    'Order4': {'from': (55.7450, 37.6180), 'to': (56.7150, 37.6250), 'price': 10}

}

couriers = {
    'Curier1': (56.7500, 37.6200),
    'Curier2': (56.7400, 37.6100),
    'Curier3': (56.7150, 37.6250),
    'Curier4': (56.7350, 37.6150),
}


courier_order_distances = find_courier_order_distances(orders, couriers)

# Выводим результат
for courier_id, assigned_orders in courier_order_distances:
    print(f"Courier {courier_id}:")
    for order_id, distance in assigned_orders:
        print(f"  Order {order_id}: {distance:.4f} units")