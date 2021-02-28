# 红岩二进制方向寒假作业



## 准备阶段

* 解压题目后，看到是一个可执行文件，立马便想到了学长以前分享的IDA反编译器。

![Image text](https://raw.githubusercontent.com/Aotue/syqc/main/QQ%E6%88%AA%E5%9B%BE20210227152933.png?token=ARORX34XSWV2P5EZZ47SXKDAIMZUA)

* 打开后发现好像什么也不懂，按F5发现伪编码也不是太懂，立马想到自己c语言没学好，于是乎开始了b站C语言学习之路。

  <img src="https://raw.githubusercontent.com/Aotue/syqc/main/QQ%E6%88%AA%E5%9B%BE20210227153657.png?token=ARORX3Z2O77RS3L2YQ5IS3LAIM2O6" alt="Image text" style="zoom: 50%;" />

* 顺便在CSDN和b站上看了一些关于IDA的教程，看完后也对这次的题目没什么感觉，一筹莫展……:broken_heart:

## 解题（碰运气）阶段

* 尝试随便输了下发现每次都是Nice！然后程序结束。想了想，是不是可以打补丁“让Nice！”变成

“Chongqing No Water No Electric No Network University”，于是找了下相关的软件，就是下面这个。

![Image text](https://raw.githubusercontent.com/Aotue/syqc/main/QQ%E6%88%AA%E5%9B%BE20210227153834.png?token=ARORX32T2JQCC5CPVZFF7CLAIM3FW)

* 抱着试一试的心态学了下这个软件，发现可行性很大。于是ALT+T搜到了Nice！十六进制位置。复制，然后在x64dbg上按CTRL+G找到了Nice！的位置，右键编辑修改一气呵成。

  <img src="https://raw.githubusercontent.com/Aotue/syqc/main/QQ%E6%88%AA%E5%9B%BE20210227154002.png?token=ARORX3YYULVM2GBFBWO6YS3AIM3VO" alt="Image text" style="zoom:80%;" />

  <img src="https://raw.githubusercontent.com/Aotue/syqc/main/QQ%E6%88%AA%E5%9B%BE20210227154113.png?token=ARORX3766DFUCHR2BFCYLC3AIM33A" alt="Image text" style="zoom:80%;" />

  <img src="https://raw.githubusercontent.com/Aotue/syqc/main/QQ%E6%88%AA%E5%9B%BE20210227154242.png?token=ARORX36DD4IOKPM4MNBRJDDAIM36K" alt="Image text" style="zoom:67%;" />

  

  + 接着用打完补丁的可执行文件试了下，发现无论输什么都可以出来“Chongqing No Water No Electric No Network University”。瞎猫碰到死耗子:smile:

    <img src="https://raw.githubusercontent.com/Aotue/syqc/main/QQ%E6%88%AA%E5%9B%BE20210227154318.png?token=ARORX32XGFABEF6SOVDSNRTAIM5KS" alt="Image text" style="zoom:67%;" />

  ## 心得体会

  

  + 总之就觉得自己非常菜:pensive:,用了很长时间才做出可能不正确的答案。希望红岩的学长（大佬）看到我的作业时多多包含。我以后也会努力的！