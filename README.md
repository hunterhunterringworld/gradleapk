## apk打包

根据已有的工程打包一个apk：打包-360加固（待定）-walle(渠道)

## 工具：

| na             | detail         |
|----------------|----------------|
| runApk         | 根据已有的工程打包一个apk |
| updateFileWord | 更改文件中文案        |
| getApk         | 获取渠道包          |
| putAppOpen     | 拷到公开文件中        |

## MCP 服务器配置

```
    {
        "mcpServers":{
            "gradeapk":{
                "name": "gradeapk",
                "command": "uv",
                "args": [
                    "--directory",
                    "D:\\python\\work\\work\\AI\\tt\\open\\opentl",
                    "run",
                    "work.py"
                ],
                "env": {
                    --python2Path="python2的路径",
                    --jdkPath="jdk的路径",
                    --proPath="工程的路径",
                    --wallePath="walle 的路径",
                    --toPath="拷到公开的路径"
                }
            }
        }  
    }
```