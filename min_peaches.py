# -*- coding: utf-8 -*-
"""猴子分桃"""

def monkey_gets_peach():
	a, n = 6, 4
	while n > 0:
		a = a * 5 +1
		n -= 1
	return a

min_peaches = monkey_gets_peach()

print(min_peaches)
