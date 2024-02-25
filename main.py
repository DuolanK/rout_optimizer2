import math

# Класс точкии координат
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Класс заказа
class Order:
    def __init__(self, order_id, from_point, to_point, price):
        self.order_id = order_id
        self.from_point = from_point
        self.to_point = to_point
        self.price = price

# Класс курьера
class Courier:
    def __init__(self, courier_id, coordinates):
        self.courier_id = courier_id
        self.coordinates = coordinates

# Класс для вычисления расстояния между двумя точками
class DistanceCalculator:
    @staticmethod
    def calculate_distance(point1, point2):
        return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)

# Функция для нахождения минимальных расстояний между заказами и курьерами
def find_courier_order_distances(orders, couriers):
    courier_order_distances = []

    for order_id, order in orders.items():
        distances = []

        for courier_id, courier in couriers.items():
            distance = DistanceCalculator.calculate_distance(courier.coordinates, order.from_point)
            distances.append({
                'courier_id': courier_id,
                'distance': distance,
                'from_point': order.from_point,
                'to_point': order.to_point,
                'price': order.price
            })

        distances.sort(key=lambda x: x['distance'])

        assigned_couriers = distances[:1]  # Выбираем первого курьера с самым коротким расстоянием

        courier_order_distances.append({'order_id': order_id, 'assigned_couriers': assigned_couriers})

    courier_order_distances.sort(key=lambda x: x['assigned_couriers'][0]['distance'] if x['assigned_couriers'] else float('inf'))

    return courier_order_distances

# Входные данные для заказов и курьеров
orders_data = {
    'Order1': {'from': Point(56.7500, 37.6200), 'to': Point(56.7150, 37.6250), 'price': 10},
    'Order2': {'from': Point(55.7412, 37.6156), 'to': Point(56.7150, 37.6250), 'price': 10},
    'Order3': {'from': Point(55.7522, 37.6221), 'to': Point(56.7150, 37.6250), 'price': 10},
    'Order4': {'from': Point(55.7450, 37.6180), 'to': Point(56.7150, 37.6250), 'price': 10},
    'Order5': {'from': Point(55.7558, 37.6176), 'to': Point(56.7150, 37.6250), 'price': 10}
}

couriers_data = {
    'Courier1': Point(56.7500, 37.6200),
    'Courier2': Point(56.7400, 37.6100),
    'Courier3': Point(56.7150, 37.6250),
    'Courier4': Point(55.7558, 37.6176),
}

# Создание объектов заказов и курьеров
orders = {order_id: Order(order_id, data['from'], data['to'], data['price']) for order_id, data in orders_data.items()}
couriers = {courier_id: Courier(courier_id, coordinates) for courier_id, coordinates in couriers_data.items()}

# Выполнение первоначального распределения
courier_order_distances = find_courier_order_distances(orders, couriers)

# Проверка наличия нераспределенных заказов и обновление координат курьеров
unassigned_orders = [order_info['order_id'] for order_info in courier_order_distances if
                     not order_info['assigned_couriers']]
if unassigned_orders:
    # Создание нового списка курьеров с обновленными координатами
    new_couriers_data = {}

    for i, order_info in enumerate(courier_order_distances):
        assigned_couriers = order_info['assigned_couriers']
        if assigned_couriers:
            new_couriers_data[f'Courier{i}'] = Point(assigned_couriers[0]['to_point'].x,
                                                     assigned_couriers[0]['to_point'].y)

    # Добавление новых курьеров к существующему словарю курьеров
    couriers.update(
        {courier_id: Courier(courier_id, coordinates) for courier_id, coordinates in new_couriers_data.items()})

    # Повторное выполнение распределения для оставшихся нераспределенных заказов
    remaining_orders = {order_id: Order(order_id, data['from'], data['to'], data['price']) for order_id, data in
                        orders_data.items() if order_id in unassigned_orders}
    courier_order_distances = find_courier_order_distances(remaining_orders, couriers)

# Вывод конечного результата
for order_info in courier_order_distances:
    order_id = order_info['order_id']
    assigned_couriers = order_info['assigned_couriers']

    print(f"Заказ {order_id}:")

    if assigned_couriers:
        for courier_info in assigned_couriers:
            courier_id = courier_info['courier_id']
            distance = courier_info['distance']
            from_point = courier_info['from_point']
            to_point = courier_info['to_point']
            price = courier_info['price']
            print(
                f"  Курьер {courier_id}: Расстояние - {distance:.4f} единиц, От - {from_point.x}, {from_point.y}, До - {to_point.x}, {to_point.y}, Цена - {price}")
    else:
        print("  Нет назначенных курьеров.")

