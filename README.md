# Are u ok
> 东北大学学生防控信息统计系统自动化打卡脚本

## 功能

1. 只需要账号和密码

2. 定时每天的北京时间10点到13点每隔一个小时打卡一次，防止服务器抽筋没打上

3. 支持打卡后邮件通知(非SSL)

4. 不需要下载本脚本或部署到服务器上

## 使用步骤
1. Fork本项目

2. 前往Fork后的项目的`Settings`页面

3. 侧边栏点击`Secrets`

4. 通过`add a new secret`添加自己的如下信息（冒号前面的是需要添加的secret的`Name`，后面是对应的`Value`的含义）
    
    - `USER`: 学号
    - `PASS`: 密码

    如果需要邮件通知，需要再设定以下secret:

    - `MAIL_HOST`: SMTP服务器地址，带上端口，如`smtp.ym.163.com:25` **不支持SSL**
    - `MAIL_USER`: SMTP登陆用的用户名
    - `MAIL_PASS`: SMTP登陆用的密码
    - `MAIL_RECEIVER`:接收通知邮件的邮箱地址

5. 完成，以防万一还是需要关注邮件或班干部通知

## 更新步骤
1. 重新输密码版    
    1. 删除Fork后的项目，步骤如下    
        1. 进入Fork后的项目仓库，进入`Settings`页面
        2. 在最底下找到`Delete this repository`，点击验证后删除
    2. 重新fork本项目，接下来的步骤同[使用步骤](#使用步骤)
2. 无需重新输入密码版
    1. 点击     
    ![pull_request](https://user-images.githubusercontent.com/31768052/75086758-a9dedb80-552f-11ea-8de6-5cf8cc326005.png)
    2. 点击     
    ![new_pull_request](https://user-images.githubusercontent.com/31768052/75086760-ae0af900-552f-11ea-8ce5-9cd5476dbd50.png)
    3. 根据图片选择    
    ![select](https://user-images.githubusercontent.com/31768052/75086765-b06d5300-552f-11ea-9628-9f5e26c319cc.png)
    4. 点击创建pull request     
    ![$JT(V~PT0%APNLGQS{%DIIG](https://user-images.githubusercontent.com/31768052/75086768-b2371680-552f-11ea-85ec-590826e475c3.png)
    5. 接着把绿色按钮按到没为止

## 开源协议

MIT License.
