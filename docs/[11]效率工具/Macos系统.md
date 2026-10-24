## MacOS系统
文件系统: MacOS的文件系统和Linux十分相似，因为所有的Unix系统都支持文件系统层次化结构标准（hierarchical file system, hfs）
1. MacOS特有目录：
  1. Applications： 应用程序目录，默认是所有的GUI应用程序都安装在这里；
  2. Library：系统的数据文件、帮助文件、文档等；
  3. Network：网络节点存放目录；
  4. System：包含大多数系统配置和操作系统文件；
  5. Users：所有常规用户主目录的默认位置，每个用户有自己的单独目录；
  6. Volumes：文件系统挂载点存放目录；
  7. Cores：内核转储文件存放目录，当一个进程崩溃时，则会允许产生转储文件；
  8. Private：存放tmp、var、etc等链接目录的目标目录；
2. Unix传统目录：
  1. bin: 所有用户可以执行的二进制文件，传统unix命令的存放目录，例如ls、mv等；
  2. dev: 用于引用系统设备的设备文件，设备文件存放目录；
  3. sbin: 传统unix管理类命令存放目录，例如fdisk、ifconfig等；
  4. usr: 第三方程序安装目录；
    1. usr/bin: 系统安装命令，例如clang、git等；
    2. usr/sbin: 根系统不必要的系统管理命令，例如多数服务程序；
    3. usr/lib: 存放共享库（动态链接库）；
    4. user/local: 本地安装的程序；
  5. etc: 标准unix系统配置文件存放目录，例如用户密码文件/etc/passwd，此目录实际上指向/private/ect的链接；
  6. tmp: 临时文件存放目录，其权限是所有人任意读写，此目录实际指向/private/tmp的链接；
  7. var: 存放经常变化的文件，例如日志文件，此目录实际指向/private/var的链接；
  8. home: 
  9. opt： 用户级的安装程序；
3.2 环境变量
- 启动顺序：
  - /etc/profile: 全局配置，不管是哪个用户，登录时都会读取该文件，但不建议修改这个文件；
  - /etc/paths: 编辑path，将环境变量添加到paths文件中，一行一个路径；
  - /etc/bashrc：一般在这个文件中添加系统级环境变量，全局配置，bash shell执行时，不管是何种方式，都会读取此文件；
  - ~/.bash_profile：每一个运行bash shell的用户执行此文件，修改这个文件不需要重启即可生效；
  - ~/.bash_login
  - ~/.profile: 为系统的每个用户设置环境信息，当用户第一次登录的时候，该文件被执行，如果有对该文件的修改，需要重启才能生效；
  - ~/.bashrc：一般会在这个文件中添加系统级环境变量；
  - 编辑方式：export PATH=$PATH:<PATH1>:<PATH2>:<PATH3>…
  前面两个是系统级别，系统启动就会加载，后面几个是当前用户的环境变量；后面三个是按照顺序读取，如果.bash_profile存在，则后面的几个文件就会被忽略不读了；.bashrc没有上述限制，它是bash_shell打开时载入的；
- Mac配置文件加载顺序：
  - /etc/profile -> /etc/paths -> ~/.bash_profile -> ~/.bashrc -> ~/.zsh_profile -> ~/.zshrc
  - 在linux系统中默认shell是bash，如果安装有zsh则优先加载~/.zsh_profile和~/.zshrc;
  - /etc/profile: 全局配置，所有用户登录时都读取该文件；
  - /etc/paths：全局建议修改这个文件，一行一个路径；
  - /etc/bashrc：一般在这个文件中添加系统环境变量；
  - ~/.bash_profile: 单个用户的配置文件；
3.3 系统配置
1. 常用软件
  1. 搜狗输入法；
  2. Google chrome；
  3. 飞书；
  4. Seal: 链接内网；
  5. iTerm: 终端软件；
  6. oh-my-zsh：个性化主题；
  7. homebrew：包管理器；
2. 终端配置
  1. 打印所有shell: $cat /etc/shell;
  2. 查看当前shell: $echo $SHELL
  3. 查看脚本配置文件：$ls -a
  4. 对比: zsh完全兼容bash，iterm相比于terminal更容易配置，oh-my-zhs相比较于zsh更美观；
3. Python 
  1. 随着 os menterey 12.3移除了随系统自带的python，后面需要自己安装；
4. Homebrew 
  1. 使用Homebrew安装Apple没有预装的东西；例如：$brew install wget；
  2. Homebrew会将软件包安装到独立目录，并将其软连接到/usr/local；
  3. Homebrew不会将文件安装到它本身目录之外，所以可以将homebrew安装到任意位置；
  4. 创建自己的homebrew包；
  5. 完全基于git和ruby，自由修改的同时仍然可以撤销变更或与上游合并；
  6. Homebrew使MacOS更完整；