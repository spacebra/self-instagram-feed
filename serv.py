from bottle import route, redirect, post, run, request, hook
from instagram import client


client_id = 'eb700866470e4951a25c3199073a28aa'
client_secret = '067bea5ac5054529b3ac950b4e55e46d'
access_token = ''
user_id = 0

CONFIG = {
'client_id':client_id,
'client_secret':client_secret,
'redirect_uri':'http://127.0.0.1:8080/oauth_callback'
}
unauthenticated_api = client.InstagramAPI(**CONFIG)

@route('/')
def hello():
    url = unauthenticated_api.get_authorize_url(scope=["likes","comments"])
    return '<a href="%s">Instagram login</a>' % url

@route('/oauth_callback')
def on_callback():
    code = request.GET.get("code")

    access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)

    api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
    user_id = user_info['id']
    recent_media, next_ = api.user_recent_media(user_id=user_id, count=10)

    image_html = ''
    for media in recent_media:
        if media.type == 'image':
            image_html += '<a href="/p/'+media.id+'">'
            image_html += '<img src="'+media.images['thumbnail'].url+'"></img>'
            image_html += '</a>'

    return image_html

@route('/p/<media_id>')
def p(media_id):
    return media_id

run(host='127.0.0.1', port=8080, debug=True)
