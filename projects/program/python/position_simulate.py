import numpy as np
from matplotlib import pyplot as plt
from program.python.utils import simulate_price_path,plot_price_value_positions

# 设置随机种子以便复现
np.random.seed(42)


# 模拟价格路径：假设初始价格为center，震荡幅度为20%
# 这里我们用均值回归过程模拟震荡（Ornstein-Uhlenbeck过程的离散形式）
center = 6300  # 价格带中心
lower_band = 5300 # 区间上界
upper_band = 6500 # 区间下界
band_width = (upper_band - lower_band) / center
prices = simulate_price_path(T=365,initial_price=center, mean_reversion=0.05, sigma=center/50)

# 初始化
threshold = 0.02  # 操作阈值5%
portfolio_value = 100000 # 组合价值
position_num =  round(10000/center,2) # 初始持仓数量
position_value = position_num * center # 初始持仓金额
position_rate = position_value/portfolio_value # 初始持仓比例
cash = portfolio_value-position_value # 初始现金
last_operation_price = center # 上一次操作价格

# 过程记录
rebalance_points = [] # 调仓点
cashs = [cash] # 现金变化
position_nums = [position_num]  # 持仓数量
position_rates = [position_rate] # 持仓比例
position_values = [position_value]  # 持仓金额
portfolio_values = [portfolio_value] # 投资组合价值

# 均值价格
m30_prices = [prices[0]]
m60_prices = [prices[0]]
m90_prices = [prices[0]]

for i in range(1, len(prices)):
    # 更新价格状态
    pre_price = prices[i-1]
    current_price = prices[i]
    m30_price = np.average(prices[max(0,i-30):i])
    m60_price = np.average(prices[max(0, i - 60):i])
    m90_price = np.average(prices[max(0, i - 90):i])
    m30_prices.append(m30_price)
    m60_prices.append(m60_price)
    m90_prices.append(m90_price)

    # 计算当前目标仓位比例（反向），限制在[-1,1]
    target_f = - (current_price - center) / (band_width * center)
    target_f = max(0, min(1, target_f))

    # 检查是否需要操作：如果当前价格与上一次操作的价格变动超过5%
    trade_num = 0
    trade_value = 0
    flag_1 = (abs(current_price - last_operation_price) / last_operation_price) > threshold
    flag_2 = (abs(current_price - pre_price) / pre_price) > threshold

    if flag_1 or flag_2:
        # 目标持仓市值 = target_f * portfolio_value
        target_position_value = target_f * portfolio_value
        # 目标持仓数量
        target_position_num = round(target_position_value / current_price,2)
        # 交易仓位数量
        trade_num = target_position_num - position_num
        trade_value = trade_num * current_price
        # 记录操作价格
        last_operation_price = current_price
        # 记录调仓点
        rebalance_points.append(i)
        # print(i, current_price, target_position_value, target_position_num, trade_value, trade_num)
    else:
        # 不操作，但更新总资产（用于记录）
        pass

    # 状态计算
    cash -= trade_value
    position_num += trade_num
    position_value = position_num * current_price
    portfolio_value = cash + position_value

    # 状态保存
    cashs.append(cash)
    position_nums.append(position_num)
    position_values.append(position_value)
    position_rates.append(position_value/portfolio_value)
    portfolio_values.append(portfolio_value)

# 转换为numpy数组
position_nums = np.array(position_nums)
position_values = np.array(position_values)
position_rates = np.array(position_rates)
cashs = np.array(cashs)
position_values = np.array(position_values)

# 计算收益率
final_return = (portfolio_values[-1] / portfolio_values[0] - 1) * 100
print
print(final_return)


# 画图
plot_price_value_positions(prices, m30_prices, m60_prices, m90_prices, center, upper_band, lower_band, rebalance_points, portfolio_values, cashs, position_values)






