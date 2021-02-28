@[TOC](Wintertask)

# winterTASK.exe

一开始没有Hint的时候走了许多弯路，幸好Hint放得早。
## RESERVE
**先从Level-空开始吧**
直接双击打开程序,输入a，结果错误的话就输出nice。![在这里插入图片描述](https://img-blog.csdnimg.cn/20210129200308355.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2OTk1MzEz,size_16,color_FFFFFF,t_70)
直接IDA64打开程序按F5查看伪c代码
```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  CreateThread(0i64, 0i64, StartAddress, 0i64, 0, 0i64);
  while ( dword_140005034 )
    Sleep(1u);
  Sleep(500u);
  system("pause");
  return 0;
}
```
可见重点在于 
>CreateThread()函数

[百度百科对于CreateThread()函数的介绍](https://baike.baidu.com/item/CreateThread/8222652?fr=aladdin#4)
调用StartAddress()函数创建了一个新进程，双击查看该函数
```c
__int64 __fastcall StartAddress(LPVOID lpThreadParameter)
{
  DWORD (__stdcall *i)(LPVOID); // rax
  DWORD flOldProtect; // [rsp+48h] [rbp+10h] BYREF

  VirtualProtect(loc_1400011A0, (char *)main - (char *)loc_1400011A0, 0x40u, &flOldProtect);
  for ( i = loc_1400011A0; (unsigned __int64)i < (unsigned __int64)main; i = (DWORD (__stdcall *)(LPVOID))((char *)i + 1) )
    *(_BYTE *)i ^= 0x44u;
  CreateThread(0i64, 0i64, loc_1400011A0, 0i64, 0, 0i64);
  return 0i64;
}
```
根据Hint结合[BUUCTF-re-[GWCTF 2019]re3](https://blog.csdn.net/Palmer9/article/details/105034093?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-7.baidujs&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-7.baidujs)与[SMC 入门笔记 && HGAME 题目复现](https://zhuanlan.zhihu.com/p/66797526) 这两篇文章，可知==loc_1400011A0==为加密块的起始地址，并且在==main函数==(0x1400015A0)前截止，采用与0x44异或来加密，于是编写的解密脚本。
```c
#include <idc.idc>

static main()
{
    auto addr = 0x1400011A0;
    auto main = 0x1400015A0;
    for (; addr < main ; addr++ ){
        PatchByte(addr, Byte(addr) ^ 0x44);
}
}
```
解密前：
![解密前](https://img-blog.csdnimg.cn/20210210164935560.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2OTk1MzEz,size_16,color_FFFFFF,t_70#pic_center)
解密后：
![解密后](https://img-blog.csdnimg.cn/20210210165924192.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2OTk1MzEz,size_16,color_FFFFFF,t_70#pic_center)

但是==loc_1400011A0==没有自动生成sub_xxx的函数，先随便选中汇编汇编代码块，按<kbd>P</kbd>生成函数，出现了错误，而且标红
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210210170628381.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2OTk1MzEz,size_16,color_FFFFFF,t_70#pic_center)

按F5查看伪C代码：
```c
_int64 __fastcall sub_1400011A0(LPVOID lpThreadParameter, __int64 a2, __int64 a3, __int64 a4, int a5, int a6, int a7, int a8, int a9, int a10, int a11, int a12, int a13, int a14, int a15, int a16, int a17, int a18, int a19, __int64 a20, __int64 a21)
{
  __int64 v21; // rdx
  int v22; // er8
  int v23; // er9
  __int64 v24; // rax
  __int128 v26[6]; // [rsp+20h] [rbp-78h] BYREF
  int v27; // [rsp+80h] [rbp-18h]

  v26[0] = 0i64;
  v27 = 0;
  v26[1] = 0i64;
  v26[2] = 0i64;
  v26[3] = 0i64;
  v26[4] = 0i64;
  v26[5] = 0i64;
  sub_140001760(std::cout, "Give me some words > "); //对应程序开头的输出
  sub_140001A00(std::cin, v21, v26); //对应输入，但是有两个参数
  if ( LODWORD(v26[0]) == “PUQC“ && BYTE4(v26[0]) == ”T“ )
  {
    rand();
    JUMPOUT(0x14000121Ai64);
  }
  v24 = -1i64;
  do
    ++v24;
  while ( *(v26 + v24) );
  return sub_140001299(
           SBYTE4(v26[0]),
           v26,
           v22,
           v23,
           a5,
           a6,
           a7,
           a8,
           a9,
           a10,
           a11,
           a12,
           a13,
           a14,
           a15,
           a16,
           a17,
           a18,
           a19,
           a20,
           a21);
}
```
使用==sub_140001760==与==sub_140001A00==分别调用cout与cin应该是某种更高级的CPP输入输出方法，CPP Primer Plus才看到300多页，现在先不管，后面再去找找吧。（没有SMC解密之前，以为在这两个是加密函数，看了好久都没看懂QAQ)。

随后的if判断：
关于LODWORD
>这是Win32编程中常用的两个宏,
HIWORD是High Word的缩写du,作用是取得某个zhi4字节变量(即32位的值dao)在内存中处于高位的两zhuan个字节,即一个word长的数据,例如对于十六进制数0xCCDDEEFF,那么HIWORD(0xCCDDEEFF)得到的结果就是oxCCDD,正好是一个word值.
同理,LOWORD(0XCCDDEEFF)返回的结果就是0xEEFF,也正好是一个word值.
可以用下面的c语言代码测试一下:
#include <windows.h>
#include <stdio.h>
int main()
{
DWORD dwValue ;
WORD low, high ;
dwValue = 0XCCDDEEFF ;
high = HIWORD(dwValue) ;
low = LOWORD(dwValue) ;
printf("high = 0x%x, low = 0x%x", high, low) ;
return 0 ;
}

关于BYTE4
>Sbyte:代表有符号的8位整数，数值范围从-128 ～ 127,后面跟数字应该就是位移4位了，相当于str[4]（猜测）
Byte:代表无符号的8位整数，数值范围从0～255。

详情见[IDA Pro反编译代码类型转换参考](https://www.cnblogs.com/goodhacker/p/7692443.html)
```c
LODWORD(v26[0]) == “PUQC“ && BYTE4(v26[0]) == ”T“
```
第一个字符串是反的”CQUP“，先输入试一下。
![CQUPT](https://img-blog.csdnimg.cn/20210210174005981.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2OTk1MzEz,size_16,color_FFFFFF,t_70#pic_center)
虽然什么也没有输出，但是也没有输出"Nice!"。
说明确实是进入到里面执行了，而不是进到==sub_140001299==里面（sub_140001299如果条件符合就会输出Nice！，等下再看）。
但是字符串为何是反的？想到的关联因素有：
- __int128 str 为小端序存储方式，后面求解的时候需要特别注意！

但是if代码块里面只有==rand()==函数和标红的==JUMPOUT(0x14000121Ai64)==,而跳转到的地方和上文中有标红的位置一致。
在查看了[IDA出现"sp-analysis failed"和F5(反编译)失败](https://blog.csdn.net/lixiangminghate/article/details/78820388)和[IDA反编译的几个注意和技巧](https://blog.csdn.net/qq_36535153/article/details/105215746)这两篇文章后，还是第一个靠谱hhh。
	
	第一篇文章大概意思就是说代码里面添加了花指令，通过一些手法来还原代码
发现还原不出来，但是注意到了还是那段汇编代码块，类型为db，而不是代码，一不小心，操作失误，按了右键->转化为代码，竟练出代码坤，哦原赖氏要把那几个
```basic
text:000000014000121A                 db 0C1h
.text:000000014000121B ; ---------------------------------------------------------------------------
.text:000000014000121B                 cli
.text:000000014000121B ; ---------------------------------------------------------------------------
.text:000000014000121C                 db    2
.text:000000014000121D                 db  8Bh
.text:000000014000121E                 db 0CAh
.text:000000014000121F                 db 0C1h
.text:0000000140001220                 jmp     near ptr 0CDD11544h
.text:0000000140001220 ; ---------------------------------------------------------------------------
.text:0000000140001225                 db  0Ch
.text:0000000140001226                 db  92h
```
按<kbd>C</kbd>转化为汇编代码，之前那个位置的错误就消失了。按照之前的步骤生成函数，按<kbd>F5</kbd>，if语句里面又有了新的内容：
```c
v24 = rand() % 10;
    if ( v24 + rand() % 10 > 30 )
    {
      v25 = sub_140001760(std::cout, "Redrock");
      std::ostream::operator<<(v25, sub_140001930);
    }
    JUMPOUT(0x14000157Ei64);
```
观察到v24和v25两个变量被用了起来，但是还有其他变量没有用，而且还有==JUMPOUT==，而且在汇编代码处，还有sp-analysis failse
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021021018375920.png#pic_center)
看来，没有变成代码的 db xxx才是干扰指令，这时，把从==0x1400011A0==到main函数之前的代码全部选中，生成函数，才得到了正确的函数：
```c
__int64 __fastcall sub_1400011A0(LPVOID lpThreadParameter)
{
  __int64 v1; // rdx
  int v2; // ebx
  __int64 v3; // rax
  __int64 v4; // rax
  const char *v5; // rdx
  __int64 v6; // rax
  __int128 v8[6]; // [rsp+20h] [rbp-78h] BYREF
  int v9; // [rsp+80h] [rbp-18h]

  v8[0] = 0i64;
  v9 = 0;
  v8[1] = 0i64;
  v8[2] = 0i64;
  v8[3] = 0i64;
  v8[4] = 0i64;
  v8[5] = 0i64;
  sub_140001760(std::cout, "Give me some words > ");
  sub_140001A00(std::cin, v1, v8);
  if ( LODWORD(v8[0]) == 1347768643 && BYTE4(v8[0]) == 84 ) //转换成16进制，发现是ASCII码，转换为字符串
  { //这块是另一个level的入口
    v2 = rand() % 10;
    if ( v2 + rand() % 10 > 30 )
    {
      v3 = sub_140001760(std::cout, "Redrock");
      std::ostream::operator<<(v3, sub_140001930);
    }
  }
  else
  {
    v4 = -1i64;
    do
      ++v4;
    while ( *(v8 + v4) ); //这段代码判断字符串长度是否等于8
    if ( v4 != 8
      || 870732 * SBYTE5(v8[0])
       + 620576 * SBYTE6(v8[0])
       + 687392 * SBYTE3(v8[0])
       + 790701 * SBYTE4(v8[0])
       - 264980 * SLOBYTE(v8[0])
       - 558068 * SBYTE1(v8[0])
       - 940616 * SBYTE7(v8[0])
       - 805665 * SBYTE2(v8[0]) != -1990197
      || 242625 * SBYTE5(v8[0])
       + 230650 * SBYTE4(v8[0])
       + 460946 * SBYTE3(v8[0])
       + 269419 * SLOBYTE(v8[0])
       + 630862 * SBYTE1(v8[0])
       - 24920 * SBYTE7(v8[0])
       - 482510 * SBYTE2(v8[0])
       - 580412 * SBYTE6(v8[0]) != 50416313
      || 340464 * SBYTE2(v8[0])
       + 719348 * SBYTE3(v8[0])
       + 240775 * SBYTE7(v8[0])
       + -207754 * SBYTE1(v8[0])
       - 470557 * SLOBYTE(v8[0])
       - 719143 * SBYTE5(v8[0])
       - 114858 * SBYTE6(v8[0])
       - 13126 * SBYTE4(v8[0]) != -8167199
      || 639378 * SBYTE5(v8[0])
       + 903739 * SBYTE2(v8[0])
       + 577554 * SBYTE3(v8[0])
       + 107894 * SBYTE7(v8[0])
       - 860840 * SLOBYTE(v8[0])
       - 657457 * SBYTE6(v8[0])
       - 358459 * SBYTE4(v8[0])
       - 179591 * SBYTE1(v8[0]) != 8821640
      || 1848 * SBYTE1(v8[0])
       + 693461 * SBYTE2(v8[0])
       + 862506 * SBYTE7(v8[0])
       - 208232 * SBYTE6(v8[0])
       - 664100 * SBYTE4(v8[0])
       - 192669 * SBYTE5(v8[0])
       - 354894 * SLOBYTE(v8[0])
       - 644389 * SBYTE3(v8[0]) != -31320696
      || 773383 * SBYTE1(v8[0])
       + 154384 * SBYTE7(v8[0])
       + 714136 * SBYTE5(v8[0])
       + -592212 * SBYTE6(v8[0])
       - 858737 * SBYTE4(v8[0])
       - 263859 * SLOBYTE(v8[0])
       - 130037 * SBYTE3(v8[0])
       - 997096 * SBYTE2(v8[0]) != -80151959
      || 209448 * SBYTE1(v8[0])
       + 679897 * SLOBYTE(v8[0])
       + 138284 * SBYTE7(v8[0])
       - 982280 * SBYTE4(v8[0])
       - 127647 * SBYTE2(v8[0])
       - 157768 * SBYTE6(v8[0])
       - 679219 * SBYTE5(v8[0])
       - 907473 * SBYTE3(v8[0]) != -85049773
      || (v5 = "Chongqing No Water No Electric No Network University",
          802559 * SBYTE4(v8[0])
        + 448649 * SBYTE5(v8[0])
        + 190047 * SBYTE1(v8[0])
        + -256569 * SBYTE7(v8[0])
        - 813631 * SLOBYTE(v8[0])
        - 708096 * SBYTE3(v8[0])
        - 999068 * SBYTE2(v8[0])
        - 965947 * SBYTE6(v8[0]) != -166206160) )
    {
      v5 = "Nice!";
    }
    v6 = sub_140001760(std::cout, v5);
    std::ostream::operator<<(v6, sub_140001930);
  }
  dword_140005034 = 0;
  return 0i64;
}
```
>根据Hint提示，使用z3约束器，这里需要注意，如果把负数变为16进制，再变回10进制，IDA会错误判断

参考文章[CG-CTF-re-签到题](https://www.cnblogs.com/palmer0801/p/12111811.html)
写出py脚本：
```python
from z3 import *
s = Solver()
a1 = [0] * 8
for i in range(8):
    a1[i] = Int('a1['+ str(i)+']')
for i in range(1,8):
       s.add(a1[i] >0)
       s.add(a1[i] <255)
s.add(870732 *  a1[5]
       + 620576 *  a1[6]
       + 687392 *  a1[3]
       + 790701 *  a1[4]
       - 264980 *  a1[0]
       - 558068 *  a1[1]
       - 940616 *  a1[7]
       - 805665 *  a1[2] == -1990197 )
s.add(242625 *  a1[5]
       + 230650 *  a1[4]
       + 460946 *  a1[3]
       + 269419 *  a1[0] 
       + 630862 *  a1[1]
       - 24920 *   a1[7]
       - 482510 *  a1[2]
       - 580412 *  a1[6] == 50416313)
s.add(340464 *  a1[2]
       + 719348 *  a1[3]
       + 240775 *  a1[7]
       + (-207754 *  a1[1])
       - 470557 * a1[0] 
       - 719143 *  a1[5]
       - 114858 *  a1[6]
       - 13126 *  a1[4] == -8167199)
s.add(639378 *  a1[5] 
       + 903739 *  a1[2] 
       + 577554 *  a1[3] 
       + 107894 *  a1[7 ]
       - 860840 *  a1[0]
       - 657457 *  a1[6] 
       - 358459 *  a1[4] 
       - 179591 *  a1[1]  == 8821640)
s.add(1848 *  a1[1] 
       + 693461 *  a1[2] 
       + 862506 *  a1[7] 
       - 208232 *  a1[6] 
       - 664100 *  a1[4] 
       - 192669 *  a1[5] 
       - 354894 *  a1[0]
       - 644389 *  a1[3]  != -31320696)
s.add(773383 *  a1[1] 
       + 154384 *  a1[7] 
       + 714136 *  a1[5] 
       + (-592212 *  a1[6]) 
       - 858737 *  a1[4] 
       - 263859 *  a1[0]
       - 130037 *  a1[3] 
       - 997096 *  a1[2]  == -80151959)
s.add(209448 * a1[1] 
       + 679897 * a1[0]
       + 138284 * a1[7] 
       - 982280 * a1[4] 
       - 127647 * a1[2] 
       - 157768 * a1[6] 
       - 679219 * a1[5] 
       - 907473 * a1[3]  == -85049773)
s.add(802559 * a1[4] 
        + 448649 * a1[5] 
        + 190047 * a1[1] 
        + (-256569 * a1[7]) 
        - 813631 * a1[0]
        - 708096 * a1[3] 
        - 999068 * a1[2] 
        - 965947 * a1[6]  == -166206160)
print(s.check())
answer = s.model
print(answer)

```
得到结果：

转换成字符：
解毕
***Level-荧***
根据Hint，主要思路为：
通过动态调试，找到条件判断完成后的位置，修改下一段汇编代码，跳转输出。
程序入口点：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210216040020619.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2OTk1MzEz,size_16,color_FFFFFF,t_70#pic_center)
根据前面的分析，在判断前，直接JMP到V4赋值的位置
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021021604120747.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2OTk1MzEz,size_16,color_FFFFFF,t_70#pic_center)
下断点，断点下在：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210216041850788.png#pic_center)
JMP到赋值的代码块位置                        |![在这里插入图片描述](https://img-blog.csdnimg.cn/20210216042358617.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2OTk1MzEz,size_16,color_FFFFFF,t_70#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210216043135265.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2OTk1MzEz,size_16,color_FFFFFF,t_70#pic_center)

再次修改此处汇编代码：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210216043418712.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2OTk1MzEz,size_16,color_FFFFFF,t_70#pic_center)
修改之后就会执行转移，
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210216044127681.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2OTk1MzEz,size_16,color_FFFFFF,t_70#pic_center)
按<kbd>Ctr</kbd> +<kbd>P</kbd>把之前的修改应用成为补丁，这里也可以在IDA里面修改汇编代码，然后直接把补丁打入程序内，参考[IDA打补丁](https://blog.csdn.net/lilongsy/article/details/108544669)
## PWN(Level-Paimon)
### 基础知识准备
Windows下的PWN以前没有接触过，学习的资料相对于Linux也比较少，先从基础开始吧。
>[Windows Pwn 学习之路](https://www.anquanke.com/post/id/210394#h3-8)这篇文章包含了Win下PWN的环境配置还有详细的基础知识。
>关于vcpkg的环境配置有很多坑，除了文章中提到的，这里列举一下我出现的问题的解决方法。
>1. 必须要安装Visual Studio和一些组件才能正常运行vcpkg
>- 用于CMake和Linux的VisualC++工具
>
>2. 引用包下载失败解决办法: [vcpkg问题-环境配置](https://blog.csdn.net/baidu_40840693/article/details/84704988)
> 
> 3. 编译时要用
> cmake -B [build directory] -S . -DCMAKE_TOOLCHAIN_FILE=[path to vcpkg]/scripts/buildsystems/vcpkg.cmake 这个命令
> 
> 然后看一些例题 [Windows漏洞利用开发教程Part1]( 1https://www.freebuf.com/articles/system/166500.html)
 



