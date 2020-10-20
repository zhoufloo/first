from django.shortcuts import render, HttpResponse

# 导入配置文件中的信息， 扫描的网段列表、执行的命令(自动采集的主机信息)

from djangoProjectDMDB.settings import  commands

# 导入扫描需要的函数

from .utils import get_active_hosts,is_ssh_up,login_ssh_passwd

# 导入数据库模型

from .models import  Server,User

# Create your views here.

# 路由-视图函数: /scanhosts/

def do_scanhosts(request):

    # 需要完成的需求3： 用户在网页上填写需要扫描的主机网段， 开始扫描。

    # 3-1).

    # 如果用户是GET请求，获取html页面， 可以看到表单， 代表用户像获取表单，填写扫描的网段.

    # 如果用户是POST请求， 代表用户填写了需要扫描的网段(1.1.1.0/24,2.2.2.0/24)

    if request.method == 'POST':

        # 3-2).如何获取到用户表单提交的要扫描的网段呢?

        # 获取表单POST方法提交过来的scanhosts里面的内容

        scanhosts = request.POST.get('scanhosts')

        # print(scanhosts)    # "1.1.1.0/24，2.2.2.0/24"

        scanhosts = scanhosts.split(',')

        # print("切割后要扫描的网段: ", scanhosts)



        # 存储所有扫描到的服务器对象

        servers = []

        # 依次扫描配置文件中的所有网段/所有主机

        for net_host in scanhosts:

            # 获取该网段存活的所有主机

            active_hosts = get_active_hosts(net_host)

            # 判断主机的ssh端口是否打开，如果打开就是Linux，可以采集主机信息，否则目前无法采集。

            for host in active_hosts:

                # 如果ssh端口存活， 则代表Linux系统，可以批量执行命令采集主机信息并自动保存到数据库中。

                if is_ssh_up(host):

                    # 通过ORM将将主机信息存储到数据库, 实例化对象，指定属性名

                    # 数据库中该IP已经存在了， 还需要重复存储么?不需要的。 还需要做判断。

                    # 如果该IP在数据库中已经存在， 则更新该主机的信息。 如果不存在，则增加该服务器信息

                    server = Server.objects.get(IP=host)

                    if not server:

                        # 新增一条服务器信息

                        server = Server(IP=host)

                    # 需要完成的功能1： 远程执行命令，采集到主机信息(MAC, hostname...)， 存储到数据库中.

                    # 等讲完面向对象的反射机制，再来写代码

                    """

                    commands = {

                        'hostname': 'hostname',

                        'os_type': 'uname',

                        'os_distribution': 'dmidecode -s system-manufacturer',

                        'os_release': "hostnamectl  | grep Operating  |  awk -F ':' '{print $2}'",

                        'MAC': 'cat /sys/class/net/`[^vtlsb]`*/address',

                    }

                    """

                    for attr, cmd in commands.items():

                        # print(attr, cmd)

                        # 命令执行的结果

                        result = login_ssh_passwd(hostname=host, username='root',

                                         pasword='Asimov', command=cmd)

                        # 通过setattr动态设置对象的属性

                        setattr(server, attr, result)

                    server.save() # 将服务器信息保存到数据库中

                    servers.append(server)

                # 如果ssh端口不存活，代表大概率不是Linux系统, 此处不能采集主机信息，则不做操作

                else:

                    pass

        # 需要完成的功能2: 扫描完成后， 返回用户扫描的所有主机信息并以表格方式展现在页面中。

        return  render(request, 'scanhosts.html', {'servers':servers})



    # 如果不是POST方法，那么就是GET方法

    else:

        return  render(request, 'scanhosts.html')