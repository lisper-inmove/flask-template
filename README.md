
# Table of Contents

1.  [作用](#orgc37cd86)
2.  [结构说明](#org8e7f413)
3.  [安装protoc到Path](#org5235063)
4.  [保存bp](#org0bee7af)
5.  [启动服务](#org206c9ae)



<a id="orgc37cd86"></a>

# 作用

<p class="verse">
主要用于派生其它基于Flask的项目<br />
</p>


<a id="org8e7f413"></a>

# 结构说明

<p class="verse">
1. dao: 数据库交互层<br />
2. manager: 业务逻辑层,直接访问dao<br />
3. ctrl: 控制层,与manager对接，业务逻辑控制<br />
4. view: 视图层,与ctrl对接<br />
5. proto: protobuf保存目录<br />
6. submodules: git子模块保存目录<br />
7. gproto: gRPC的proto保存目录<br />
8. api: 对外提供的服务<br />
</p>


<a id="org5235063"></a>

# 安装protoc到Path

<p class="verse">
在 <https://github.com/protocolbuffers/protobuf/releases> 下载最新的protoc二进制文件<br />
</p>


<a id="org0bee7af"></a>

# 保存bp

<p class="verse">
将以下脚本保存在PATH路径下,取名为 bp，该脚本用于批量将protobuf文件转成py文件<br />
</p>

    #!/bin/bash
    ipath="."

    function walk_proto() {
        include_path=()
        for d in `find ${1}`
        do
            if [[ $d = $1 ]];then
                continue
            elif [[ -f $d ]];then
                 if [[ ${d##*.} = "proto" ]];then
                    c="protoc $d --python_out=. -I${ipath}"
                    for inc_path in ${include_path[@]};do
                        if [ -d $inc_path ];then
                            c="$c -I${inc_path}"
                        fi
                    done
                    `$c`
                    echo "$c ==> $?"
                fi
            elif [[ -d $d ]];then
                walk_proto $d
            fi
        done
    }

    function walk_gproto() {
        include_path=()
        for d in `find ${1}`
        do
            if [[ $d = $1 ]];then
                continue
            elif [[ -f $d ]];then
                 if [[ $d == *"api.proto" ]];then # 以api.proto结尾的
                    c="python -m grpc_tools.protoc --python_out=. --grpc_python_out=. $d -I${ipath}"
                    for inc_path in ${include_path[@]};do
                        if [ -d $inc_path ];then
                            c="$c -I${inc_path}"
                        fi
                    done
                    `$c`
                    echo "$c ==> $?"
                fi
            elif [[ -d $d ]];then
                walk_gproto $d
            fi
        done
    }

    paths=("./proto" "./api")
    for path in ${paths[@]}
    do
        if [ -d $path ];then
           walk_proto $path
        fi
    done

    paths=("./gproto" "./gapi")
    for path in ${paths[@]}
    do
        if [ -d $path ];then
           walk_gproto $path
        fi
    done


<a id="org206c9ae"></a>

# 启动服务

<p class="verse">
查看Makefile文件<br />
</p>
