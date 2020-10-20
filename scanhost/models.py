from django.db import models

"""
数据库模型相关的内容
服务器: 用户= 1:n (口诀: 一对多关系， 存在多的一端)
"""

# Create your models here.
class Server(models.Model):
    """服务器信息"""
    server_type_choice = (
        (0, 'PC服务器'),
        (1, '刀片机'),
        (2, '小型机')
    )
    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入')
    )
    # SmallIntegerField小整型， IntegerField整型， 占用内存空间不同，使用小整形为了节省加内存空间
    # choices=server_type_choice => 服务器类型是有选项：0-PC服务器， 1-刀片机， 2-小型机,
    # default=0, 用户没有选择/设置服务类类型。默认情况下设定为0(PC服务器)
    # verbose_name="服务器类型"后台管理时的中文显示
    server_type = models.SmallIntegerField(choices=server_type_choice,
                                           default=0,  # 默认情况下服务器类型是PC服务器
                                           verbose_name="服务器类型")

    created_by = models.CharField(choices=created_by_choice,
                                  max_length=32,
                                  default='auto',  # 默认情况下添加方式是自动录入的
                                  verbose_name="添加方式")
    IP = models.CharField(verbose_name='IP地址', max_length=30, default='')
    MAC = models.CharField(verbose_name='Mac地址', max_length=200, null=True, blank=True,default='')
    # null和blank有什么区别? null=, blank=
    """
    null 是针对数据库而言，如果 null=True, 表示数据库的该字段可以为空。
    blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填，比如 admin 界面下增加 model 一条记录的时候。直观的看到就是该字段不是粗体
    """
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='服务器型号')
    hostname = models.CharField(max_length=128, null=True, blank=True, verbose_name="主机名")
    # os_type: Linux/Windows
    os_type = models.CharField(verbose_name='操作系统类型', max_length=64, blank=True, null=True)
    # os_distribution: Redhat 8 , Centos 7, Windows10, Windows8
    os_distribution = models.CharField(verbose_name='发行商', max_length=64, blank=True, null=True)
    os_release = models.CharField(verbose_name='操作系统版本', max_length=64, blank=True, null=True)
    sn = models.CharField(verbose_name='资产标识', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.IP
    class Meta:
        # 设置数据库表的名称，默认情况下表名是APP名称_models类名
        db_table = 'servers'
        verbose_name = "服务器管理"
        verbose_name_plural = "服务器管理"
class User(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=30, default='root')
    password = models.CharField(verbose_name="密码", max_length=40, default='123')
    pkey = models.CharField(verbose_name="私钥", max_length=40, default='id_rsa')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name="所属服务器")

    def __str__(self):
        return self.username
    class Meta:
        # 设置数据库表的名称，默认情况下表名是APP名称_models类名
        db_table = 'users'
        verbose_name = "服务器用户管理"
        verbose_name_plural = "服务器用户管理"