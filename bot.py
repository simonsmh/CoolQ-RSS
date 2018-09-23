import none
import getopt
import sys
import os
import json
from aiocqhttp.message import unescape
from aiocqhttp.exceptions import Error as CQHttpError

from rss import rss


def loadConfig():
    none.logger.info("Refreshing config...")
    try:
        with open(os.path.split(os.path.realpath(__file__))[0] + '/config.json', 'r') as f:
            config = json.loads(f.read())
            global URLS
            URLS = config['URLS']
            global QQGroup
            QQGroup = config['QQGroup']
            global FORMAT
            FORMAT = config['FORMAT']
        none.logger.info("Loaded config, %s, %s", URLS, QQGroup)
    except:
        none.logger.error(
            "Config load failed! Make sure config.json is present.")
        sys.exit(-1)


@none.on_command('echo')
async def _(session: none.CommandSession):
    await session.send(session.get_optional('message') or session.current_arg)


@none.scheduler.scheduled_job('cron', second='*/30')
async def _():
    none.logger.info("Running scheduled Job")
    loadConfig()

    bot = none.get_bot()
    tmp = rss().query(URLS)
    none.logger.info(tmp)
    for i, post in enumerate(tmp):
        text = FORMAT.format(post.title, ' '.join(post.summary.split()), post.link.replace('/Information/..', ''))
        try:
            await bot.send_group_msg(group_id=QQGroup, message=text)
        except CQHttpError:
            pass

if __name__ == '__main__':
    loadConfig()
    none.init()
    none.run(host='172.17.0.1', port=8080)
