### Level-空（什么时候能做派蒙啊）

##### 拿到题先看看，程序逻辑是输入一串字符，如果正确则输出“重庆没水没电没网大学”，如果正确则输出“好”，看起来像是普通的re签到题，不管，丢ida，找到main函数（ctrl+f寻找），无脑f5开始研究。



#### **静态调试部分（这一段其实基本都是踩的坑，可以忽略绝大部分直接看动态调试部分）**

[1.png](https://github.com/fuurinko/photo0/raw/main/1.png)		![](/Users/rin/Documents/image/1.png)	 		

【ps：找main函数时候其实踩了巨多坑。我用的是ida7.0，它并不能自动识别main函数，但其实也有办法，start跟进就好了，奈何我菜，研究了很多天没有一点头绪（因为这个main函数里面感觉也很绕（由于本来就不应该静态调试（这也是后话了）））。直到后来问了大佬于是更新了7.5版本这个问题才得以解决】



While（）括号后面原本是一串指令，跟进后显示数值为1，可以理解为一个死循环。无限执行sleep函数

[2.png](https://github.com/fuurinko/photo0/raw/main/2.png)		![](/Users/rin/Documents/image/2.png)	 		

##### 这个sleep函数，参考百度上的定义：

###### Sleep函数可以使计算机程序（进程，任务或线程）进入休眠，使其在一段时间内处于非活动状态，括号后的数则是休眠的时间。



也就是在休眠这么一段时间后中止程序。所以 create thread（）以后的句子可以理解为没什么用了。我们就把重心放在这个create thread函数上。

create thread（），百度后知这是一个建立新线程的函数，其中一个参数是在新线程中需要被执行的函数。也就是这个startaddress。【ps：0i64也就是0，create thread在被调用的时候需要有六个参数，这里把其他几个设置成0，可能是没必要吧。。。】

我们跟进它。

[3.png![](/Users/rin/Documents/image/3.png)](https://github.com/fuurinko/photo0/raw/main/3.png)

第一句定义函数基本信息后。第三四没有看懂，也许是某种定义。不是关键句。





第六句，virtual protect。百度得 “VirtualProtect，是对应 Win32 函数的逻辑包装函数，它会在呼叫处理程序的虚拟位置空间里，变更认可[页面](https://baike.baidu.com/item/页面/5544813)区域上的保护” ，对于这句话我并不能深刻理解，但是我们可以知悉这个函数的调用参数的含义。

loc_1400011A0 目标地址起始位置

(char *)main - (char *)loc_1400011A0 内存大小

后面两个可以忽略。

这一句大概就是针对于从main函数地址到loc_1400011A0地址的内存属性进行改变。具体目的可能是为了实现保护吧。

也不是关键的东西

第七句是一个循环体。

[4.png![](/Users/rin/Documents/image/4.png)](https://github.com/fuurinko/photo0/raw/main/4.png)



I=某个数（稍后分析），当I小于main（int），i对0x44进行异或。



第九句再次创建了一个新的线程，但是这次调用的不是startaddress而是loc_1400011A0，最后return 0。

我不是很能理解第九句的作用，所以让我们跟进loc_1400011A0看看这一个指令集的具体作用。





跟进后发现这一指令位于text段。查看交叉引用发现不止startaddress对其进行了引用。

[5.png![](/Users/rin/Documents/image/5.png)](https://github.com/fuurinko/photo0/raw/main/5.png)



但这不好。我并不能看懂。百度过后我们知道它和动态代码有关，但我选择战略性忽略。

[6.png![](/Users/rin/Documents/image/6.png)](https://github.com/fuurinko/photo0/raw/main/7.png)

 直接看汇编指令。

首先明确：我们不知道al里的值，设为a。

a与17h进行与运算得b

b与0c5h进行或运算得c

Test运算不会改变al的值，忽略。

C与0cfh或运算得d

D与5bh进带借位减法得e

E与0c9进行或运算得f

之后就没有针对al的运算指令了。

看下一句

push rcx后条件转移到loc_14000121B

[7.png![](/Users/rin/Documents/image/7.png)](https://github.com/fuurinko/photo0/raw/main/8.png)

Mov 858ECF46h至esi，

lodsd指令指从 [esi]加载到 eax

pop rbx 出栈

交换eax和r13d数据

清栈。

由于已经跳转，战略性忽略adc   rax, [r15+r14*2+554B84h]这一条指令。（看不懂）（）







解决i的问题需要一个多元一次方程，这里我们先放一放。

来看main，这里main是一个int类型数，作为一个c语言分数不尽人意的菜鸡，我姑且猜测它为main函数的返回值，也就是0。

那么再重新看之前的循环体。

“I=某个数（稍后分析），当I小于main（int），i对0x44进行异或。”

I=a=f，当If小于0，

F对0x44异或得x

F再次进行之前的运算分别得g，h，i，j，k，但是没啥用。



代码到这里就快分析完了。但是我们仍未知道那天我们寻找的字符是多少，我们甚至没有寻找到哪怕printf或者scanf或者getchar。

我们可以肯定这些东西被巧妙地隐藏起来了。



ida字符串搜索“give”

[8.png](https://github.com/fuurinko/photo0/raw/main/8.png)![](/Users/rin/Documents/image/8.png)

可以看到程序显示的字符都在这些只读数据段中，但是没有任何的交叉引用。



然后我没有了思路，直到hint提示：smc

？

What is smc？

###### **SMC（Self-Modifying Code）（自解码），可以在一段代码执行前对它进行修改。常常利用这个特性，把代码以加密的形式保存在可自行文件中，然后在程序执行的时候进行动态解析。这样我们在采用静态分析时，看到的都是加密的内容，从而阻断了静态调试的可能性。**



------------------------------------------------------------------------------------------------------------

#### **动态调试部分**





**从天而降的****hint****总算是给弹尽粮绝的可怜人一点希望了。**



**（我对于）这道题的动态分析部分的思路就是，先找到被****smc****代码加密的关键函数**

[9.png](https://github.com/fuurinko/photo0/raw/main/9.png)

![](/Users/rin/Documents/image/9.png)

 **姑且猜测这个函数就是之前跟进以后内容非常诡异的****loc_1400011A0**

**我们就地取材，就用****ida****自带的动态调试器进行动态调试。**

**（并且在动态调试器中由于程序已经被执行，所以代码会和未执行前的静态代码有区别**

[10.png](https://github.com/fuurinko/photo0/raw/main/10.png)

![](/Users/rin/Documents/image/10.png)

**直接对第九句下断点，查看运行情况**



**可以看到（我们熟悉的）主程序已经被执行一部分了，所以我们想要寻找的被加密的函数应该就藏在第九句。我们的猜测似乎被验证了一部分**





**继续跟进loc_1400011A0** 

[11.png](https://github.com/fuurinko/photo0/raw/main/11.png)![](/Users/rin/Documents/image/11.png)

**继续我们的猜测，我们缺少一个能够加密我们输入字符串并将其加密后与原本的字符串进行对比然后输出重庆balabala大学的函数。**

**由于smc代码对该段进行了加密，所以ida无法将其正确识别成某个单独的函数。所以当我们获得了函数的开始的地址，我们得再找到它的结束地址。**

[12.png](https://github.com/fuurinko/photo0/raw/main/12.png)![](/Users/rin/Documents/image/12.png)

**如图00000001400015A0后为main。**



######  **所以这个函数其实是在main执行之前就执行了吗，还是说ida里面数据段的排布是混乱的？**

**在经过对00000001400011A0和00000001400015A0之间的一些奇怪的函数的测试之后，我们终于发现如果把这个地址区间的数据转换成一个完整的函数，那么奇迹就会发生。**

**因为ida显示的是它瞎识别以后的结果，我们先把这一段数据变为undefine后，手动将它转为code，再在开头创建函数**

**F5发现可以反汇编**

[13.png](https://github.com/fuurinko/photo0/raw/main/13.png)

![](/Users/rin/Documents/image/13.png)

[14.png](https://github.com/fuurinko/photo0/raw/main/14.png)![](/Users/rin/Documents/image/14.png)

**至此我们终于找到了最关键的函数。**

**通过分析这个函数我们就能知道程序加密字符串的方式，并且解出字符串。**

**研究程序后，大致认为是输入一个八位的字符，把字符存入v8这个数组。**

**设a1a2a3a4a5a6a7a8,这八个数经过函数中的运算后符合方程式，则输出重庆balabla大学。**





[15.png](https://github.com/fuurinko/photo0/raw/main/15.png)![](/Users/rin/Documents/image/15.png)

[16.png](https://github.com/fuurinko/photo0/raw/main/16.png)

![](/Users/rin/Documents/image/16.png)

**运用神奇的z3-solver（这玩意真难装）**

**解出八个变量的值，依次排序后对应asc2表推出输入字符为MAGA2020（77 65 71 65 50 48 50 48）**

**输入后得到期盼的答案。**

**重庆**

**没水**

**没电**

**没网**

**大学。**

[17.png](https://github.com/fuurinko/photo0/raw/main/17.png)

![](/Users/rin/Documents/image/17.png)

 yeah







**总结（唠叨）：**

  基于我上学期都去爬墙学web还学的特别烂的情况下我觉得level空真是贼难。

  虽然之前对二进制安全有过一小段时间的研究（主要都是去啃汇编指令了），但re是真没怎么接触，题做的也都是pwn类型的。所以对于做题中碰到的难点（我认为的）最初都是一头雾水。好在问了请教了一些大佬之后山回路转（）

  荧妹妹我是真的做不出了，汇编指令我可能还需要再研究一段时间再patch，大致的思路就是直接jmp到重庆没水没电大学或者其他啥的（）。

  但是level派蒙我还是有点信心的（虽然还没有做（毕竟应急食品不能随便动（x）））。毕竟栈溢出算半个老朋友了，做出来的话会另外交（现在交大概是因为我怕过ddl还没有做出来）

[7aadfc42b3f3e37fe6e4ca25f750b03c_2399226640606781105.jpg](https://upload-bbs.mihoyo.com/upload/2019/08/27/73733731/7aadfc42b3f3e37fe6e4ca25f750b03c_2399226640606781105.jpg?x-oss-process=image/resize,s_600/quality,q_80/auto-orient,0/interlace,1/format,jpg)![](/Users/rin/Downloads/7aadfc42b3f3e37fe6e4ca25f750b03c_2399226640606781105.jpg)