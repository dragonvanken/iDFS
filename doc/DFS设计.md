# NameServer

## 1.文件目录树
```
graph TD
    A[\root] --> B(\dir)
    A --> C(file)
    B --> D(\dir)
    B --> E(file)
    B --> F(file)
```
&emsp;&emsp;文件目录树包括**文件夹非叶子节点**和**文件叶子节点**。

1.1 抽象节点
```C
class AbstractNode
{
    private:
        string name; // 节点名称
        bool iswirte;// 写访问控制
    public:
        void setname(string);//设置名称
        string getname();//获取名称
        AbstractNode* child; //左起第一个孩子节点
        AbstractNode* brother; //向右的兄弟节点
}
```
1.2 文件夹节点
```C
class DirNode：public AbstractNode
{
   \\可做权限控制
}
```
1.3 文件节点FID
```C
class FileNode：public AbstractNode
{
    private:
        string file_ID;
        \\可做文件访问流量检测
    public:
        void setID(string);
        string getID();
}
```
1.4 文件目录树结构
```C
class tree
{
    private:
        AbstractNode* root;//根节点
    public:
        AbstractNode* seek(string path); //根据路径返回对应的节点
        bool addnode(AbstractNode*);//添加节点
        bool deletenode(string path);//删除节点
}
```

## 2、注册表

```
graph TD
    C1(注册DID)--> D1(网络socket)
    C2(注册DID)--> D2(网络socket)
    C3(注册DID)--> D3(网络socket)
```

2.1 注册表DID

注册ID | IP | 端口 | 活跃状态 | 文件块数
--|--|--|--|--
D01|192.168.1.2|50000|1|3
D02|192.168.1.6|50000|0|2
```c++
class head{
    public:
        string DID;
        string IP;
        int port;
        int alive;
        int nchunk;
}
```
2.2 注册表
```C
class Register{
    private:
        head serverlist[1024];
    public:
        string add(head);//ID不传入
        bool delete(string ID);
        void setalive(string ID,int);
        void updatechunk(string ID,int);
        string getip(string ID);
        string getport(string ID);
}
    
    
```
## 3、分块表
```
graph TD
    A[文件FID]--> B1(文件块KID)
    A1[FID] --> B2(KID)
    A1--> B3(KID)
    A1--> B4(KID)
    B1--> C1(注册DID)
    B2--> C1(注册DID)
    B3--> C2(DID)
    B4--> C3(DID)
   
```
3.1 文件块列表（KID->DID）
文件块KID|服务器DID
--|--
chunk011|D01
chunk012|D01
chunk013|D02
```python
class chunklist:
    map(KID,DID)
    
    add(KID,DID)
    delete()
    seek(KID)
```
3.2 分块表(FID -> KIDs)

文件FID|文件块KID|文件块KID|文件块KID
--|--|--|--
file01|chunk011|chunk012|chunk013
file02|chunk021|chunk022|null
file01|chunk011|null|null


```python
class filechunk:
    file_chunk={}
    
    addchart(string FID,string KID[]);
    deletechart(string FID);
    getchunk(string FID); // return KID[]
    getFID(string KID);//return FID
```

## 4、备份文件块
主文件块KID|备份文件块KID1|备份文件块ID2|...
--|--|--|--
chunk011|chunk0111|chunk0112|null
chunk021|chunk0211|null

4.1 备份
```pyhton
class backup：
        string KID;主文件块
        string backupChunk=[]//备份文件块数组
        
        add(KID);//添加备份
        delete();//删除备份
        getKID();//返回一个KID
```
4.2 备份队列
```pyhton
class backupque：
        backup backupque=[]//备份数组
        
        seek(主KID);//查询备份数目
        add();//添加备份
        delete();//删除备份
        getKID();//返回一个KID 
```

# DataServer
1.注册表
```C++
string DID
NameServer IP+socket
```

2.文件块存储表
文件块KID|存储位置
--|--
chunk011|\user\01.dat
chunk012|\user\02.dat
```C++
Map<KID,path>
```

