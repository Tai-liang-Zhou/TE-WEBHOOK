# te-webhook 开发,编译,布署方式

# 所需安装的工具
- Git
- Docker

# 开发
- 编辑 vip/controller.py 档案
- 共有 4 个 Handler 对应到 4 个 Restful api，分别是
    - /urge_refund/list_all_order 催促退款-列出所有订单
    - /urge_refund/get_order_info 催促退款-列出订单详细资料
    - /urge_logistics/list_all_order 催促物流-列出所有订单
    - /urge_logistics/get_order_info 催促物流-列出订单详细资料

# 编译
- 切换到 docker 资料夹
- 执行 ./build.sh

# 布署
- 切换到 docker 资料夹
- 执行 ./run.sh dev.env [git版号7码]
- 范例：
```
# 手动输入tag启动范例
./run.sh dev.env c2a4982

# 自动选取目前tag的启动范例
./run.sh dev.env $(git rev-parse --short HEAD)
```

# 测试
```
curl -X POST -d '{"user_id":"0E2C2D3D11FB8502E8629830869B05CAD","msg_confirm_template":[],"msg_confirm_json":{},"text":"催促物流","cu":{},"task_info":{"vip_user_id":"001"}}' http://localhost:5008/urge_logistics/list_all_order
# 预期结果
{"status_code": 0, "msg_response": {"update": {"second_ask": "false", "order_length": 4, "order": {"order_list": [{"order_id": "16100567243327", "item_list": [{"item": "\u68d5\u8272\u9ad8\u5e2e\u82f1\u4f26\u590d\u53e4\u5546\u52a1\u76ae\u9774", "price": "338", "description": "\u6e05\u4ed3-\u4fa7\u6069ceen\u7537\u978b\u4e13\u573a\u5c3a\u780140"}], "total_price": "338"}, {"order_id": "16100567243328", "item_list": [{"item": "\u68d5\u8272\u9ad8\u5e2e\u82f1\u4f26\u590d\u53e4\u5546\u52a1\u76ae\u9774",
"price": "338", "description": "\u6e05\u4ed3-\u4fa7\u6069ceen\u7537\u978b\u4e13\u573a\u5c3a\u780140"}], "total_price": "338"}, {"order_id": "16100567243329", "item_list": [{"item": "\u68d5\u8272\u9ad8\u5e2e\u82f1\u4f26\u590d\u53e4\u5546\u52a1\u76ae\u9774", "price": "338", "description": "\u6e05\u4ed3-\u4fa7\u6069ceen\u7537\u978b\u4e13\u573a\u5c3a\u780140"}], "total_price": "338"}, {"order_id": "16100567243330", "item_list": [{"item":
"\u68d5\u8272\u9ad8\u5e2e\u82f1\u4f26\u590d\u53e4\u5546\u52a1\u76ae\u9774", "price": "338", "description": "\u6e05\u4ed3-\u4fa7\u6069ceen\u7537\u978b\u4e13\u573a\u5c3a\u780140"}], "total_price": "338"}], "type": "order_list"}}}}
```


# 环境变数设定:
如程式需要读取任何变数，需要透过环境变数传入
例如以下变数设置
- dev.env 可更改 TW_PORT 连接埠号

设置完毕后，亦需在entrypont.sh 内，加入启动指令。

