import time
from logger import logger as log
from matter_test import MatterTester as Mtester

def onoff_test(qrcode,conf):
    test_items = [
        ["蓝牙配网测试", "未测试"],
        ["onoff测试", "未测试"],
        ["恢复出厂测试", "未测试"]]
    
    def do_matter_test():
        mdev = Mtester(qrcode, conf.get("chip_tool"), conf.get("ssid"), conf.get("password"))
        if False == mdev.pairing():
            test_items[0][1] = "失败"
            return False
        else:
            test_items[0][1] = "成功"

        rets = []
        rets.append( mdev.onoff(True) )
        time.sleep(1)
        rets.append( mdev.onoff(False) )
        time.sleep(1)
        rets.append( mdev.onoff(True) )
        
        if False in rets:
            test_items[1][1] = "失败"
        else:
            test_items[1][1] = "成功"
        
        if False == mdev.factory_rest():
            test_items[2][1] = "失败"
        else:
            test_items[2][1] = "成功"
    do_matter_test()
    print(conf.get("device_name") + " 测试结果： ")
    for item in test_items:
        print(item[0] + ": " + item[1])