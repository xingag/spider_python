#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: exec_jar_example.py 
@time: 2021-01-02 12:30 
@description：TODO
"""

import jpype
import os

# 初始化
jar_path = os.path.join(os.path.abspath('.'), 'jar/encry.jar')

print(jar_path)

# 启动jvm
jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % (jar_path))


# 通过包名，实例化JAVA对象
EncryClass = jpype.JClass("com.xingag.common.EncryHelper")
encryClass = EncryClass()

# 调用JAVA中的加密方法
content_encry = encryClass.encrypt("xag")
print(content_encry)

# 关闭jvm
jpype.shutdownJVM()
