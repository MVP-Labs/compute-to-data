
# 在executor_runner.py里运行新进程python template.py?

# template里的大致内容如下：

# from executor_interface import executor

# use query/compute, script, args     script和args都已由exec_runner.py移动到具体目录下  

# executor.comm(query)

# parse_result = parse(args(包含compute) or  args + compute?)

# executor.compute(script, parse_result)   运行多方计算子进程

# script为前端数据科学家写的实际代码，以上做法使得他不需要写comm, 后端自动集成

if __name__ == '__main__':

    ## 可以接收query端口参数，用于运行comm
    ## 而compute端口参数，跟其他模型参数放在args.json里也行
    print('successful')