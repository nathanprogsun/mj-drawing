<div align="center">

<h1 align="center">ChatGPT-Midjourney</h1>

中文 | [English](./README_EN.md)

Free deployment of your private Midjourney web application（based on[Discord.py](https://github.com/Rapptz/discord.py)）


![index page](./docs/images/index.png)
![generate images](./docs/images/imagine.png)

</div>

## Support
- [x] discord `upload` 传图
- [x] midjourney `imagin` 想象
- [x] midjourney `upscale` 放大
- [x] midjourney `variation` 变幻

## Manual Deployment
### front-end(web) deploy

```shell
cd web
cp .env_example .env  # set mj-api url(REACT_APP_URL)
npm install
npm start             # default url: http://localhost:3000
```

### back-end(midjourney-api) deploy
```shell
cd midjourney-api

# set variables
cp .env_example .env  # set db and discord token
# install dependencies (for details, see pyproject.toml)
poetry install
# db migrations
dbmate up
# start the api service
python manage.py
# start the bot service
python bot.py
```
#### Parameter description
> DISCORD_BOT_TOKEN: [bot token](https://discord.com/developers/applications)


## More features
- [ ] support websocket return
- [ ] Drawing progress percentage
- [ ] Front-end page optimization: style selection/scene switching/picture download

## Acknowledgments
- [Discord.py](https://github.com/Rapptz/discord.py)
