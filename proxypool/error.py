# 异常模块
class ResourceDepletionError(Exception):  # 资源枯竭异常，如果从所有抓取网站都抓不到可用的代理资源，则抛出此异常

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已经枯竭')


class PoolEmptyError(Exception):  # 代理池空异常，如果代理池长时间为空，则抛出此异常。

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池是空的')
