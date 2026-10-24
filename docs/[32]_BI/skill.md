# Agent Skill 定义与开发指南

> 如何定义、创建和使用 Agent Skill

---

## 📋 什么是 Skill

**Skill** 是 Agent 的专用能力模块，提供特定领域的功能封装。

### 核心概念

| 概念 | 说明 |
|------|------|
| **Skill** | 一个独立的功能模块，完成特定任务 |
| **SKILL.md** | Skill 的元数据文件，定义能力、命令、用法 |
| **工具函数** | Skill 内部实现的具体功能代码 |
| **命令接口** | 用户调用 Skill 的方式（CLI/API/自然语言） |

### Skill 能做什么

- ✅ 领域知识查询（法律、医疗、金融）
- ✅ 专业任务执行（代码审查、文案检测）
- ✅ 外部服务集成（天气、邮件、日历）
- ✅ 数据处理转换（格式化、分析、可视化）

---

## 🏗️ Skill 结构

### 标准目录结构

```
skill-name/
├── SKILL.md              # ⭐ 必需 - Skill 元数据
├── README.md             # 推荐 - 详细文档
├── main.py               # 推荐 - 主程序入口
├── utils.py              # 可选 - 工具函数
├── config.py             # 可选 - 配置管理
├── requirements.txt      # 可选 - Python 依赖
└── examples/             # 可选 - 使用示例
```

### SKILL.md 标准格式

```markdown
# Skill Name

简短描述（一句话说明 Skill 做什么）

## Description

详细描述：
- 功能说明
- 适用场景
- 能力边界

## Commands

| Command | Description | Parameters |
|---------|-------------|------------|
| `/command <arg>` | 功能说明 | arg: 参数说明 |

## Usage

### Basic Usage

```bash
command argument
```

### Examples

```
示例 1
示例 2
```

## Implementation

技术实现说明：
- 使用的库/框架
- 核心算法
- 依赖服务

## Configuration

配置项说明：
- 环境变量
- 配置文件
- API Keys

## Limitations

使用限制：
- 不支持的场景
- 性能限制
- 注意事项

## Files

文件清单：
- main.py - 主程序
- utils.py - 工具函数
```

---

## 🛠️ 创建 Skill 步骤

### 步骤 1: 确定需求

明确 Skill 要解决的问题：
- 目标用户是谁？
- 解决什么痛点？
- 输入输出是什么？

### 步骤 2: 设计接口

设计用户如何调用：
- 命令行参数
- API 端点
- 自然语言命令

### 步骤 3: 实现功能

编写核心代码：
```python
# main.py
def main_function(input_data):
    # 核心逻辑
    return result
```

### 步骤 4: 编写 SKILL.md

填写元数据文件：
- 功能描述
- 命令列表
- 使用示例

### 步骤 5: 测试验证

测试各种场景：
- 正常输入
- 边界情况
- 错误处理

### 步骤 6: 文档完善

补充 README 和示例：
- 详细用法
- 常见问题
- 最佳实践

---

## 📖 使用方式

### 方式 1: 命令行调用

```bash
# 直接进入 skill 目录
cd skill-name
python3 main.py argument

# 或者添加 PATH
export PATH="$PATH:/path/to/skill-name"
main-command argument
```

### 方式 2: Python 导入

```python
from skill_name import main_function

result = main_function("input")
```

### 方式 3: MCP 集成 (Claude)

```python
# mcp_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Skill Name")

@mcp.tool()
def skill_function(arg: str) -> str:
    """Skill 功能描述"""
    return main_function(arg)
```

### 方式 4: HTTP API

```python
# api_server.py
from fastapi import FastAPI

app = FastAPI()

@app.post("/skill")
def skill_endpoint(request: Request):
    return main_function(request.data)
```

### 方式 5: 自然语言调用 (LLM)

配置 Function Calling：
```json
{
  "name": "skill_function",
  "parameters": {
    "type": "object",
    "properties": {
      "arg": {"type": "string"}
    }
  }
}
```

---

# 📚 示例：广告法检测 Skill

> 以 `advertising-law-checker` 为例，完整展示 Skill 开发流程

---

## 1. Skill 概述

**名称：** Advertising Law Checker

**功能：** 检测广告文案是否违反中国/美国广告法

**场景：**
- 广告文案审核
- 电商产品描述
- 社交媒体内容
- 法律咨询

---

## 2. 完整 SKILL.md

```markdown
# Advertising Law Checker

检测广告文案是否违反中国/美国广告法，提供法律条款解释和修改建议。

## Description

本 Skill 提供广告法合规检测功能：
- 检测中国广告法违规（9 大类）
- 检测美国 FTC 法规违规（6 大类）
- 提供法律条款解释
- 生成修改建议

适用场景：
- 广告发布前审核
- 电商文案合规检查
- 社交媒体内容审查
- 法律培训教育

## Commands

| Command | Description | Parameters |
|---------|-------------|------------|
| `/check-ad <text>` | 检测广告文案 | text: 广告文案，law_type: china/us/both |
| `/explain-ad <question>` | 解释法律条款 | question: 问题，law_type: china/us |
| `/quick-check <text>` | 快速检测 | text: 广告文案（自动识别法规） |

## Usage

### 命令行使用

```bash
# 检测中文广告
python3 ad_law_checker.py "本产品是最好的"

# 检测英文广告
python3 ad_law_checker.py "Miracle cure!" --us

# 查询法律
python3 ad_law_checker.py --explain "什么是绝对化用语"

# 交互模式
python3 ad_law_checker.py --interactive
```

### Python 导入

```python
from ad_law_checker import AdvertisingLawChecker, LawType

checker = AdvertisingLawChecker()
result = checker.analyze("本产品是最好的", LawType.CHINA)

print(f"风险等级：{result.risk_level}")
print(f"违规数：{len(result.violations)}")
```

### MCP 调用 (Claude)

配置后直接说：
```
检查这个广告："本产品是最好的"
解释什么是绝对化用语
```

### HTTP API

```bash
curl http://localhost:8000/check \
  -d '{"text": "本产品是最好的", "law_type": "china"}'
```

## Examples

### 示例 1: 检测绝对化用语

**输入：**
```
/check-ad "本产品是市场上最好的，销量第一"
```

**输出：**
```
📋 广告法合规检测报告
风险等级：HIGH
发现 2 处问题:
1. 绝对化用语：'最好'
2. 绝对化用语：'第一'
```

### 示例 2: 检测医疗违规

**输入：**
```
/check-ad "根治糖尿病，治愈率 100%"
```

**输出：**
```
📋 广告法合规检测报告
风险等级：HIGH
发现 3 处问题:
1. 医疗违规：'根治'
2. 医疗违规：'治愈率 100%'
3. 食品违规：'治疗'
```

### 示例 3: 查询法律条款

**输入：**
```
/explain-ad "什么是绝对化用语"
```

**输出：**
```
📋 绝对化用语
⚖️ 法律条款：《广告法》第九条
💰 处罚标准：20 万 -100 万元罚款
```

## Implementation

技术栈：
- Python 3.9+
- 无外部依赖（纯 Python 实现）

核心模块：
- `ad_law_checker.py` - 主检测引擎
- `china_law.py` - 中国广告法知识库
- `us_law.py` - 美国 FTC 法规知识库

检测流程：
1. 文本预处理
2. 关键词匹配
3. 违规分类
4. 生成建议
5. 输出报告

## Configuration

无需配置，开箱即用。

可选配置：
- 自定义违规词库（编辑 china_law.py/us_law.py）
- 调整风险阈值（修改 ad_law_checker.py）

## Limitations

- 仅供参考，不构成法律意见
- 需要人工审核重要文案
- 法规会更新，需定期维护词库
- 某些行业有特殊规定

## Files

```
advertising-law-checker/
├── SKILL.md              # 本文件
├── ad_law_checker.py     # 主检测引擎
├── china_law.py          # 中国广告法知识库
├── us_law.py             # 美国 FTC 法规
├── mcp_server.py         # MCP 服务器
├── api_server.py         # HTTP API 服务器
├── test_examples.py      # 测试示例
├── README.md             # 详细文档
└── MY_INTEGRATION.md     # 集成指南
```
```

---

## 3. 项目结构示例

```
advertising-law-checker/
│
├── 📄 SKILL.md              # ⭐ Skill 元数据
├── 📄 README.md             # 详细文档
├── 📄 QUICK_START.md        # 快速开始
├── 📄 INTEGRATION.md        # 集成指南
├── 📄 MY_INTEGRATION.md     # 我的集成方案
│
├── 🐍 ad_law_checker.py     # ⭐ 主检测引擎
├── 🐍 china_law.py          # 中国广告法知识库
├── 🐍 us_law.py             # 美国 FTC 法规
├── 🐍 mcp_server.py         # MCP 服务器
├── 🐍 api_server.py         # HTTP API 服务器
├── 🐍 test_examples.py      # 测试示例
│
├── 📁 skill/                # OpenClaw Skill 配置
│   └── SKILL.md
│
└── 📁 examples/             # 使用示例（可选）
```

---

## 4. 核心代码示例

### 主检测引擎 (ad_law_checker.py)

```python
#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class LawType(Enum):
    CHINA = "china"
    US = "us"
    BOTH = "both"

@dataclass
class Violation:
    law_type: str
    category: str
    text: str
    reason: str
    severity: str
    suggestion: str

@dataclass
class AnalysisResult:
    original_text: str
    violations: List[Violation]
    risk_level: str
    summary: str
    suggestions: List[str]

class AdvertisingLawChecker:
    def __init__(self):
        # 违规词库
        self.china_violations = {...}
        self.us_violations = {...}
    
    def analyze(self, text: str, law_type: LawType) -> AnalysisResult:
        violations = []
        
        # 检测中国法规
        if law_type in [LawType.CHINA, LawType.BOTH]:
            violations.extend(self.detect_china(text))
        
        # 检测美国法规
        if law_type in [LawType.US, LawType.BOTH]:
            violations.extend(self.detect_us(text))
        
        return AnalysisResult(
            original_text=text,
            violations=violations,
            risk_level=self.calc_risk(violations),
            summary=self.gen_summary(violations),
            suggestions=[v.suggestion for v in violations]
        )
```

### MCP 服务器 (mcp_server.py)

```python
from mcp.server.fastmcp import FastMCP
from ad_law_checker import AdvertisingLawChecker, LawType

mcp = FastMCP("Advertising Law Checker")
checker = AdvertisingLawChecker()

@mcp.tool()
def check_ad_copy(text: str, law_type: str = "both") -> str:
    """Check advertising copy for legal violations."""
    lt = LawType(law_type)
    result = checker.analyze(text, lt)
    return format_result(result)

@mcp.tool()
def explain_law(query: str, law_type: str = "china") -> str:
    """Explain advertising law clauses."""
    lt = LawType.CHINA if law_type == "china" else LawType.US
    return checker.explain_law(query, lt)
```

### HTTP API (api_server.py)

```python
from fastapi import FastAPI
from ad_law_checker import AdvertisingLawChecker, LawType

app = FastAPI()
checker = AdvertisingLawChecker()

@app.post("/check")
async def check_ad(text: str, law_type: str = "both"):
    result = checker.analyze(text, LawType(law_type))
    return {
        "risk_level": result.risk_level,
        "violations": result.violations,
        "suggestions": result.suggestions
    }

@app.post("/explain")
async def explain(query: str, law_type: str = "china"):
    return {"explanation": checker.explain_law(query, LawType(law_type))}
```

---

## 5. 使用示例

### 场景 1: 电商文案审核

```bash
# 输入
python3 ad_law_checker.py "本店产品全网最低价，100% 纯天然"

# 输出
风险等级：HIGH
违规：
1. 绝对化用语：'全网最低'
2. 绝对化用语：'100%'
3. 虚假宣传：'纯天然'
```

### 场景 2: 社交媒体内容

```bash
# 输入
python3 ad_law_checker.py "Miracle cure! #ad 100% effective" --us

# 输出
风险等级：HIGH
违规：
1. False Claims: 'Miracle cure'
2. False Claims: '100% effective'
3. Endorsement: '#ad' (需披露关系)
```

### 场景 3: 法律咨询

```bash
# 输入
python3 ad_law_checker.py --explain "医疗广告不能说什么"

# 输出
📋 医疗违规
⚖️ 《广告法》第十六条
💰 处罚：广告费用 3-5 倍罚款
```

---

## 6. 集成方式对比

| 方式 | 配置难度 | 适用场景 | 示例 |
|------|----------|----------|------|
| **命令行** | ⭐ | 快速测试 | `python3 main.py` |
| **Python 导入** | ⭐ | 本地脚本 | `from skill import func` |
| **MCP** | ⭐⭐⭐ | Claude Desktop | 自然语言调用 |
| **HTTP API** | ⭐⭐⭐ | 远程调用 | `curl /check` |
| **Function Calling** | ⭐⭐⭐ | LLM 集成 | OpenAI/Anthropic |

---

## 7. 最佳实践

### ✅ 推荐做法

1. **单一职责** - 一个 Skill 只做一件事
2. **清晰接口** - 命令简单易懂
3. **完善文档** - SKILL.md + README
4. **错误处理** - 友好的错误提示
5. **测试覆盖** - 覆盖主要场景

### ❌ 避免做法

1. **功能臃肿** - 一个 Skill 做太多事
2. **接口复杂** - 参数太多难记
3. **缺少文档** - 用户不知道怎么用
4. **无错误处理** - 崩溃无提示
5. **硬编码** - 配置写死在代码里

---

## 8. Skill 发布流程

1. **开发完成** - 功能测试通过
2. **编写文档** - SKILL.md + README
3. **添加示例** - 使用示例代码
4. **版本标记** - git tag v1.0.0
5. **发布到平台** - GitHub/技能市场
6. **收集反馈** - 持续改进

---

## 📎 附录：完整文件清单

### 广告法 Skill 文件

| 文件 | 行数 | 说明 |
|------|------|------|
| `SKILL.md` | 150 | Skill 元数据 |
| `ad_law_checker.py` | 450 | 主检测引擎 |
| `china_law.py` | 50 | 中国法规库 |
| `us_law.py` | 60 | 美国法规库 |
| `mcp_server.py` | 100 | MCP 服务器 |
| `api_server.py` | 180 | HTTP API |
| `README.md` | 200 | 详细文档 |
| `test_examples.py` | 100 | 测试示例 |

**总计：** 约 1,300 行代码

---

## 📞 总结

**Skill 开发要点：**

1. **明确需求** - 解决什么问题
2. **设计接口** - 如何调用
3. **实现功能** - 核心代码
4. **编写文档** - SKILL.md
5. **测试验证** - 各种场景
6. **集成部署** - MCP/API/导入

**广告法 Skill 展示了：**
- ✅ 完整的 Skill 结构
- ✅ 多种集成方式
- ✅ 详细的使用文档
- ✅ 实际的代码示例

---

**开始创建你的第一个 Skill 吧！** 🚀

*文档版本：1.0.0*
*最后更新：2026-04-05*
