
# Table of Contents

1.  [作用](#orgc10729d)
2.  [结构说明](#org4488b0d)
3.  [如何添加一个新的实体](#org5fe72c7)
4.  [新建一个项目](#orgb8bb509)



<a id="orgc10729d"></a>

# 作用

<p class="verse">
主要用于派生其它基于Flask的项目<br />
</p>


<a id="org4488b0d"></a>

# 结构说明

<p class="verse">
1. dao: 数据库交互层<br />
2. manager: 业务逻辑层,直接访问dao<br />
3. ctrl: 控制层,与manager对接，业务逻辑控制<br />
4. view: 视图层,与ctrl对接<br />
5. proto: protobuf保存目录<br />
&#xa0;&#xa0;&#xa0;1. proto/xx 保存xx数据类型<br />
&#xa0;&#xa0;&#xa0;2. proto/vo/xx 保存xx数据类型的视图。也就是返回到前端的结构<br />
6. submodules: git子模块保存目录<br />
7. gproto: gRPC的proto保存目录。用于定义api。以子模块的方式引入该gproto<br />
</p>


<a id="org5fe72c7"></a>

# 如何添加一个新的实体

<p class="verse">
1. 创建 /proto/XXX/new-x.proto: **cm** snippet<br />
2. 创建 /dao/XXX/new-x.py: **cda** yasnippet<br />
3. 创建 /manager/XXX/new-x.py: **cmn** yasnippet<br />
4. 创建 /ctrl/XXX/new-x.py: **cct** yasnippet<br />
5. 在 gproto/添加 new-x.proto 使用 **capi** yasnippet 添加基础接口以及其返回的VO<br />
</p>


<a id="orgb8bb509"></a>

# 新建一个项目

<p class="verse">
1. frok from flask-template named A<br />
2. create project A-gproto<br />
3. create api.proto in A-gproto if you need gRPC<br />
3. create project-client if A is a backend service<br />
4. add A-gproto as A's submodule. `git submodule add A-gproto gproto`<br />
</p>
