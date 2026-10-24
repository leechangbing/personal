import numpy as np
import matplotlib.pyplot as plt

# 设置随机种子以便复现
np.random.seed(42)

# 模拟价格路径：假设初始价格为initial_price，回归速度为mean_reversion
# 这里我们用均值回归过程模拟震荡（Ornstein-Uhlenbeck过程的离散形式）
def simulate_price_path(T, initial_price, mean_reversion, sigma):
    prices = [initial_price]
    for t in range(1, T):
        # OU过程：dP = mean_reversion*(mu - P) dt + sigma * dW
        # mu为长期均值，设为initial_price
        mu = initial_price
        dt = 1
        dW = np.random.normal(0, np.sqrt(dt))
        dP = mean_reversion * (mu - prices[-1]) * dt + sigma * dW
        new_price = round(prices[-1] + dP, 2)
        prices.append(new_price)
    return np.array(prices)


# 绘制价格、调仓点、净值、仓位比例
def plot_price_value_positions(prices, m30_prices, m60_prices, m90_prices, center, upper_band, lower_band, rebalance_points, portfolio_values, cashs, position_values):
    plt.figure(figsize=(14, 10))

    # 绘制价格变化
    plt.subplot(4, 1, 1)
    plt.plot(prices, label='Price')
    plt.plot(m30_prices, label='M30_prices')
    plt.plot(m60_prices, label='M60_prices')
    plt.plot(m90_prices, label='M90_prices')
    plt.axhline(center, color='black', linestyle='--', label='Center')
    plt.axhline(upper_band, color='red', linestyle='--', label='Upper Band (20%)')
    plt.axhline(lower_band, color='green', linestyle='--', label='Lower Band (20%)')
    for tp in rebalance_points:
        plt.axvline(tp, color='orange', linestyle='--', alpha=0.6)
    plt.title("Simulate Price Path")
    plt.legend(loc='upper right')

    # 绘制价值变化
    plt.subplot(4, 1, 2)
    plt.plot(portfolio_values, label='Portfolio Value')
    plt.plot(position_values, label='position_values')
    plt.plot(cashs, label='Cashs')
    plt.title('Portfolio Value Over Time')
    plt.legend(loc='upper right')

    # 绘制持仓比例变化
    plt.subplot(4, 1, 3)
    position_ratio = position_values / portfolio_values
    plt.plot(position_ratio, label='Position Ratio')
    plt.axhline(0, color='black', linestyle='--')
    plt.axhline(1, color='red', linestyle='--', alpha=0.5)
    plt.axhline(-1, color='green', linestyle='--', alpha=0.5)
    plt.title('Position Ratio Over Time')
    plt.legend(loc='upper right')


    # 绘制收益率变化
    plt.subplot(4, 1, 4)
    return_ratio = [x/portfolio_values[0] for x in portfolio_values]
    plt.plot(return_ratio, label='Return Ratio')
    # plt.axhline(0, color='black', linestyle='--')
    # plt.axhline(1, color='red', linestyle='--', alpha=0.5)
    # plt.axhline(-1, color='green', linestyle='--', alpha=0.5)
    plt.title('Return Ratio Over Time')
    plt.legend(loc='upper right')

    plt.tight_layout()
    plt.show()



# 为了简化，我们假设可以按当前价格即时成交，无滑点，无手续费
# 操作逻辑：当价格从中心向上突破5%则做空，向下突破5%则做多（均值回归思路）
# 但这里更贴合区间交易：在区间上下沿反向操作
# 具体：当价格上涨超过上沿-5%（即接近上沿）时减仓/做空；下跌超过下沿+5%时加仓/做多
# 不过题目说“震荡幅度大于5%则操作一次”，我们理解为：每当价格偏离中心超过5%，就进行一次反向交易

# 更清晰的策略：
# - 当价格从中心上涨超过+5%，我们认为超买，卖出（如果没空则开空，但这里我们只做多空对冲，用仓位比例）
# - 当价格从中心下跌超过-5%，我们认为超卖，买入
# 但结合20%震荡幅度，我们设定一个动态的仓位比例，比如用凯利公式的思想：根据胜率和赔率计算仓位
# 然而，在区间交易中，我们假设价格在[80,120]之间震荡，那么在100时无仓位，越偏离100仓位越重（反向）
# 这里我们采用一个简单的线性仓位比例：
# 仓位比例 = - (price - center) / (band_width * center)  但限制在[-1,1]
# 但题目要求“震荡幅度大于5%则操作一次”，所以我们在价格突破±5%时调整仓位

# 我们设计：当价格首次突破+5%或-5%时，我们建立反向仓位，仓位大小根据偏离程度（但不超过100%）
# 之后每当价格继续向边界移动，我们增加反向仓位（金字塔加仓），但为了简化，我们每次突破5%的整数倍就调整

# 这里我们采用另一种方式：每当价格变动超过5%（相对于前一次操作的价格），我们就调整仓位到目标仓位
# 目标仓位：f = - (price - center) / (0.2 * center)  # 线性，最大±1
# 但限制在[-1,1]