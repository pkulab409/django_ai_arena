# AI对战平台
基于django的AI对战游戏运行平台

## 功能：

### usr_sys 用户系统
1. 用户注册登录修改密码邮件验证
1. 个人主页：查看已上传代码

### match_sys 比赛系统
1. 比赛代码
    * 代码上传、保存功能
    * 上传阶段的代码合法性验证
    * 限制单用户单游戏最大上传代码数
1. pairmatch功能
    * 自己代码发起与他人代码的对战
    * 代码参与的所有比赛记录查询
    * 比赛记录查看、前端渲染与删除
1. 天梯系统：显示特定类型游戏所有代码战绩与积分

### external 比赛系统后端
1. 监视进程维护多进程比赛运行，支持超时中止与手动中止
1. 提供抽象层接口，调用ORM与不同比赛模块

## 待实现功能：

### usr_sys 用户系统
1. 用户个人资料修改、上传头像
1. 用户大厅，检索所有用户公开信息

### match_sys 比赛系统
1. 代码修改、更新信息、删除功能
1. 比赛邀请功能
1. 比赛记录保存为PNG/GIF/MP4

### external 比赛系统后端
1. 基于图与pairmatch的复杂比赛系统框架

### 其它
1. 多元素表格基于GET参数的部分显示、翻页功能