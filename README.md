# Are u ok
> 东北大学学生防控信息统计系统自动化打卡脚本



## 目录

- [功能](#功能)
- [手动打卡步骤](#手动打卡步骤)
- [自动打卡步骤](#自动打卡步骤)
- [更新步骤](#更新步骤)
  - [手动打卡](#手动打卡)
  - [自动打卡](#自动打卡)
- [开源协议](#开源协议)



## 功能

1. 只需要账号和密码
2. 定时每天的北京时间10点到13点每隔一个小时打卡一次，防止服务器抽筋没打上
3. 支持打卡后邮件通知(非SSL)
4. 不需要下载本脚本或部署到服务器上



## 手动打卡步骤

系统要求: 已安装`python`

第一次使用:

1. 下载本项目 `git clone https://github.com/unbyte/are-u-ok`
2. 进入项目目录`cd are-u-ok`
3. 安装依赖`pip install -r requirements.txt`

日常打卡:

1. 执行`python ./main.py 学号 密码`



## 自动打卡步骤
1. Fork本项目

2. 前往Fork后的项目的`Settings`页面

3. 侧边栏点击`Secrets`

4. 通过`add a new secret`添加自己的如下信息（冒号前面的是需要添加的secret的`Name`，后面是对应的`Value`的含义）
  
    - `USER`: 学号
    - `PASS`: 密码

    <p align="center"><img src="https://i.loli.net/2020/02/24/RAPvJ4qu5hUIr2K.png"/></p>
    如果需要邮件通知，需要再设定以下secret:
    
- `MAIL_HOST`: SMTP服务器地址，带上端口，如`smtp.ym.163.com:25` **不支持SSL**
    - `MAIL_USER`: SMTP登陆用的用户名
    - `MAIL_PASS`: SMTP登陆用的密码
    - `MAIL_RECEIVER`:接收通知邮件的邮箱地址
    
    设置好之后应该是这样的:
    
    <p align="center"><img src="https://i.loli.net/2020/02/24/na1A3y2EJZQukCx.png"/></p>
    
5. **如果此前从未使用过`Github Action`，请进入fork后的项目的`Actions`页面，点击
`I understand my workflows, go ahead and run them`才能开启定时打卡**

6. 完成，以防万一还是需要关注邮件或班干部通知



## 更新步骤

### 手动打卡

直接删除已下载脚本并重复[手动打卡步骤](#手动打卡步骤)即可



### 自动打卡

- 重新Fork版 

    1. 删除Fork后的项目，步骤如下
       1. 进入Fork后的项目仓库，进入`Settings`页面
       2. 在最底下找到`Delete this repository`，点击验证后删除
    2. 重新fork本项目，接下来的步骤同[使用步骤](#使用步骤)

- Pull Request版(不需要重新设置secret)
    1. 点击
    
        <p align="center"><img src="https://user-images.githubusercontent.com/31768052/75086758-a9dedb80-552f-11ea-8de6-5cf8cc326005.png"/></p>
    
    2. 点击
    
        <p align="center"><img src="https://user-images.githubusercontent.com/31768052/75086760-ae0af900-552f-11ea-8ce5-9cd5476dbd50.png"/></p>
    
    3. 根据图片选择
    
        <p align="center"><img src="https://user-images.githubusercontent.com/31768052/75086765-b06d5300-552f-11ea-9628-9f5e26c319cc.png"/></p>
    
    4. 点击创建pull request
    
        <p align="center"><img src="https://user-images.githubusercontent.com/31768052/75086768-b2371680-552f-11ea-85ec-590826e475c3.png"/></p>
    
    5. 接着把绿色按钮按到没为止

## 开源协议

MIT License.
