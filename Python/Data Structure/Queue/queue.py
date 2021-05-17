from collections import deque
import time
from threading import Thread
class Queue:
	def __init__(self):
		self.buffer = deque()

	def enqueue(self, data):
		self.buffer.appendleft(data)

	def dequeue(self):
		return self.buffer.pop()

	def is_empty(self):
		return len(self.buffer)==0

	def size(self):
		return len(self.buffer)


class OrderSystem(Queue):
	def place_order(self, orders):
		for order in orders:
			self.enqueue(order)
			print(f"Placing Order for: {order}")
			print(f"Current Queue: {self.buffer}")
			time.sleep(0.5)
		# while len(orders)>0:
		# 	order = orders.pop()
		# 	self.enqueue(order)
		# 	print(f"Orders in Queue: {self.buffer}")
		# 	time.sleep(0.5)
			

	def serve_order(self):
		while self.size() > 0:
			print(f"Serving: {self.dequeue()}")
			time.sleep(2)

orders = ['pizza','samosa','pasta','biryani','burger']
foodorder = OrderSystem()

t1 = Thread(target=foodorder.place_order, args=(orders,))
t2 = Thread(target=foodorder.serve_order)

t1.start()
time.sleep(1)
t2.start()

t1.join()
t2.join()

# food_order_queue = Queue()

# def place_orders(orders):
#     for order in orders:
#         print("Placing order for:",order)
#         food_order_queue.enqueue(order)
#         time.sleep(0.5)


# def serve_orders():
#     time.sleep(1)
#     while True:
#         order = food_order_queue.dequeue()
#         print("Now serving: ",order)
#         time.sleep(2)

# if __name__ == '__main__':
#     orders = ['pizza','samosa','pasta','biryani','burger']
#     t1 = Thread(target=place_orders, args=(orders,))
#     t2 = Thread(target=serve_orders)

#     t1.start()
#     t2.start()


