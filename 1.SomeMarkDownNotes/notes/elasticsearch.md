##记录elastic search优化的一些参数

cluster.name: es-test
node.name: "test-169-71"
 
node.master: false
node.data: true
 
index.store.type: niofs                                    读写文件方式
index.cache.field.type: soft                             缓存类型
 
bootstrap.mlockall: true                                 禁用swap
 
gateway.type: local                                        本地存储
 
gateway.recover_after_nodes: 3                           3个数据节点开始恢复
gateway.recover_after_time: 5m                          5分钟后开始恢复数据
 
gateway.expected_nodes: 4                                 4个es节点开始恢复
 
cluster.routing.allocation.node_initial_primaries_recoveries:8               并发恢复分片数
cluster.routing.allocation.node_concurrent_recoveries:2                        同时recovery并发数
 
indices.recovery.max_bytes_per_sec: 250mb                                    数据在节点间传输最大带宽
indices.recovery.concurrent_streams: 8                                         同时读取数据文件流线程
 
discovery.zen.ping.multicast.enabled: false                                        禁用多播
discovery.zen.ping.unicast.hosts:["192.168.169.51:9300", "192.168.169.52:9300"]
discovery.zen.fd.ping_interval: 10s                                             节点间存活检测间隔
discovery.zen.fd.ping_timeout: 120s                                               存活超时时间
discovery.zen.fd.ping_retries: 6                                                  存活超时重试次数
 
http.cors.enabled: true                                                           使用监控
index.analysis.analyzer.ik.type:"ik"                                               ik分词
 

thread pool setting
threadpool.index.type: fixed                                      写索引线程池类型
threadpool.index.size: 64                                       线程池大小（建议2~3倍cpu数）
threadpool.index.queue_size: 1000                                队列大小
 
threadpool.search.size: 64                                      搜索线程池大小
threadpool.search.type: fixed                                     搜索线程池类型
threadpool.search.queue_size: 1000                                队列大小
 
threadpool.get.type: fixed                                      取数据线程池类型
threadpool.get.size: 32                                          取数据线程池大小
threadpool.get.queue_size: 1000                                 队列大小
 
threadpool.bulk.type: fixed                                        批量请求线程池类型
threadpool.bulk.size: 32                                        批量请求线程池大小
threadpool.bulk.queue_size: 1000                                   队列大小
 
threadpool.flush.type: fixed                                       刷磁盘线程池类型
threadpool.flush.size: 32                                       刷磁盘线程池大小
threadpool.flush.queue_size: 1000                                  队列大小

indices.store.throttle.type: none                               写磁盘类型
indices.store.throttle.max_bytes_per_sec:500mb                    写磁盘最大带宽
 
index.merge.scheduler.max_thread_count: 8                       索引merge最大线程数
index.translog.flush_threshold_size:600MB                       刷新translog文件阀值

---

使用7台机器，每台3个shard，一共21个shards，replicas为0，这样索引创建的速度更快。
关闭swap，使用bulk操作，增大queue size的大小控制index的buffer大小，关闭translog等系统日志开关。

merge policy相关，segment多大开始合并，一次合并多少个segment，segment到一定大小就不参与合并了，merge的线程数等等。
每台机器用64G的内存。

---
flume的sink设置，8个source，12个sink，