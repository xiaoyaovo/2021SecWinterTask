



**荧**



要让任意字符长度小于20的字符串输出，思路大致是

利用hint中的“无脑jmp”，无条件跳转到输出目标字符串的指令。





先清楚代码逻辑是第一。



[a.png![](/Users/rin/Desktop/level-荧/image_ying/a.png)](http://note.youdao.com/s/bo1aGfZp)

定义变量

输入字符串 输出“give”句

if条件句当lodwordv8[0]=1347768643和byte4v8[0]=84都为真时，返回值为真，否则为假。

设返回值为真，则令v2为0—9中的一个随机数。若v2再加这个随机数大于30，则输出红岩

跳出里面的那个if条件句，看最外面的if，如果返回值为假，

那么令v4为-1

，++v4开始循环（如果输入数值不符合方程，则输出nice，符合的话进入else中的v5的输出，也就是重庆没水没电没网大学），

最后结束程序。



首先字符串cqnwnennu是在运算中被定义的，如果我们执行思路2，就一定不能跳过这个运算。也许我们可以先让这个运算执行，虽然输入的字符完全不符合方程，但是在程序输出nice之前jmp成输出v5这一句指令，也就是输出重庆没水大学。

所以只需要对一些指令进行patch







然而在对程序patch之前。我们还面临一个新的问题。

之前动态调试的时候smc自解密没有任何问题，但是如何将这种解密后的状态保存下来。又是一个问题。

上一个level我全程没有考虑到这个问题，程序其实一直都是在running状态下的。这次要对程序打补丁。必须先要把没有加密代码的程序做出来。



把startaddress函数中的异或改成异或0————原本是异或44，结果为0，现在结果为i本身

只要运用ida脚本使用异或解密，就可以解开。

[b.png](http://note.youdao.com/s/PQ5OwQrm)

[c.png](http://note.youdao.com/s/JFSTutDP)



首先寻找解密的起始地址，就是整个loc_1400011A0的开头结尾 00000001400011A0和00000001400015A0

开始改脚本（）

[d.png](http://note.youdao.com/s/Inlek3up)

放进ida执行。

[f.png](http://note.youdao.com/s/dNQltil4)

执行的时候脚本总是解不完全。有一小段无法直接转换成代码。手动调了好几次总归是把他弄成可以反编译的函数了.

[e.png](http://note.youdao.com/s/ZKxU9GVI)

（图这里已经把字符判断的数改成了20）





解决了第一步

，来看如何对这个文件打补丁。













我的思路还是先看伪代码，确定要jmp的地方，然后再寻找与其对应的汇编指令。



思路还是把判断是否是nice的地方强制跳转到输出重庆三无大学的地方。

先找到判断输入字符长度的指令



 这里比较14h（20u）和输入字符串长长度，目的是如果字符串长度大于20则输出nice 。

[g.png](http://note.youdao.com/s/66EOo8vK)

jnz改成jge，大于等于即转移到输出nice

[h.png](http://note.youdao.com/s/8utoA8BO)

字符串长度判定完成了。

接下来任务就是跳转输出重庆

[i0.png](http://note.youdao.com/s/TPSP1Xow)

[i.png](http://note.youdao.com/s/G6O0WPMv)

这里的loc_140001283对应的伪代码其实就是执行后面的解密。jnz条件运算是针对于输出redrock的条件的，如果这里直接jmp会使程序简化

jnz改jmp后的伪代码如下

[j.png](http://note.youdao.com/s/AFykoAPz)

到现在改了两处。一处是字符判定，一处是把和level派蒙有关的内容删去了。



剩下的我们需要使“无论输什么数，都跳转到重庆”

[k.png](http://note.youdao.com/s/AxKLCHp5)

可以直接把运算后输出jmp成重庆

这样看看伪代码。

[l.png](http://note.youdao.com/s/Pl02q5j7)

还是有一大段运算。怎么样把他们jmp掉是一个问题。



还是要找到对应的汇编指令

[m.png](http://note.youdao.com/s/91xR6JpT)

如图。最后一个指令，如果运算未满足条件就不跳转，为了把这一段运算jmp掉，把jz改成jmp

[n.png](http://note.youdao.com/s/d1pfu3xw)







[o.png](http://note.youdao.com/s/RhyHmw2Q)

现在的代码

感觉挺靠谱。

但是实际测试发现输出还是nice

心急如焚地研究了一下啥也没发现，然后开始魔改程序。先是把字符判断给jmp了。结果重庆都没了/然后改成jz，字符长度等于20.试试看倒是成功了。见鬼了，为什么小于就失败》

[p.png](http://note.youdao.com/s/GpwPbuc1)

Jle输入长于20个字符也输出nice。

[q.png](http://note.youdao.com/s/9P3rGdwb)

**昨天晚上试怎么都不成功，今天下午一试发现是patch没有完全保存，jge的地方还是jnz，还有一个本来要改成jmp的地方也变成了jnz，然后重新改回来了，直接测试，成功。好家伙**