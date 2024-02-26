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
        self.count = 0

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


    # Метод для вычисления расстояния между двумя точками
    def calculate_distance(self, point1, point2):
        return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)

    # Метод для нахождения расстояний между курьерами и заказами
    def find_courier_order_distances(self):
        courier_order_distances = []

        # Цикл по каждому курьеру
        for courier in self.couriers:
            distances = []

            # Цикл по каждому заказу
            for order in self.orders:
                distance = self.calculate_distance(courier.coordinates, order.from_point)
                distances.append((order.order_id, distance))

            # Сортировка расстояний от курьера до заказов по возрастанию
            distances.sort(key=lambda x: x[1])

            assigned_orders = []

            # Выбор одного заказа с минимальным расстоянием для каждого курьера
            for order_id, distance in distances:
                assigned_orders.append((order_id, distance))
                if len(assigned_orders) == 1:
                    # Убираем уже назначенный заказ из списка заказов
                    self.orders = [order for order in self.orders if order.order_id != order_id]
                    break

            courier_order_distances.append((courier.courier_id, assigned_orders))

        # Сортировка курьеров по минимальному пути к первому заказу
        courier_order_distances.sort(key=lambda x: x[1][0][1])

        return courier_order_distances

    def find_courier(self):
        courier_order_distances = []

        # Loop through each courier
        for courier in self.couriers:
            distances = []

            # Loop through each order
            for order in self.orders:
                distance = self.calculate_distance(courier.coordinates, order.from_point)
                distances.append((order.order_id, distance))

            # Sort distances from courier to orders in ascending order
            distances.sort(key=lambda x: x[1])

            assigned_orders = []

            # Choose one order with the minimum distance for each courier
            for order_id, distance in distances:
                assigned_orders.append((order_id, distance))
                self.orders = [order for order in self.orders if order.order_id != order_id]
                break  # Stop the loop after assigning one order

            courier_order_distances.append((courier.courier_id, assigned_orders))

        # Sort couriers by the minimum distance to the first assigned order
        courier_order_distances.sort(key=lambda x: x[1][0][1] if x[1] else float('inf'))

        return courier_order_distances

# Листы:
orders_data = {
    'Order1': {'from': (56.7500, 37.6200), 'to': (56.7150, 37.6250), 'price': 10},
    'Order2': {'from': (55.7412, 37.6156), 'to': (56.7150, 37.6250), 'price': 10},
    'Order3': {'from': (55.7522, 37.6221), 'to': (56.7150, 37.6250), 'price': 10},
    'Order4': {'from': (55.7450, 37.6180), 'to': (56.7150, 37.6250), 'price': 10},
    'Order5': {'from': (55.7412, 37.6156), 'to': (56.7150, 37.6250), 'price': 10},
    'Order6': {'from': (55.7522, 37.6221), 'to': (56.7150, 37.6250), 'price': 10},
    'Order7': {'from': (55.7450, 37.6180), 'to': (56.7150, 37.6250), 'price': 10},
    'Order8': {'from': (55.7450, 37.6180), 'to': (56.7150, 37.6250), 'price': 10}
}

couriers_data = {
    'Courier1': (56.7500, 37.6200),
    'Courier2': (56.7400, 37.6100),
    'Courier3': (56.7150, 37.6250),
    'Courier4': (56.7350, 37.6150),
}

# Создание объекта DeliveryService
delivery_service = DeliveryService(orders_data, couriers_data)


if len(delivery_service.orders) == len(delivery_service.couriers):
    courier_order_distances = delivery_service.find_courier_order_distances()

elif len(delivery_service.orders) < len(delivery_service.couriers):
    courier_order_distances = delivery_service.find_courier()

elif len(delivery_service.orders) > len(delivery_service.couriers):
    courier_order_distances = []  # Define the variable here
    # Перебираем не назначенные заказы
    for order in delivery_service.orders:
        # Находим курьера с минимальным счетчиком
        min_count_courier = min(delivery_service.couriers, key=lambda c: c.count)

        # Назначаем заказ этому курьеру и увеличиваем его счетчик
        courier_order_distances.append((min_count_courier.courier_id, [(order.order_id, delivery_service.calculate_distance(min_count_courier.coordinates, order.from_point))]))
        min_count_courier.count += 1

        # Убираем уже назначенный заказ из списка заказов
        delivery_service.orders = [o for o in delivery_service.orders if o.order_id != order.order_id]

# Вывод результата
for courier_id, assigned_orders in courier_order_distances:
    print(f"Courier {courier_id} (Count: {next(c.count for c in delivery_service.couriers if c.courier_id == courier_id)}):")
    for order_id, distance in assigned_orders:
        print(f"  Order {order_id}: {distance:.4f} units")

# Вывод не назначенных заказов
print("Unassigned Orders:")
for order in delivery_service.orders:
    print(f"  Order {order.order_id}")