import numpy as np
from matplotlib import pyplot as plt
from program.python.utils import simulate_price_path,plot_price_value_positions

upper_band = 6700
lower_band = 5000
curr_price = 5662
# pre_price = 5615

portfolio_value = 120000
target_f = -(curr_price - upper_band) / (upper_band-lower_band)
target_f = max(0, min(1, target_f))

target_position_value = target_f * portfolio_value
print(target_position_value)