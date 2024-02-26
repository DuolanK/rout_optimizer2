import math

# Класс представления точки на плоскости
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Класс  заказа
class Order:
    def __init__(self, order_id, from_point, to_point, price):
        self.order_id = order_id
        self.from_point = from_point
        self.to_point = to_point
        self.price = price

# Класс  курьера
class Courier:
    def __init__(self, courier_id, coordinates):
        self.courier_id = courier_id
        self.coordinates = coordinates

# Класс сервиса
class DeliveryService:
    def __init__(self, orders, couriers):
        # Преобразование данных о заказах в объекты класса Order
        self.orders = [Order(order_id, Point(order_data['from'][0], order_data['from'][1]),
                             Point(order_data['to'][0], order_data['to'][1]), order_data['price'])
                       for order_id, order_data in orders.items()]

        # Преобразование данных о курьерах в объекты класса Courier
        self.couriers = [Courier(courier_id, Point(coordinates[0], coordinates[1]))
                         for courier_id, coordinates in couriers.items()]

        # Добавление дебага для проверки количества заказов и курьеров
        if len(self.orders) < len(self.couriers):
            print("DEBUG: There are more couriers than orders.")
        elif len(self.orders) > len(self.couriers):
            print("DEBUG: There are more orders than couriers.")

    # Метод для вычисления расстояния между двумя точками
    def calculate_distance(self, point1, point2):
        return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)

    def find_courier_order_distances(self):
        courier_order_distances = []
        assigned_couriers = set()

        # Цикл по каждому заказу
        for order in self.orders:
            distances = []

            # Цикл по каждому курьеру, исключая уже назначенных
            for courier in [c for c in self.couriers if c.courier_id not in assigned_couriers]:
                distance = self.calculate_distance(courier.coordinates, order.from_point)
                distances.append((courier.courier_id, order.order_id, distance))

            if not distances:
                # Если нет доступных курьеров, прерываем цикл
                break

            # Сортировка расстояний от курьеров до текущего заказа по возрастанию
            distances.sort(key=lambda x: x[2])

            # Выбор первого курьера с минимальным расстоянием для текущего заказа
            courier_id, assigned_order_id, min_distance = distances[0]

            # Убираем уже назначенного курьера из списка доступных
            assigned_couriers.add(courier_id)

            # Убираем уже назначенный заказ из списка заказов
            self.orders = [o for o in self.orders if o.order_id != assigned_order_id]

            courier_order_distances.append((courier_id, assigned_order_id, min_distance))

        # Сортировка курьеров по минимальному пути к первому заказу
        courier_order_distances.sort(key=lambda x: x[2])

        return courier_order_distances

# Листы:
orders_data = {
    'Order1': {'from': (56.7500, 37.6200), 'to': (56.7150, 37.6250), 'price': 10},
    'Order2': {'from': (55.7412, 37.6156), 'to': (56.7150, 37.6250), 'price': 10},
    'Order3': {'from': (55.7522, 37.6221), 'to': (56.7150, 37.6250), 'price': 10},
    'Order4': {'from': (55.7450, 37.6180), 'to': (56.7150, 37.6250), 'price': 10},
    'Order5': {'from': (55.7450, 37.6180), 'to': (56.7150, 37.6250), 'price': 10}
}

couriers_data = {
    'Courier1': (56.7500, 37.6200),
    'Courier2': (56.7400, 37.6100),
    'Courier3': (56.7150, 37.6250),
    'Courier4': (56.7350, 37.6150),
}

# Создание объекта DeliveryService
delivery_service = DeliveryService(orders_data, couriers_data)
# Получение расстояний между курьерами и заказами
courier_order_distances = delivery_service.find_courier_order_distances()

# Вывод результата
for courier_id, assigned_order_id, distance in courier_order_distances:
    print(f"Courier {courier_id}:")
    print(f"  Order {assigned_order_id}: {distance:.4f} units")

# Вывод не назначенных заказов
print("Unassigned Orders:")
for order in delivery_service.orders:
    print(f"  Order {order.order_id}")