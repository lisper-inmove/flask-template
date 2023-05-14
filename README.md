
# Table of Contents

1.  [作用](#org01e54b8)
2.  [结构说明](#org12b5cd0)



<a id="org01e54b8"></a>

# 作用

<p class="verse">
主要用于派生其它基于Flask的项目<br />
</p>


<a id="org12b5cd0"></a>

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
