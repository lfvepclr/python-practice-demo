from bottle import route, run, request, get, post, delete, error
import hashlib
import reply
import receive

appId = "wx975998f2dc3a6c93"
appSecret = "876b37cdcf48d6dd0699d0a7b1631e71"


@get("/")
def hello():
    if len(request.query) == 4:
        return checksignature()
    return "Hello World!"


@post("/")
def message():

    recMsg = receive.parse_xml(request.body.read())
    if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
        toUser = recMsg.FromUserName
        fromUser = recMsg.ToUserName
        if recMsg.MsgType == 'text':
            content = "test"
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        if recMsg.MsgType == 'image':
            mediaId = recMsg.MediaId
            replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
            return replyMsg.send()
        else:
            return reply.Msg().send()
    else:
        print
        "暂且不处理"
        return "success"


@error(405)
def errorHandler(error):
    print(error)


def checksignature():
    query = request.query
    signature = query.signature
    token = "hellolofo"

    list = [token, query.timestamp, query.nonce]
    list.sort()
    hashcode = hashlib.sha1(''.join(list).encode("UTF-8")).hexdigest()
    print("handle/GET func: hashcode, signature: ", hashcode, signature)

    if hashcode == signature:
        return query.echostr
    else:
        return "Signature Valid Error"


if __name__ == "__main__":
    run(host='localhost', port=80, debug=True)
