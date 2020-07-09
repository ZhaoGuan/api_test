## 接口测试框架
### 简介
开发基于python3,主要使用yml文件配置方法来进行用例管理,并且可以自行自动定义header组成方法，body组成方法，断言方法,和上文生成方法来满足特殊需求。  
用例中所有的完整大写字母单词都为关键字，根据命名规则在用例中包含context的时候会执行上下文测试用例在环境文件中可以利用文件夹名来指定环境变量。  
环境：python3   
依赖内容安装：pip3 install -r requirements.txt  
### 使用
主要通过命令行运行  
python3 main.py 然后添加参数，参数内容如下:  
-h --help   
-r --record main.py 指定读取.har文件路径进行用例转换  
-p --path .har文件录制转换结果路径  
-c --cases 运行case某个文件夹的用例，all_case时为所有文件夹  
-f --filepath 运行用例文件夹下某一个用例case文件夹的相对路径  
-s --source 运行case所指定的环境,不填写默认为online  
-j --json json内容转化为format校验内容  
    eg: -j '{"a":1}'  
-a --alluredir pytest allure报告数据格式存放文件夹，默认为./report  
test运行方法在basics_function/test_template.py中，数据处理和请求的主要内容在api_tester文件夹中.
如果想添加自动以方法请将内容填写在customize_function文件下的对应.py文件中
### 环境变量 
全局环境配置文件在env_config中主要配置全局host    
现规定测试环境使用dev作为表示线上使用online作为标识  
全局host根据文件夹区分host指向的具体内容  
```yaml
xbk:
  online:
    HOST:
      xxxx
  test:
    HOST:
little_bear:
  online:
    HOST:
      https://test.meixiu.mobi
  dev:
    HOST: https://test.meixiu.mobi
```
最外层标识文件夹名,随后是环境名称参数名和具体数值   
根据以上配置对应文件夹下的所有内容在对应的环境下都拥有所填写的全局HOST值   
###单用例
```yaml
SOURCE:
  URL_PATH: #请求路径会与环境变量组合形成url
  METHOD: #请求方法现行只有GET POST
    GET
  DATA_TYPE: #数据类型ONLY表示单用例，MORE表示多用例 
    ONLY
  online: #环境标识
    URL: #当全局HOST不存在的时候或URL_APTH为None时会使用这里的url
    HEADERS: #request时候的headers数据
      TYPE: #HEASERS的类型现行关键字为NORMAL，如果添加了自动定义方法这里添加对应方法名
        NORMAL
      DATA: #HEADERS的数据可以直接使用字典形数据,使用自定义方法的时候直接传入方法中
    PARAMS: #请求参数
      TYPE: #请求参数类型现行关键字为JOIN拼接url,如果添加了自动定义方法这里添加对应方法名
        JOIN
      DATA: #JOIN的时候传入字典形,使用自定义方法的时候直接传入方法中
    BODY:
      TYPE: #请求体类型关键字现行为JSON,请求时使用json格式，如果添加了自动定义方法这里添加对应方法名
        JSON
      DATA: #请求体数据使用字典形，使用自定义方法的时候直接传入方法中
  dev:
    URL:
    HEADERS:
      TYPE:
        NORMAL
      DATA:
    PARAMS:
      TYPE:
        JOIN
      DATA:
    BODY:
      TYPE:
      DATA:
ASSERT:
  DATA_FORMAT: #结构体检查细节后边会描述
    TYPE: #ONLY为唯一结构体检查,当填写MORE的时候DATA使用 k/k/k/v : {结构体},表示当k/k/k等于value的时候结构体为{结构体} 
      ONLY
    DATA: #结构体具体数据生成办法使用命令行 -j 'json数据'
  DATA_CONTENT: #详细数据检查在环境下方加入检查内容
    online:
        - k/k/k: value #k/k/k/k层级下等于value
        - k/k/k=value1: k/k/k/k=value2 # 当k/k/k/k等于value1时,k/k/k/k等于value2
        - STRUCTURE : k/k/k=v 
                        : k/k/k/k
                            {结构体} #特殊结构体检查,当k/k/k等于v时k//k/k/k的结构等于{结构体}
    dev:
  ANOTHER_ASSERT: 
    online: #如果不填写一下关键字不要保留
       TYPE: #填写自定义方法名
       DATA: #填写对应具体数据
    dev:
  RESPONSE_HEADER: #保留字暂时没有作用，随后根据业务添加header判断方法
```
### 单文件多用例
单文件多用例,是在具体的DATA数据下添加一个表示符来区分使用的数据,不添加标识符的数据视为通用数据。标识如果添加要保证数量一致。  
```yaml
SOURCE:
  URL_PATH: /api/home/v1/config/home1Init
  METHOD: GET
  DATA_TYPE: MORE
  online:
    URL:
    HEADERS:
      TYPE:
        NORMAL
      DATA:
    PARAMS:
      TYPE:
        JOIN
      DATA:
    BODY:
      TYPE:
        JSON
      DATA:
  dev:
    URL:
    HEADERS:
      TYPE:
        NORMAL
      DATA:
    PARAMS:
      TYPE:
        JOIN
      DATA:
        - a: #这里是一个标识符
            uid: 469154496589860864
        - b: #这里是一个标识符
            uid: ""
    BODY:
      TYPE:
      DATA:
ASSERT:
  DATA_FORMAT:
    TYPE:
      ONLY
    DATA:
  DATA_CONTENT:
    online:
    dev:
      - a: #这里是一个标识符
        - code: 0
        - status: OK
      - b: #这里是一个标识符
        - code: 0
        - payload/banners/0/banner: "https://s1.meixiu.mobi/image/ad/banner1-invite.png"
  ANOTHER_ASSERT:
  RESPONSE_HEADER:
```
### 上下问用例
上下文用例是顺序执行可以使用之前已经写好的单用例文件,如果不需要可以让PATH关键字为空，随后和单用例一致的数据格式填写,ABOVE关键字是描述使用上文的方法，可以自定义。  
如果要正确的执行上下文用例文件名需要有关键字context,例如:context_xxxxx.yml    
```yaml
- STEP:
  PATH: /little_bear/cases_from.yml #复用的单用例数据
  SOURCE:
    URL_PATH:
    METHOD:
        GET
    DATA_TYPE:
        ONLY
    dev: #以下都是为会替换原有用例的内容
        URL: https://test.meixiu.mobi/api/ts/v1/teaching/student/history/course/list
        HEADERS:
            TYPE:
                NORMAL
            DATA:
        PARAMS:
            TYPE:
                JOIN
            DATA:
                appversion: 1.3.2
                ostype: ios
                page: 0
                studentId: 462297116145094656
        BODY:
            TYPE:
                JSON
            DATA:
  ASSERT: #这里不支持替换DATA_FORMAT内容
    DATA_CONTENT:
    ANOTHER_ASSERT:
  ABOVE: #不填写不会处理上文内容，没有上文也请删除
- STEP:
  PATH:
  SOURCE:
    URL_PATH: /api/ts/v1/teaching/student/course/getCourseDetail
    METHOD:
        GET
    DATA_TYPE:
        ONLY
    dev:
        URL:
        HEADERS:
            TYPE:
                NORMAL
            DATA:
        PARAMS:
            TYPE:
                JOIN
            DATA:
                courseId: 944
                studentId: 462297116145094656
        BODY:
            TYPE:
                JSON
            DATA:
  ASSERT:
    DATA_CONTENT:
    ANOTHER_ASSERT:
  ABOVE: # 支持list替换多个内容,但是要保证自身数据内容的完整，应为是修改，而不是增加
    - FROM: BODY #数据来源,BODY或HEADERS
      TYPE: KEYS #获取数据方法，HEADERS和BODY都支持KEYS，HEADER的时候支持ALL会完整替换headers数据
      DATA: payload/content/0/courseId
      TO:
        PARAMS: courseId #要替换到的位置和路径，位置支持PARAMS,HEADER,BODY,路径为k/k/k/k,在数据的部分可以使用random来随机去当前层级下的内容
    - FROM:
      TYPE: #如果想使用自定义方法主要是填写TYPE，保证和自己添加的方法名一致，其他数据所以，会将case中的所有数据传入方法中。
      DATA:
      TO:
```
### 关于DATA_FORMAT的校验语法
Bool 表示布尔型  
Int 表示数字型  
String 表示字符型  
null 表示None  
在String的情况是如果是个url会做一次请求检查  
$$$ 表示忽略    
| 表示或当有多个可能的时候可以用|分离    
本身DATA_FORMAT是可以填写具体值的,所以你可以复制一个完整的具体内容，如果有特殊部分需要校验可以使用DATA_CONTENT的STRUCTURE进行校验DATA_FORMAT中填写忽略($$$).  
### 关于报告
运行后会默认生成一份allure的报告数据在report文件夹中如果想生成具体报告请使用allure具体使用请参考自己的环境.  
MAC/Linux下实例:  
allure generate --clean  ./report  
