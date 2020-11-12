import requests
import requests_ftp
from myftp import StcakQueue
requests_ftp.monkeypatch_session()#补丁，一个特定效果的适应性改变代码
url = 'ftp://*.*.*.*'#获取ftp路径
url_temp=url#用temp存储没转换之前的路径名称
url=url.encode('utf-8').decode('latin1')#将路径先编码再解码，解决路径中含有中文名问题
s = requests.Session()#实例化
res = s.list(url, auth=('', ''))#进行ftp连接
res.encoding = 'utf-8'
url=url_temp#将路径名赋为没编码之前路径，解决编码之后路径查找不到问题
print(res.text)#输出文件类型，文件名，日期等信息；是一个字符串
str=res.text.split('\r\n')#按换行符将字符串分割
queue=StcakQueue()#定义队列，存储每个文件信息
for i in range(0,len(str)-1):#将根目录下每个文件夹提取
    a=str[i].split()#按空格分割每行字符串
    b=a#获取字符串列表
    if b[0] == 'drwxr-xr-x':#是文件夹则压入队列
        if len(b) > 9:#整合文件名，由于文件名可能带空格，因此需要整合完整的文件名，第八个字符串之后为文件名
            name=b[8]
            for i in range(9,len(b)):
                name+=' '+b[i]
            queue.enqueue(name)#文件名压入队列
        else:
            queue.enqueue(b[8])
urls=StcakQueue()#存储ftp路径
urls.enqueue(url)#将初始路径入队
temp=StcakQueue()#用于更换队列
num=StcakQueue()#计数
while queue.is_empty() == True:#或队列此时为空，则代表这一层次的文件名被访问完
    url_1=urls.top();#获取队头文件名，即该层次的根路径
    url_1+='/'+queue.top()#根路径下加上需要访问的路径名，即下一层路径
    url_fag=url_1#用flag存储没转换之前的路径名称
    url_1 = url_1.encode('utf-8').decode('latin1')#解决路径中含有中文名
    queue.dequeue()#队列头访问完毕则出队
    s_1 = requests.Session()  # 实例化
    res_1 = s_1.list(url_1, auth=('', ''))  # 进行ftp连接
    url_1=url_fag#将路径名转换回去，即原来带有中文名的字符串
    res_1.encoding = 'utf-8'
    print(res_1.text)#输出该路径下所有文件信息
    str = res_1.text.split('\r\n')  # 按换行符将每个文件分割
    time = 0
    for i in range(0, len(str) - 1):  # 将根目录下每个文件夹提取
        a = str[i].split()
        b = a
        if b[0] == 'drwxr-xr-x':  # 是文件夹则压入队列
            time+=1#该层文件夹数量+1，用于获取上层目录下文件夹数量
            if len(b) > 9:  # 整合文件名
                name = b[8]
                for i in range(9, len(b)):
                    name += ' ' + b[i]
                temp.enqueue(name)
            else:
                temp.enqueue(b[8])
    if time != 0:#文件夹不为空则压入队列，文件夹数量和当层目录绑定
        num.enqueue(time)
        urls.enqueue(url_1)
    if queue.is_empty() == False:#若当层的文件被访问完则向下一层继续访问，直至目录队列为空
        urls.dequeue()
        if urls.is_empty() == False:
            break
        else:
            for x in range(0,num.top()):#若目录队列不为空，则将下一层类型为文件夹的压入下一层队列
                queue.enqueue(temp.top())
                temp.dequeue()
            num.dequeue()
