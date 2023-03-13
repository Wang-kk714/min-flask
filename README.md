# conclusion

1. Unix/Linux 和 Windows下 - 多线程和多进程效率
2. GIL未释放时(做代码解释)无法并行 - 单核心
3. [GIL & CPython](https://juejin.cn/post/7007043202251390984)
3. GIL会在I/O等待释放，不需要在应用层控制。coroutine+异步效果不如直接多线程