import math

# Класс для представления точки на плоскости
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Класс для представления заказа
class Order:
    def __init__(self, order_id, from_point, to_point, price):
        self.order_id = order_id
        self.from_point = from_point
        self.to_point = to_point
        self.price = price

# Класс для представления курьера
class Courier:
    def __init__(self, courier_id, coordinates):
        self.courier_id = courier_id
        self.coordinates = coordinates

# Класс, представляющий службу доставки
class DeliveryService:
    def __init__(self, orders, couriers):
        # Преобразование данных о заказах в объекты класса Order
        self.orders = [Order(order_id, Point(order_data['from'][0], order_data['from'][1]),
                             Point(order_data['to'][0], order_data['to'][1]), order_data['price'])
                       for order_id, order_data in orders.items()]

        # Преобразование данных о курьерах в объекты класса Courier
        self.couriers = [Courier(courier_id, Point(coordinates[0], coordinates[1]))
                         for courier_id, coordinates in couriers.items()]

        # Дебаг для проверки количества заказов и курьеров
        if len(self.orders) < len(self.couriers):
            print("DEBUG: There are more couriers than orders.")
            # Обрезаем список курьеров по количеству заказов
            self.couriers = self.couriers[:len(self.orders)]
        elif len(self.orders) > len(self.couriers):
            print("DEBUG: There are more orders than couriers.")
            # Разбиваем список заказов на части по количеству курьеров
            self.split_orders()

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
            for order_list in self.orders:
                for order in order_list:
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
                    for order_list in self.orders:
                        self.orders[self.orders.index(order_list)] = [order for order in order_list if order.order_id != order_id]
                    break

            courier_order_distances.append((courier.courier_id, assigned_orders))

        # Сортировка курьеров по минимальному пути к первому заказу
        courier_order_distances.sort(key=lambda x: x[1][0][1])

        return courier_order_distances

    # Метод для разбиения списка заказов на части по количеству курьеров
    def split_orders(self):
        num_orders = len(self.orders)
        chunk_size = len(self.couriers)
        remainder = len(self.orders) % len(self.couriers)

        new_orders = []
        start_index = 0

        for i in range(len(self.couriers)):
            end_index = start_index + chunk_size + (1 if i < remainder else 0)
            new_orders.append(self.orders[start_index:end_index])
            start_index = end_index

        self.orders = new_orders

# Листы:
orders_data = {
    'Order1': {'from': (56.7500, 37.6200), 'to': (56.7150, 37.6250), 'price': 10},
    'Order2': {'from': (55.7412, 37.6156), 'to': (56.7150, 37.6250), 'price': 10},
    'Order3': {'from': (55.7522, 37.6221), 'to': (56.7150, 37.6250), 'price': 10},
    'Order4': {'from': (55.7450, 37.6180), 'to': (56.7150, 37.6250), 'price': 10},
    'Order5': {'from': (55.7450, 37.6180), 'to': (56.7150, 37.6250), 'price': 10},
    'Order6': {'from': (55.7450, 37.6180), 'to': (56.7150, 37.6250), 'price': 10}
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
for courier_id, assigned_orders in courier_order_distances:
    print(f"Courier {courier_id}:")
    for order_id, distance in assigned_orders:
        print(f"  Order {order_id}: {distance:.4f} units")

# Вывод не назначенных заказов
print("Unassigned Orders:")
for order_list in delivery_service.orders:
    for order in order_list:
        print(f"  Order {order.order_id}")