import time

import pytest

from PVSS import PVSS


def test_construct_LDEI_and_verify_LDEI(benchmark):
    start_time = time.time()
    generators = [62087002890306841792819976219620254928086660388,
                  222262993336593348232115899855000956074107185676,
                  669057394706137335297166195181244205263555743]  # 生成器列表
    m = len(generators)  # 生成器数量
    p = pow(2, 256) - 1  # 循环群G的大素数
    p_arr = [289721540117667154830115937543,
             328428904965001235767119458,
             367136269812335316704122980]  # p数组
    x_arr = []
    for i in range(m):
        x_arr.append(pow(generators[i], p_arr[i], p))
    print(x_arr)
    # 构造LDEI证明
    pvss = PVSS()
    proof = pvss.construct_LDEI(generators, m, p, p_arr, x_arr)

    # 验证LDEI证明
    result = pvss.verify_LDEI(generators, p, proof.x_arr, proof.a_arr, m, proof.e, proof.z_arr)
    print("result", result)
    assert result == True
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"execution_time：{execution_time} s")
    # self.assertTrue(result)


if __name__ == "__main__":
    pytest.main()
