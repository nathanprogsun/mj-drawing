<div align="center">

<h1 align="center">mj-drawing</h1>

中文 | [English](./README_EN.md)

免费部署你的私人 Midjourney 网页应用（基于[Discord.py](https://github.com/Rapptz/discord.py)开发）


![主界面](./docs/images/index.png)
![图片弹窗](./docs/images/imagine.png)

</div>

## 功能支持
- [x] discord `upload` 传图
- [x] midjourney `imagin` 想象
- [x] midjourney `upscale` 放大
- [x] midjourney `variation` 变幻

## 手动部署
### 前端(web)部署

```shell
cd web
cp .env_example .env  # 设置后端的接口地址(REACT_APP_URL)
npm install
npm start # 默认网页地址: http://localhost:3000
```

### 后端(midjourney-api)部署
```shell
cd midjourney-api

# 配置环境变量
cp .env_example .env  # 设置数据库与discord token
# 安装环境依赖(详情见 pyproject.toml)
poetry install
# 数据库迁移
dbmate up
# 启动 api服务
python manage.py
# 启动 bot服务
python bot.py
```
#### 配置参数说明
> DISCORD_BOT_TOKEN: [bot token](https://discord.com/developers/applications)


## 计划功能
- [ ] 支持websocket通信
- [ ] 绘图进度百分比
- [ ] 前端页面优化:风格选择/场景切换/图片下载
- [ ] docker一键部署

## 鸣谢
- [Discord.py](https://github.com/Rapptz/discord.py)
