# openclaw安装和使用指南


## 部署指南

### 系统要求
- 操作系统: macOS/Linux/Windows
- Node.js 版本: v14.x 或更高
- npm 版本: v6.x 或更高
- 磁盘空间: 至少 500MB

### 安装步骤
1. 验证环境要求:
```bash
node -v
npm -v
```

2. 下载安装脚本:
```bash
curl -fsSL https://openclaw.bot/install.sh -o install.sh
```

3. 执行安装:
```bash
chmod +x install.sh
./install.sh
```

### 配置
安装完成后，需要配置 OpenClaw:
```bash
openclaw config set api-key <your-api-key>
openclaw config set environment production
```

### 验证安装
```bash
openclaw --version
openclaw status
```

### 常见问题
**Q: 安装过程中出现权限错误怎么办?**  
A: 请使用 `sudo` 执行安装命令，或修改 npm 的全局安装目录权限:
```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
```

**Q: 安装后命令未找到怎么办?**  
A: 请检查环境变量 PATH 是否包含 npm 全局安装目录:
```bash
echo $PATH
export PATH=$(npm config get prefix)/bin:$PATH
```
- node 
- npm



 # OpenClaw 安装和使用指南

## 安装方式

### 前置要求
- Node.js
- npm

### 安装命令
```bash
curl -fsSL https://openclaw.bot/install.sh | bash
```

## 使用方式

安装完成后，可通过以下命令：

- 查看帮助：`openclaw --help`
- 初始化项目：`openclaw init`
- 运行命令：`openclaw run`
- 查看版本：`openclaw --version`
- 启动服务：`openclaw start`
- 停止服务：`openclaw stop`
- 重启服务：`openclaw restart`
- 启动 TUI 界面：`openclaw tui`

## 环境检查

安装前建议验证环境:
```bash
node -v
npm -v
```

## 服务管理

### 启动服务
安装并配置完成后，可以使用以下命令启动 OpenClaw 服务:
```bash
openclaw start
```

### 停止服务
要停止正在运行的 OpenClaw 服务，可以使用以下命令:
```bash
openclaw stop
```

### 重启服务
要重启 OpenClaw 服务，可以使用以下命令:
```bash
openclaw restart
```

### 查看服务状态
要查看 OpenClaw 服务的当前状态，可以使用以下命令:
```bash
openclaw status
```

## TUI 界面

### 启动 TUI 界面
安装并启动服务后，可以通过以下命令启动 TUI 界面:
```bash
openclaw tui
```

TUI 界面提供了一个交互式终端界面，可以：
- 与 OpenClaw 助手进行对话
- 管理文件和项目
- 搜索信息、总结内容
- 设置提醒和定时任务
- 控制智能家居设备
- 发送邮件、管理通讯

### TUI 界面特性
- **持久化存储**：所有对话和文件操作都会持久化存储在 `/Users/bytedance/.openclaw/workspace/` 目录下
- **会话管理**：支持多会话管理，可以切换不同的工作区
- **命令行集成**：可以直接在 TUI 界面中执行命令行操作
- **插件系统**：支持插件扩展，可以安装和管理各种插件

### 退出 TUI 界面
要退出 TUI 界面，可以按 `Ctrl+C` 或输入 `exit` 命令。退出 TUI 界面不会关闭 Gateway 服务。
```bash
exit
```

## 安装验证

安装完成后，建议执行以下步骤验证安装:
1. 检查版本:
```bash
openclaw --version
```

2. 检查服务状态:
```bash
openclaw status
```

3. 尝试启动服务:
```bash
openclaw start
```

4. 检查服务是否正常运行:
```bash
openclaw status
```

5. 停止服务:
```bash
openclaw stop
```

## 开机自启配置

OpenClaw 支持开机自启配置，确保在系统重启后自动启动服务。以下是配置方法：

### macOS 配置
在 macOS 上，可以使用 `launchd` 配置开机自启：

1. 创建 `launchd` 配置文件：
```bash
mkdir -p ~/Library/LaunchAgents
nano ~/Library/LaunchAgents/com.openclaw.gateway.plist
```

2. 在打开的编辑器中添加以下内容：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.openclaw.gateway</string>
    
    <key>ProgramArguments</key>
    <array>
      <string>/opt/homebrew/bin/openclaw</string>
      <string>gateway</string>
      <string>start</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/Users/bytedance/.openclaw/logs/gateway.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/bytedance/.openclaw/logs/gateway.err</string>
  </dict>
</plist>
```

3. 保存并退出编辑器。

4. 加载配置文件：
```bash
launchctl load ~/Library/LaunchAgents/com.openclaw.gateway.plist
```

5. 启动服务：
```bash
launchctl start com.openclaw.gateway
```

### 验证配置
重启系统后验证服务是否自动启动：
```bash
openclaw status
```

### 停止开机自启
如果需要停止开机自启，可以使用以下命令：
```bash
launchctl stop com.openclaw.gateway
launchctl remove com.openclaw.gateway
```

### 数据持久化

OpenClaw 的数据持久化机制确保了即使在服务关闭或系统重启后，重要数据也不会丢失。以下是数据持久化的详细说明：

### 持久化存储位置
所有数据都存储在以下目录中：
```bash
/Users/bytedance/.openclaw/workspace/
```

### 主要存储文件
- **IDENTITY.md**: 存储 OpenClaw 的身份信息（例如："小明"）
- **USER.md**: 存储用户信息（例如："李白"）
- **MEMORY.md**: 长期记忆存储
- **memory/*.md**: 每日笔记存储

### 数据持久化特性
- **服务关闭**: 即使 Gateway 服务关闭，所有数据仍然保留在磁盘上。
- **终端退出**: 退出终端不会影响数据持久化。
- **系统重启**: 电脑重启后，数据仍然存在。
- **卸载重装**: 只要工作区目录未被删除，数据仍然保留。

### 数据丢失情况
数据只有在以下情况下才会丢失：
- **手动删除工作区目录**
- **格式化硬盘**
- **卸载时选择清除所有数据**

### 最佳实践
- **重要信息写入文件**: 为了确保长期记忆，建议将重要信息写入 `MEMORY.md` 或 `memory/` 目录下的文件。
- **避免手动删除**: 不要手动删除工作区目录或其中的文件，以免造成数据丢失。

通过这些机制，OpenClaw 确保了数据的持久化和安全性，即使在服务关闭或系统重启后，数据也不会丢失。👋

## 常见问题解答

### 如何防止电脑休眠导致的服务暂停？

电脑休眠会导致 OpenClaw 的部分功能暂停（如网络连接、定时任务等）。要防止休眠导致的服务暂停，可以使用以下方法：

**方法 1：使用 `caffeinate` 命令（macOS）**
```bash
# 防止休眠
caffeinate -d
```

**方法 2：修改系统设置**
1. 打开 "系统设置"
2. 进入 "电池" 或 "节能" 设置
3. 选择 "电源适配器" 选项卡
4. 勾选 "防止自动睡眠"

### 如何查看 OpenClaw 的日志？

OpenClaw 的日志默认存储在以下目录中：
```bash
/Users/bytedance/.openclaw/logs/
```

你可以使用以下命令查看日志：
```bash
# 查看主日志
cat /Users/bytedance/.openclaw/logs/main.log

# 查看 Gateway 服务日志（如果配置了开机自启）
cat /Users/bytedance/.openclaw/logs/gateway.log
cat /Users/bytedance/.openclaw/logs/gateway.err
```

### 如何手动备份 OpenClaw 的数据？

要手动备份 OpenClaw 的数据，可以将整个工作区目录复制到安全位置：
```bash
# 备份工作区
cp -R /Users/bytedance/.openclaw/workspace /path/to/backup/location/openclaw_workspace_backup_$(date +%Y%m%d)
```

### 如何恢复 OpenClaw 的数据？

要恢复 OpenClaw 的数据，可以将备份的工作区目录复制回原位置：
```bash
# 停止 Gateway 服务
openclaw gateway stop

# 备份当前工作区（可选）
cp -R /Users/bytedance/.openclaw/workspace /Users/bytedance/.openclaw/workspace_backup_$(date +%Y%m%d)

# 替换为备份的工作区
rm -rf /Users/bytedance/.openclaw/workspace
cp -R /path/to/backup/location/openclaw_workspace_backup /Users/bytedance/.openclaw/workspace

# 重启 Gateway 服务
openclaw gateway start
```

### 如何更新 OpenClaw 到最新版本？

要更新 OpenClaw 到最新版本，可以使用以下命令：
```bash
# 更新 OpenClaw
curl -fsSL https://openclaw.bot/install.sh | bash
```

更新完成后，建议验证安装：
```bash
openclaw --version
openclaw status
```
