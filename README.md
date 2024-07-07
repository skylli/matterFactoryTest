# matterFactoryTest

## 打包
```
 pyinstaller --name matterTester --onefile --copy-metadata readchar "src/main.py"
 ```
## 使用说明
```
└── matterTester
    ├── config
    │   ├── chip-tool
    │   └── config.json 
    └── matterTester   // 产测执行文件
```

### 配置文件
```json
{
    "device_name": "81919",    // 产品型号
    "ssid": "ssid",                 // 测试用到的 wifi， 注意测试电脑必须接到这个路由下
    "password": "pwd",              // 路由密码
    "chip_tool": "config/chip-tool", // 不要改动
    "debug": false,                 // 不要改动
    "type": "onoff"                 // 目前不变.
}
```

### 运行测试
```
./matterTester config/config.json
```