
## Docker简介
历史：
2010年，dot cloud公司成立于美国旧金山。后来，dot cloud公司将自己的容器技术进行简化和标准化，并命名为docker。
2103年3月，docker之父Solomon Hykes决定将docker开源。
在容器技术之前常用虚拟机，代表为VMware，Openstack。虚拟机属于虚拟化技术，而 docker的容器技术是一种轻量级虚拟化技术。
概念：
Docker本身不是容器，而是创建容器的工具，是应用容器引擎。
-build, ship and run.
-build once, run anywhere.
镜像image：一个静态模板
容器container：启动镜像模板，产生一个容器()
仓库repository：保存各种镜像
Docker相关环境安装：本身支持gpu，若需要则在dicker基础上，再装nvidia-docker；
下载镜像：利用docker，pull指令下载该镜像
基础入门：
1. docker与VM的相同点与不同点；
2. 了解docker的基本概念与组件（docker daemon，docker client, registry镜像库，image镜像， container容器）。
3. docker命令实际操作，对docker及容器有感性的认识。
[图片]
Docker使用介绍：
- 环境准备：按照docker，docker-compose, 启动docker服务，熟悉和修改docker服务的参数。
- 熟悉基本命令：容器操作（run, rm, ps, stop, restart, exec, …），镜像操作（docker images/ build/ tag/ history/ pull/ push/ rmi,…）网络，volum。
- 镜像制作及上传下载：docker build，docker pull/push, docker, hub, registry, docker file。
- docker run运行容器以及docker-compose制作运行容器（docker run -p 80:80 nginx）
- 将docker应用
1. docker commit将运行中容器生成镜像
2. docker build使用dicker file生成镜像
3. 理解docker思想和方法，经docker运行
