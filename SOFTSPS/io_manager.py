#!/usr/bin/python
# -*- coding: ascii -*-
from time import sleep
from dp_holder import DPHolder

dp_holder = DPHolder()

i = 0
while True:
	sleep(.5)
	dp_holder.write_all_physical_values()
	
	i += 1
	if i == 20:
		i = 0
		dp_holder.update_all_to_db()


