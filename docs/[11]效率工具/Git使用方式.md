## Git使用指南
- 本地仓库：
  - 版本库又叫仓库，repository，一个目录。Git管理里面所有的文件，每个文件都可以修改，删除，git追踪历史。
- 本地仓库建立：
  - 新建文件夹，进入该目录
  - 将该文件夹初始化为仓库，git init，并生成一个隐藏的文件夹 .git。
- 本地仓库修改和创建文件：
  - 工作区：目录下可见文件，就是工作区；
  - 暂存区：add操作后将文件放入到暂存区，commit操作将暂存区中文件放入到仓库；
  - 状态查看：使用git status查看工作区和暂存区状态；
- 远程仓库：
Github与gitlab的区别，github是开源仓库，gitlab是企业版私有仓库。
关联本地仓库和远程仓库：
- http方式： git remote add origin , http://github.com/username
- ssh方式：git remote add origin, git@github.com:username/
- 推送方式：git push origin master
分支管理：gitlab上默认分支为master
- 创建分支：git branch name
- 切换分支：git checkout name
- 合并分支：git merge name
- 删除分支：git branch -d name
SSH免密登录：
- 进入ssh文件位置：~/.ssh
- 生成私钥和公钥：ssh_keygen
- 添加ssh_key
常用命令：
1. git clone：由远程仓库添加到本地仓库；
2. git init：创建新的仓库；
3. git add：将修改文件添加到暂存区；
4. git commit : 将暂存区的文件同步到仓库中；
5. git push： 同步到远程仓库； 
6. git reset -hark commit id：版本重置；
7. git fetch：从远程代码仓库同步到本地仓库；
8. git pull: 从远程代码仓库同步代码到本地仓库，相当于git fetch + git merge;