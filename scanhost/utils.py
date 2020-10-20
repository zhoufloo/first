import nmap
import telnetlib
# regular expression
import re
import paramiko
def get_active_hosts(hosts):
    """获取指定网段存活的所有主机"""
    nm = nmap.PortScanner()
    result = nm.scan(hosts=hosts, arguments='-n -sP')
    # 返回当前局域网存活的主机IP
    hosts = nm.all_hosts()
    return hosts
def is_ssh_up(host, port=22, timeout=5)->bool:
    """判断指定IP的ssh端口是否开启"""
    try:
        # 实例化对象
        tn = telnetlib.Telnet(host=host, port=port, timeout=timeout)
        # read_until读取直到遇到了换行符或超时秒数。默认返回bytes类型,通过decode方法解码为字符串。
        # b'SSH-2.0-OpenSSH_7.8\r\n'(bytes-> string)SSH-2.0-OpenSSH_7.8
        tn_result = tn.read_until(b'\n', timeout=timeout).decode('utf-8')
        # 通过正则匹配SSH 寻找是否ssh服务开启
        # find is ssh in result
        ssh_result = re.search('SSH', tn_result)
    except:
        return False
    else:
        return True
def login_ssh_passwd(hostname, port=22,
                     username='root', pasword=None, command='hostname'):
    """通过密码登录主机执行指定的命令"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=port,
                   username=username, password=pasword)
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.read().decode('utf-8')