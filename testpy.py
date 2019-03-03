from redis import *
if __name__=="__main__":
    try:
        #创建StrictRedis对象，与redis服务器建⽴连接
        sr=StrictRedis(host="127.0.0.1",port=6379,password=123456)
        #获取键name的值
        result = sr.get('chen')
        #输出键的值，如果键不存在则返回None
        print(result)
    except Exception as e:
        print(e)