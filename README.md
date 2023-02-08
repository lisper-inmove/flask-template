
# Table of Contents

1.  [作用](#orgb413bde)
2.  [结构说明](#org0206b38)
3.  [使用说明](#org18d9ced)
4.  [运行demo](#org281093f)



<a id="orgb413bde"></a>

# 作用

<p class="verse">
主要用于派生其它基于Flask的项目<br />
</p>


<a id="org0206b38"></a>

# 结构说明

<p class="verse">
1. view: 视图层<br />
2. ctrl: 控制层<br />
3. manager: 业务逻辑层<br />
4. dao: 数据库操作层<br />
5. submodules: 子模块层<br />
6. proto: Protobuf 文件存放位置<br />
</p>


<a id="org18d9ced"></a>

# 使用说明

<p class="verse">
1. 更新子模块<br />
</p>

    git submodule update --init --recursive

<p class="verse">
2. 启动服务<br />
</p>

    ./test_run.sh


<a id="org281093f"></a>

# 运行demo

    git co demo && ./test_run.sh
