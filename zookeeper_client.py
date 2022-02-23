from time import sleep
from kazoo.client import KazooClient



zk = KazooClient(hosts="127.0.0.1:2181", read_only=False)


# watchers
@zk.DataWatch("/nginx.conf")
def nginx_event_cb(data, stat):
    # print(data, stat)
    pass


# connect to zookeeper
zk.start()

if not zk.exists("/nginx.conf"):
    # create data
    zk.create("/nginx.conf", b"hello world")
    print("create node....")
# get data

if zk.exists("/nginx.conf"):
    print("nginx.conf node is ok")
    data, stat = zk.get("/nginx.conf")
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
# update data
if zk.exists("/nginx.conf"):
    zk.set("/nginx.conf", b"update node") #max 1Mb
    data, stat = zk.get("/nginx.conf")
    # sleep(1)
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
# transaction
transaction = zk.transaction()
transaction.check("/nginx.conf", version=1)
transaction.set_data("/nginx.conf", b"third times")
transaction.set_data("/nginx.conf", b"four times")
result = transaction.commit()
if result:
    data, stat = zk.get("/nginx.conf")
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

# delete data
if zk.exists("/nginx.conf"):
    zk.delete("/nginx.conf", recursive=True)



# close connect
zk.stop()




