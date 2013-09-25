# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-5
#

from flask.blueprints import Blueprint
from reddit.common.web.renderer import smart_render
from reddit.common.tools.reddit_cli import rc
from reddit.common.exceptions import FriendlyException
from reddit import error_codes

bp_reddites = Blueprint('reddites', __name__)


@bp_reddites.route('/sr/<subreddit>/new', methods=['GET'])
@smart_render()
def new(subreddit):
    try:
        subreddit = rc.get_subreddit(subreddit)
        subreddit.fullname
    except:
        # means this subreddit is not exists
        raise FriendlyException.fec(error_codes.SUBREDDIT_NOT_EXIST, subreddit)

    submissions = subreddit.get_new(limit=20)
    return [dict(title=s.title,
                author=s.author.name,
                short_link=s.short_link,
                created=s.created) for s in submissions]


@bp_reddites.route('/sr/<subreddit>/popular', methods=['GET'])
@smart_render()
def popular(subreddit):
    try:
        subreddit = rc.get_subreddit(subreddit)
        subreddit.fullname
    except:
        # means this subreddit is not exists
        raise FriendlyException.fec(error_codes.SUBREDDIT_NOT_EXIST, subreddit)

    submissions = subreddit.get_hot(limit=20)
    return [dict(title=s.title,
                author=s.author.name,
                short_link=s.short_link,
                created=s.created) for s in submissions]
