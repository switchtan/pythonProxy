from sanic import Sanic ,response
from sanic.response import json
import urllib
from urllib.request import urlopen
import ssl
import urllib.request
import filetype
import redis
import base64
app = Sanic()
dict = {'www.n77888.com': 'http://www.champaignchinese.com', 'www.0008mu.com': 'http://www.0001688.com'
    , 'www.bismara22.com': 'http://www.iintern.com'
    ,'www.pk10kaijiang8.com':'https://www.canreachinternational.com'}

def replace_ment(resource):
    # replacement
    content = str(resource, 'utf-8', 'ignore')
    content = content.replace('越南', 'pk10计划网')
    content = content.replace('(champaignchinese.com)', 'pk10赛车最新开奖直播')
    content = content.replace('美国', '历史走势图')
    content = content.replace('中国', '最新走势预测')
    content = content.replace('香槟', 'pk10开奖直播')
    content = content.replace('华人', 'pk10赛车计划')
    content = content.replace('0001688', '0008mu')
    # www.bismara22.com
    content = content.replace('实习', '硕士博士申请')
    content = content.replace('学生', '申博学生')
    content = content.replace('I-internCareer', '申博|美国学生博士申请-')
    # www.bismara22.com end
    # https://www.canreachinternational.com/
    # 时时彩刷钱漏洞改单
    content = content.replace('加拿大', '时时彩')
    content = content.replace('四川', '漏洞改单')
    content = content.replace('凯瑞国际投资集团', '时时彩刷钱漏洞改单')
    content = content.replace('凯瑞', '重庆时时彩')
    content = content.replace('Can-Reach International', '重庆时时彩刷钱漏洞改单PK10')
    # https://www.canreachinternational.com end

    content = content.replace('</html>','<script type="text/javascript" src="//js.users.51.la/20032545.js"></script></html>')
    # replacement end
    resource = content
    return resource

@app.route("/<path:.*>")
@app.route('/<path:path>')
async def test(request,path):
    print('guava:'+request.path)
    host= request.headers['host']

    if host not in dict:
        return
    url = dict[host]
    content = None
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    if r.exists(url + request.path) is 0:
        # print('not match resource')
        # print(url + request.path)
        try:
            # resource = urllib.request.urlopen(url + request.path).read()
            # resource = requests.get(url + request.path)
            # https://blog.csdn.net/qq_25403205/article/details/81258327
            ssl._create_default_https_context = ssl._create_unverified_context
            resource = urllib.request.urlopen(url+ request.path).read()
            # print(response.read().decode('utf-8'))
            if request.path.find('.php')>-1 or request.path.find('.htm')>-1 or request.path.find('.html')>-1 or request.path=='/':
                resource = replace_ment(resource)
            else:
                resource = base64.b64encode(resource)
                content = resource

            r.set(url + request.path, resource, ex=60*60*24)
            # r.set(url + request.path,resource, ex=60*60*24)
        except Exception as e1:
            raise e1
            print(url + request.path)

    else:
        # print('match resource')
        content = r.get(url + request.path)
        # resource = base64.b64decode(resource)


    if request.path.find('.php')>-1 or request.path.find('.htm')>-1 or request.path.find('.html')>-1 or request.path=='/':
        # print("get html:"+request.path)
        # self.wfile.write(data.encode('utf-8'))
        # self.send_response(200)
        # self.send_header("Content-type", "text/html; charset=utf-8")
        # self.send_header("Content-Length", str(len(content)))
        # self.end_headers()
        # self.wfile.write(content.encode('utf-8'))
        return response.html(content)
    else:
        # print('getting:'+request.path)
        # self.send_response(200)
        # self.end_headers()
        # self.wfile.write(resource)
        content = base64.b64decode(content)
        # self.wfile.write(content)
        if request.path[-1]=='/':
            return response.json({'message': 'Hello world!'})
        if request.path.find('.css')>-1:
            return response.raw(content,content_type='text/css')

        if request.path.find('.js')>-1:
            return response.raw(content,content_type='application/javascript')
        kind =filetype.guess(content)
        print(kind.mime)
        return response.raw(content,content_type=kind.mime)
    # return response.text(url+':'+host)
#/<url:.*>
# app.add_route(test, '/<path:path>')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

