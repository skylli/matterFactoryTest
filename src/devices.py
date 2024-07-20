import time,sys
from logger import logger as log
from matter_test import MatterTester as Mtester
from logger import print_green_bold_with_checkmark, print_red_bold_with_crossmark


def onoff_test(qrcode,conf):
    test_items = [
        ["蓝牙配网测试", "未测试"],
        ["onoff测试", "未测试"],
        ["恢复出厂测试", "未测试"]]
    
    debug = conf.get('debug')
    manual_code = ''
    def do_matter_test():
        manual_code = ''
        mdev = Mtester(qrcode, conf.get("chip_tool"), conf.get("ssid"), conf.get("password"))
        if False == mdev.pairing(debug):
            manual_code = mdev.manual_code
            print(manual_code)
            test_items[0][1] = "失败"
            return manual_code
        else:
            test_items[0][1] = "成功"
            
        manual_code = mdev.manual_code
        rets = []
        rets.append( mdev.onoff(False, debug) )
        rets.append( mdev.onoff(True, debug) )
        
        if False in rets:
            test_items[1][1] = "失败"
            return manual_code
        else:
            test_items[1][1] = "成功"
        
        if False == mdev.factory_rest(debug):
            test_items[2][1] = "失败"
        else:
            test_items[2][1] = "成功"
            
        return manual_code
    manual_code = do_matter_test()
    print(conf.get("device_name") + " 测试结果： ")
    suceesee_count = 0
    for item in test_items:
        ret_log = '\t' + item[0] + ": " + item[1]
        if "成功" == item[1]:
            print_green_bold_with_checkmark(ret_log)
            suceesee_count +=1
        else:
            print_red_bold_with_crossmark(ret_log)

    if len(test_items) == suceesee_count:
        ok_ret = "\t\t\t\t\t 设备 [" + manual_code +"] 测试: 成功"
        print_green_bold_with_checkmark(ok_ret)
    else:
        fault_ret = "\t\t\t\t\t 设备 [ " + manual_code +" ] 测试: 失败"
        print_red_bold_with_crossmark(fault_ret)

if __name__ == "__main__":
    import json
    def read_config(file_path):
        """Read the JSON config file and return the content."""
        try:
            with open(file_path, 'r') as file:
                config = json.load(file)
                return config
        except Exception as e:
            print(f"Error reading config file: {e}")
            sys.exit(1)
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_config.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    config = read_config(config_path)
    onoff_test("MT:QL8U4JP614Y4RK4Z120", config)