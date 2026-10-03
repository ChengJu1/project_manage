### 1.原子操作
简单概念：一个操作要不然执行成功，要不然完全没有执行，不会执行到一半被其他操作插入:
- 常见的Redis原子命令有：`incre`, `decre`
- 或者使用Lua脚本，把多个命令交给Redis一次执行

### 2.分布式锁
当程序运行在多个进程或多台服务器上时，用一个大家都能访问的“公共锁”，保证同一时刻只有一个程序执行某段关键代码。

```text
服务器A ──┐
服务器B ──┼──→ Redis中的 order_lock
服务器C ──┘
```

```text
服务器A：获得锁，开始处理
服务器B：获取失败，等待或返回
服务器C：获取失败，等待或返回
```

### 3.Redis 加锁
常用SET NX EX（原子操作，同一段时间只有一个能加锁）
```Python
import uuid

lock_key = "lock:product:1001" #锁的名字
lock_value = str(uuid.uuid4()) #锁的唯一身份

acquired = redis_client.set(
    lock_key,
    lock_value,
    nx=True,
    ex=10 # 10秒后过期
)
```
lock_value唯一的原因：Redis里的锁是不是我创建的？如果是，才能删除
```text
1. 服务器A获得锁，有效期10秒
2. A处理太慢，锁自动过期
3. 服务器B获得了新的锁
4. A终于处理完，执行删除锁
5. A错误地删除了B的锁
```