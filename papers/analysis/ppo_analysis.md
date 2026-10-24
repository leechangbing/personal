# PPO (Proximal Policy Optimization) - 章节详细分析

> **论文信息**
> - 标题: Proximal Policy Optimization Algorithms
> - 作者: John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, Oleg Klimov (OpenAI)
> - 发布日期: 2017年7月 (arXiv:1707.06347v2, 2017年8月28日修订)
> - 原文链接: https://arxiv.org/abs/1707.06347

---

## 📋 目录

1. [摘要 (Abstract)](#1-摘要)
2. [引言 (Introduction)](#2-引言)
3. [背景：策略优化 (Background: Policy Optimization)](#3-背景策略优化)
4. [裁剪代理目标 (Clipped Surrogate Objective)](#4-裁剪代理目标)
5. [自适应 KL 惩罚系数 (Adaptive KL Penalty Coefficient)](#5-自适应-kl-惩罚系数)
6. [算法 (Algorithm)](#6-算法)
7. [实验 (Experiments)](#7-实验)
8. [结论 (Conclusion)](#8-结论)
9. [附录：超参数 (Appendix)](#9-附录)
10. [影响与后续发展（补充解读）](#10-影响与后续发展补充解读)

---

## 1. 摘要

### 核心要点

PPO 是一族新的**策略梯度 (Policy Gradient) 方法**，其核心思想是：

- 在"与环境交互采样数据"和"用随机梯度上升优化代理目标 (surrogate objective)"之间交替进行
- 标准策略梯度方法对每个数据样本只做一次梯度更新，而 PPO 提出了一种新颖的目标函数，**支持对同一批数据做多个 epoch 的 minibatch 更新**，显著提升样本利用率
- 继承了 TRPO (Trust Region Policy Optimization) 的部分优点，但**实现简单得多、更通用、且（经验上）样本复杂度更好**

### 实验结论

- 在模拟机器人运动 (MuJoCo) 和 Atari 游戏等基准任务上，PPO 优于其他在线策略梯度方法
- 在**样本复杂度、实现简单性、wall-time（实际运行耗时）**三者之间取得了有利的平衡

---

## 2. 引言

### 2.1 背景：当时主流方法的局限

论文回顾了当时（2017年）使用神经网络函数逼近的强化学习三大主流路线，并逐一指出其缺陷：

| 方法 | 代表 | 主要问题 |
|------|------|---------|
| Deep Q-learning | DQN [Mni+15] | 在许多简单问题上失败；理论理解不足；在连续控制任务上表现不佳 |
| 普通 (vanilla) 策略梯度 | A3C 等 [Mni+16] | 数据效率差、鲁棒性差 |
| 信赖域/自然策略梯度 | TRPO [Sch+15b] | 相对复杂；与含噪声的架构（如 dropout）或参数共享（策略与价值函数之间、或与辅助任务之间）不兼容 |

### 2.2 PPO 的目标

- 达到 TRPO 级别的**数据效率和可靠性能**，但只使用**一阶优化 (first-order optimization)**
- 核心创新：带**裁剪概率比 (clipped probability ratios)** 的新目标函数，构成对策略性能的悲观估计（即下界）
- 工作流程：从策略采样数据 → 在采样数据上做多轮优化，循环往复

### 2.3 实验结论预告

- 对比多种代理目标函数变体，**裁剪版本表现最好**
- 连续控制任务上优于所有对比算法
- Atari 上样本复杂度显著优于 A2C，与 ACER 相当但实现简单得多

---

## 3. 背景：策略优化

### 3.1 策略梯度方法 (Policy Gradient Methods)

策略梯度方法通过估计策略梯度并代入随机梯度上升算法。最常用的梯度估计器为：

$$
\hat{g} = \hat{\mathbb{E}}_t\left[\nabla_\theta \log \pi_\theta(a_t \mid s_t)\, \hat{A}_t\right]
$$

其中：

| 符号 | 含义 |
|------|------|
| $\pi_\theta$ | 参数为 $\theta$ 的随机策略 |
| $\hat{A}_t$ | 时刻 $t$ 的优势函数 (advantage function) 估计值 |
| $\hat{\mathbb{E}}_t[\ldots]$ | 在有限批次样本上的经验平均（算法在采样与优化之间交替） |

使用自动微分的实现方式是构造一个目标函数，其梯度即为上述策略梯度估计：

$$
L^{PG}(\theta) = \hat{\mathbb{E}}_t\left[\log \pi_\theta(a_t \mid s_t)\, \hat{A}_t\right]
$$

**关键问题**：虽然用同一批轨迹数据对这个损失做多步优化很诱人（提高样本效率），但这样做缺乏理论依据，且**经验上常常导致破坏性的大幅策略更新**（论文 6.1 节的实验证实，无约束版本的得分甚至低于随机策略）。

### 3.2 信赖域方法 (Trust Region Methods)

TRPO 在约束策略更新幅度的前提下最大化代理目标：

$$
\max_\theta \; \hat{\mathbb{E}}_t\left[\frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)}\, \hat{A}_t\right]
\quad \text{subject to} \quad
\hat{\mathbb{E}}_t\left[\mathrm{KL}\left[\pi_{\theta_{\text{old}}}(\cdot \mid s_t),\, \pi_\theta(\cdot \mid s_t)\right]\right] \le \delta
$$

其中 $\theta_{\text{old}}$ 是更新前的策略参数。该问题可通过**对目标做线性近似、对约束做二次近似后用共轭梯度法**高效近似求解。

理论上，TRPO 的推导其实建议使用**惩罚项而非硬约束**：

$$
\max_\theta \; \hat{\mathbb{E}}_t\left[\frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)}\, \hat{A}_t - \beta\, \mathrm{KL}\left[\pi_{\theta_{\text{old}}}(\cdot \mid s_t),\, \pi_\theta(\cdot \mid s_t)\right]\right]
$$

**为什么 TRPO 不用惩罚而用硬约束？** 因为很难选一个在所有问题上（甚至同一问题不同学习阶段）都表现好的固定 $\beta$。论文指出：实验表明直接用 SGD 优化固定 $\beta$ 的惩罚目标是不够的，还需要额外的修正——这正是 PPO 的动机。

---

## 4. 裁剪代理目标

### 4.1 概率比与 CPI 目标

定义**概率比 (probability ratio)**：

$$
r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)}, \quad \text{因此 } r(\theta_{\text{old}}) = 1
$$

TRPO 最大化的代理目标（上标 CPI 指 Conservative Policy Iteration [KL02]，该目标最早在此提出）：

$$
L^{CPI}(\theta) = \hat{\mathbb{E}}_t\left[\frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)}\, \hat{A}_t\right] = \hat{\mathbb{E}}_t\left[r_t(\theta)\, \hat{A}_t\right]
$$

**问题**：无约束地最大化 $L^{CPI}$ 会导致过大的策略更新，因此需要修改目标函数，惩罚使 $r_t(\theta)$ 偏离 1 的策略变化。

### 4.2 核心公式：Clipped Surrogate Objective

PPO 提出的主要目标函数：

$$
L^{CLIP}(\theta) = \hat{\mathbb{E}}_t\left[\min\left(r_t(\theta)\, \hat{A}_t,\; \mathrm{clip}\left(r_t(\theta),\, 1-\epsilon,\, 1+\epsilon\right)\, \hat{A}_t\right)\right]
$$

其中 $\epsilon$ 是超参数（论文取 $\epsilon = 0.2$）。逐项解释：

| 组成部分 | 含义 |
|---------|------|
| $r_t(\theta)\hat{A}_t$ | 即未裁剪的 $L^{CPI}$ 项 |
| $\mathrm{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t$ | 将概率比裁剪到 $[1-\epsilon, 1+\epsilon]$ 区间，**消除了把 $r_t$ 推出该区间的激励** |
| $\min(\cdot, \cdot)$ | 取两者的较小值，使最终目标是未裁剪目标的**下界（悲观界）** |

**设计直觉**：

- 只有当概率比的变化会**使目标变差**时才将其纳入；如果变化会让目标"改善"（超出裁剪区间），则忽略之
- $L^{CLIP}(\theta)$ 在 $\theta_{\text{old}}$ 附近（$r = 1$ 处）与 $L^{CPI}(\theta)$ **一阶等价**，但当 $\theta$ 远离 $\theta_{\text{old}}$ 时两者产生差异
- 论文 Figure 1 展示了单步项随 $r$ 变化的形状：
  - $\hat{A} > 0$ 时（好动作）：$r$ 超过 $1+\epsilon$ 后目标被削平，不再奖励"进一步加大该动作概率"
  - $\hat{A} < 0$ 时（坏动作）：$r$ 低于 $1-\epsilon$ 后目标被削平，惩罚封顶

### 4.3 Figure 2 的直观验证

论文在 Hopper-v1 的第一次策略更新上，沿 PPO 更新方向做线性插值，绘制各目标的变化曲线：

- $L^{CLIP}$ 是 $L^{CPI}$ 的下界，并对过大的策略更新施加惩罚
- 更新后策略与初始策略的 KL 散度约为 0.02，恰是 $L^{CLIP}$ 取最大值的点——说明裁剪目标确实把更新幅度控制在了"信赖区域"附近

---

## 5. 自适应 KL 惩罚系数

这是裁剪目标的**替代方案**（也可与之结合使用）：对 KL 散度加惩罚，并自适应调整惩罚系数使每次更新的 KL 接近目标值 $d_{targ}$。论文实验发现 KL 惩罚效果**不如裁剪目标**，但作为重要基线保留。

### 5.1 带惩罚的目标函数

$$
L^{KLPEN}(\theta) = \hat{\mathbb{E}}_t\left[\frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)}\, \hat{A}_t - \beta\, \mathrm{KL}\left[\pi_{\theta_{\text{old}}}(\cdot \mid s_t),\, \pi_\theta(\cdot \mid s_t)\right]\right]
$$

### 5.2 自适应更新规则

每次策略更新执行：

1. 用多轮 minibatch SGD 优化上述 $L^{KLPEN}$
2. 计算 $d = \hat{\mathbb{E}}_t\left[\mathrm{KL}\left[\pi_{\theta_{\text{old}}}(\cdot \mid s_t),\, \pi_\theta(\cdot \mid s_t)\right]\right]$
   - 若 $d < d_{targ}/1.5$：$\beta \leftarrow \beta / 2$（KL 太小 → 减弱惩罚，允许更大步长）
   - 若 $d > d_{targ} \times 1.5$：$\beta \leftarrow \beta \times 2$（KL 太大 → 加强惩罚，收缩步长）

更新后的 $\beta$ 用于下一次策略更新。

**备注**：

- 偶尔会出现 KL 与 $d_{targ}$ 显著偏离的更新，但很罕见，且 $\beta$ 会快速调整回来
- 系数 1.5 和 2 是启发式选取的，算法对它们不敏感
- $\beta$ 初值是超参数，但实际中不重要（算法会快速自适应调整）

---

## 6. 算法

### 6.1 组合目标函数

大多数降低方差的优势估计技术都需要一个学到的状态价值函数 $V(s)$（如广义优势估计 GAE [Sch+15a]，或 [Mni+16] 的有限时域估计器）。若策略与价值函数共享网络参数，损失函数需组合策略代理目标与价值函数误差项，并可加熵奖励 (entropy bonus) 保证充分探索 [Wil92; Mni+16]：

$$
L^{CLIP+VF+S}_t(\theta) = \hat{\mathbb{E}}_t\left[L^{CLIP}_t(\theta) - c_1 L^{VF}_t(\theta) + c_2 S[\pi_\theta](s_t)\right]
$$

| 符号 | 含义 |
|------|------|
| $c_1, c_2$ | 系数 |
| $S[\pi_\theta](s_t)$ | 熵奖励项 |
| $L^{VF}_t = (V_\theta(s_t) - V_t^{targ})^2$ | 价值函数的平方误差损失 |

### 6.2 优势估计：截断版 GAE

[Mni+16] 风格的实现让策略运行 $T$ 步（$T$ 远小于 episode 长度），用这批样本更新。其优势估计器为：

$$
\hat{A}_t = -V(s_t) + r_t + \gamma r_{t+1} + \cdots + \gamma^{T-t+1} r_{T-1} + \gamma^{T-t} V(s_T)
$$

推广为**截断版广义优势估计**（$\lambda = 1$ 时退化为上式）：

$$
\hat{A}_t = \delta_t + (\gamma\lambda)\delta_{t+1} + \cdots + (\gamma\lambda)^{T-t+1}\delta_{T-1}
$$

其中时序差分残差：

$$
\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)
$$

### 6.3 伪代码 (Algorithm 1: PPO, Actor-Critic Style)

```
for iteration = 1, 2, ... do
    for actor = 1, 2, ..., N do
        在环境中运行策略 π_θold，收集 T 个时间步的数据
        计算优势估计 Â_1, ..., Â_T
    end for
    优化代理损失 L（关于 θ），做 K 个 epoch，minibatch 大小 M ≤ NT
    θold ← θ
end for
```

**要点**：

- 每次迭代：$N$ 个并行 actor 各收集 $T$ 步数据，共 $NT$ 步
- 在这 $NT$ 步数据上构造代理损失，用 minibatch SGD（通常用 Adam）优化 $K$ 个 epoch
- 对自动微分实现而言，从普通策略梯度改为 PPO 只需把损失从 $L^{PG}$ 换成 $L^{CLIP}$ 或 $L^{KLPEN}$ 并做多步梯度上升——**改动只需几行代码**

---

## 7. 实验

### 7.1 代理目标的对比消融 (Section 6.1)

对比三种目标及其超参数：

| 变体 | 目标函数 |
|------|---------|
| 无裁剪无惩罚 | $L_t(\theta) = r_t(\theta)\hat{A}_t$ |
| 裁剪 | $L_t(\theta) = \min(r_t(\theta)\hat{A}_t,\, \mathrm{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t)$ |
| KL 惩罚（固定或自适应） | $L_t(\theta) = r_t(\theta)\hat{A}_t - \beta\, \mathrm{KL}[\pi_{\theta_{old}}, \pi_\theta]$ |

**实验设置**：

- 7 个 MuJoCo 机器人任务（HalfCheetah、Hopper、InvertedDoublePendulum、InvertedPendulum、Reacher、Swimmer、Walker2d，均为 -v1），每个训练 100 万步
- 策略网络：两层 64 单元 tanh MLP，输出高斯分布均值（标准差可变）；策略与价值函数**不共享参数**，不用熵奖励
- 每环境 3 个随机种子共 21 次运行；得分归一化（随机策略 = 0，最佳结果 = 1），以最后 100 个 episode 的平均总回报计分

**结果 (Table 1)**：

| 算法设置 | 平均归一化得分 |
|---------|--------------|
| 无裁剪无惩罚 | **-0.39**（HalfCheetah 上比随机策略还差） |
| Clipping, $\epsilon = 0.1$ | 0.76 |
| **Clipping, $\epsilon = 0.2$** | **0.82（最佳）** |
| Clipping, $\epsilon = 0.3$ | 0.70 |
| Adaptive KL, $d_{targ} = 0.003$ | 0.68 |
| Adaptive KL, $d_{targ} = 0.01$ | 0.74 |
| Adaptive KL, $d_{targ} = 0.03$ | 0.71 |
| Fixed KL, $\beta = 0.3$ | 0.62 |
| Fixed KL, $\beta = 1$ | 0.71 |
| Fixed KL, $\beta = 3$ | 0.72 |
| Fixed KL, $\beta = 10$ | 0.69 |

**结论**：裁剪目标（$\epsilon=0.2$）明显优于所有 KL 惩罚变体；无约束版本完全失败。论文还试过在 log 空间裁剪，效果没有更好。

### 7.2 连续控制上与其他算法的对比 (Section 6.2)

PPO（$\epsilon=0.2$ 裁剪版）对比：TRPO、交叉熵方法 (CEM)、自适应步长的 vanilla PG、A2C、A2C + Trust Region（均为调优过的实现）。

**结论**：PPO 在**几乎所有**连续控制环境上优于此前方法（Figure 3 的 7 个 MuJoCo 学习曲线）。

### 7.3 高维连续控制展示：3D 人形机器人 (Section 6.3)

三个 Roboschool 任务：

1. **RoboschoolHumanoid**：仅向前奔跑
2. **RoboschoolHumanoidFlagrun**：目标位置每 200 步（或到达后）随机改变，机器人需转向
3. **RoboschoolHumanoidFlagrunHarder**：机器人被立方体砸击，还需从倒地状态起身

展示了 PPO 在高维连续控制上的能力（学习曲线见 Figure 4）。同期工作 Heess et al. [Hee+17] 使用了 PPO 的**自适应 KL 变体**学习 3D 机器人运动策略。

### 7.4 Atari 领域对比 (Section 6.4)

在 Arcade Learning Environment (ALE) 上与调优过的 A2C、ACER 对比（使用与 [Mni+16] 相同的策略网络架构）。两种评分指标：

- 指标 (1)：整个训练期的平均每 episode 回报（偏爱学得快）
- 指标 (2)：最后 100 个 episode 的平均回报（偏爱最终性能）

**49 个游戏中各算法"获胜"局数 (Table 2)**：

| 评分指标 | A2C | ACER | PPO | 平局 |
|---------|-----|------|-----|------|
| (1) 全程平均回报 | 1 | 18 | **30** | 0 |
| (2) 最后 100 局平均回报 | 1 | **28** | 19 | 1 |

**结论**：PPO 样本效率显著优于 A2C；与 ACER 相当，但实现远比 ACER 简单（ACER 依赖经验回放等复杂机制）。

---

## 8. 结论

PPO 是一族使用**多 epoch 随机梯度上升**完成每次策略更新的策略优化方法：

- 具有信赖域方法的**稳定性和可靠性**
- **实现简单得多**：对 vanilla 策略梯度实现只需改动几行代码
- **适用场景更通用**：例如可以使用策略与价值函数的联合架构
- **整体性能更好**

---

## 9. 附录：超参数

### 9.1 MuJoCo 100 万步基准 (Table 3)

| 超参数 | 值 |
|--------|-----|
| Horizon ($T$) | 2048 |
| Adam 步长 | $3 \times 10^{-4}$ |
| Epoch 数 | 10 |
| Minibatch 大小 | 64 |
| 折扣因子 $\gamma$ | 0.99 |
| GAE 参数 $\lambda$ | 0.95 |

### 9.2 Roboschool 人形实验 (Table 4)

| 超参数 | 值 |
|--------|-----|
| Horizon ($T$) | 512 |
| Epoch 数 | 15 |
| Minibatch 大小 | 4096 |
| $\gamma$ / $\lambda$ | 0.99 / 0.95 |
| Actor 数 | 32（locomotion），128（flagrun） |
| 动作分布 log 标准差 | 线性退火 $-0.7 \to -1.6$ |
| Adam 步长 | 基于目标 KL 值自适应调整 |

### 9.3 Atari 实验 (Table 5)

| 超参数 | 值 |
|--------|-----|
| Horizon ($T$) | 128 |
| Adam 步长 | $2.5 \times 10^{-4} \times \alpha$ |
| Epoch 数 | 3 |
| Minibatch 大小 | $32 \times 8$ |
| Actor 数 | 8 |
| 裁剪参数 $\epsilon$ | $0.1 \times \alpha$ |
| 价值函数系数 $c_1$ | 1 |
| 熵系数 $c_2$ | 0.01 |

注：$\alpha$ 在学习过程中从 1 线性退火到 0。附录 B 另含全部 49 个 Atari 游戏的学习曲线与详细得分表（Table 6）。

---

## 10. 影响与后续发展（补充解读）

> ⚠️ **本节为基于论文之外背景知识的补充解读，并非论文原文内容。**

- **成为深度 RL 的默认算法**：PPO 凭借"简单 + 稳定 + 通用"的组合，在发布后迅速成为 on-policy 强化学习的事实标准基线，被 OpenAI Baselines、Stable-Baselines3 等主流框架作为核心算法实现。
- **RLHF / LLM 时代的关键角色**：PPO 是 InstructGPT（2022）和 ChatGPT 所采用的 RLHF（基于人类反馈的强化学习）训练阶段的核心算法——用大语言模型作为策略，用奖励模型打分构造优势信号，PPO 的 KL 惩罚思想（限制微调后模型不偏离参考模型太远）直接沿用到了 LLM 对齐中。这可以说是该论文影响最深远的"二次生命"。
- **后续改进与替代**：围绕 PPO 的实现细节有大量研究（如 Engstrom et al. 2020 的 "Implementation Matters"，Andrychowicz et al. 2021 的大规模消融）；在 LLM 场景中，GRPO（DeepSeekMath/R1）、DPO 及其变体等方法从不同角度简化或替代了 PPO 的 RLHF 流程，但 PPO 仍是理解这些工作的基础参照。
- **裁剪 vs KL 的历史轮回**：论文中"裁剪优于 KL 惩罚"的实验结论，在后来的大规模实践中被重新审视——许多 RLHF 框架实际采用 KL 惩罚（或两者结合），说明两种机制各有适用场景。
