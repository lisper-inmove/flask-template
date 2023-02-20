
# Table of Contents

1.  [作用](#orgf90b3a6)
2.  [结构说明](#org2fcac36)
3.  [如何添加一个新的实体](#orgc06aa0c)
4.  [新建一个项目](#org1c8815f)



<a id="orgf90b3a6"></a>

# 作用

<p class="verse">
主要用于派生其它基于Flask的项目<br />
</p>


<a id="org2fcac36"></a>

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


<a id="orgc06aa0c"></a>

# 如何添加一个新的实体

<p class="verse">
1. 创建 /proto/XXX/new-x.proto: **cm** snippet<br />
2. 创建 /dao/XXX/new-x.py: **cda** yasnippet<br />
3. 创建 /manager/XXX/new-x.py: **cmn** yasnippet<br />
4. 创建 /ctrl/XXX/new-x.py: **cct** yasnippet<br />
5. 在 gproto/添加 new-x.proto 使用 **capi** yasnippet 添加基础接口以及其返回的VO<br />
</p>


<a id="org1c8815f"></a>

# 新建一个项目

<p class="verse">
1. frok from flask-template named A<br />
2. create project A-gproto<br />
3. create api.proto in A-gproto if you need gRPC<br />
3. create project-client if A is a backend service<br />
4. add A-gproto as A's submodule. `git submodule add A-gproto gproto`<br />
5. update url-prefix at viwe/view-port.py<br />
</p>
