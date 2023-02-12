
# Table of Contents

1.  [作用](#org6ac90ac)
2.  [结构说明](#orge3db708)
3.  [使用说明](#orgccf4a41)
4.  [运行demo](#org43dd967)
5.  [如何添加一个新的实体](#orgc8267ff)



<a id="org6ac90ac"></a>

# 作用

<p class="verse">
主要用于派生其它基于Flask的项目<br />
</p>


<a id="orge3db708"></a>

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
</p>


<a id="orgccf4a41"></a>

# 使用说明

<p class="verse">
1. 更新子模块<br />
</p>

    git submodule update --init --recursive

<p class="verse">
2. 启动服务<br />
</p>

    ./test_run.sh


<a id="org43dd967"></a>

# 运行demo

    git co demo && ./test_run.sh


<a id="orgc8267ff"></a>

# 如何添加一个新的实体

<p class="verse">
1. 创建 /proto/XXX/new-x.proto: **cm** snippet<br />
2. 创建 /proto/vo/XXX/new-x.proto: **cpvo** snippet<br />
3. 创建 /dao/XXX/new-x.py: **cda** yasnippet<br />
4. 创建 /manager/XXX/new-x.py: **cmn** yasnippet<br />
5. 创建 /ctrl/XXX/new-x.py: **cct** yasnippet<br />
6. 创建 /view/XXX/new-x.py: **cvi** yasnippet<br />
</p>
