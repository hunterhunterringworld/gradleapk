import asyncio
import os
import re
import shutil
import subprocess

# 环境python 2.7.17  jdk和gradle 根据app
from mcp.server import FastMCP

python2Path = os.environ.get("python2Path", "D:\\a_work_tool\\python\\python.exe")

jdkPath = os.environ.get("jdkPath", "F:\\androidstuido\\ide\\jre")
proPath = os.environ.get("proPath", "F:\\svnWord\\appsvn\\rich")
wallePath = os.environ.get("wallePath",
                           "C:\\Users\\Administrator\\Desktop\\文档all\\wallet\\jr_ProtectedApkResignerForWalle-master1\\ProtectedApkResignerForWalle-master")

toPath = os.environ.get("toPath", "Z:\\app-渠道包\\HX\\android")
appVer = os.environ.get("appVer", "2.7.01")

general = r' -Dorg.gradle.java.home='
o1 = r"gradlew assembleReleaseChannels"
o2 = r"gradlew clean"

order1 = f"{o1}{general}{jdkPath}"
order2 = f"{o2}{general}{jdkPath}"
# os.environ["JAVA_HOME"] = 'C:\\Program Files\\Java\\jdk1.8.0_05'

notPath = "当前路径未找到"

mcp = FastMCP("takeapp")


@mcp.tool()
async def runApk(order=order1):
    f"""
    根据已有的工程打包一个apk

    :param order: window 的指令,default = {order1}
    :return:
    """
    path = proPath
    if not judgePath(jdkPath) or not judgePath(path):
        return f"{notPath}:{jdkPath} || {path}"

    print(f"path = " + path)
    print(f"order = " + order)

    pyRunOrder(path, order)

    dirApk = f"{proPath}\\app\\build\\outputs\\channels"
    fileArray = os.listdir(dirApk)
    return fileArray[len(fileArray) - 1]


@mcp.tool()
async def updateFileWord(toApkNa):
    """
    更改文件中文案
    :param toApkNa: 待替换的文案
    :return:
    """
    path = wallePath
    if not judgePath(path):
        return f"{notPath}:{path}"

    path = os.path.join(wallePath, "config.py")
    with open(
            path
            , "r"
            , encoding="utf-8"
    ) as f:
        detail = f.read()
        detail = re.sub(r"rich_.+?apk", toApkNa, detail)
        print(detail)

    with open(
            path,
            "w",
            encoding="utf-8"
    ) as f:
        f.write(detail)
    return "ok 啦"


@mcp.tool()
async def getApk():
    """
    获取渠道包
    :return:
    """
    path = wallePath
    if not judgePath(path):
        return f"{notPath}:{path}"
    if not judgePath(python2Path):
        return f"{notPath}:{python2Path}"
    order = f"{python2Path} ApkResigner.py"
    return pyRunOrder(path, order)


@mcp.tool()
async def putAppOpen():
    """
    拷到公开文件中
    :return:
    """
    path = toPath
    if not judgePath(path):
        return f"{notPath}:{path}"
    wallePathTp = wallePath
    if not judgePath(wallePathTp):
        return f"{notPath}:{wallePathTp}"
    okApkPath = os.path.join(wallePathTp, "channels")
    if not judgePath(okApkPath):
        return f"{notPath}:{okApkPath}"

    path = os.path.join(path, appVer, "正式")
    i = 0
    while judgePath(path, False):
        path = os.path.join(path, appVer, f"正式{i}")
        i += 1
    shutil.copytree(okApkPath, path)
    return "ok啦"


@mcp.tool()
async def printEnvValue():
    """
    打印配置的路径
    :return:
    """
    return f"{python2Path}\n{jdkPath}\n{proPath}\n{wallePath}\n{toPath}\n{appVer}"


def pyRunOrder(path, order):
    try:
        pro = subprocess.Popen(
            ["cmd", "/c", order]
            , cwd=path
            , stdout=subprocess.PIPE
            , stderr=subprocess.STDOUT
            , text=True
        )
        for line in pro.stdout:
            print(line, end="")

        pro.wait(timeout=300)
        if pro.returncode == 0:
            return "ok"
        else:
            print("err", pro.returncode)
    except Exception as e:
        print("err pro= ", e)

    return "fail"


def judgePath(path, printFlag=True):
    ret = os.path.exists(path)
    if not ret:
        if printFlag:
            print(f"{notPath}:{path}")
    return ret


if __name__ == "__main__":
    # mcp.run(transport='stdio')
    apkPath = asyncio.run(runApk(order1))
    # # ------------------------------只能手动加固------------------------------
    # updateFileWord("rich_release_20250425170517_v2.6.30_2630_jiagu.apk")
    # okApkPath = getApk()
    # putAppOpen(appVer)
    # print("--------------------------------------ok-----------------------------------------")
