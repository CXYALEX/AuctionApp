from Crypto.Util import number
from sympy import Poly
from sympy.abc import x
from sympy.polys.domains import FF


# transmit a int to bit array, the most significant bit is arr[1], arr[0] is null
def int_to_bit_array(bid, max_length):
    # 将整数转换为二进制字符串，并去掉前缀 '0b'
    binary_string = bin(bid)[2:]
    bit_array = [0] * (max_length + 1)
    binary_string = reverse_binary_string(binary_string)
    l = len(binary_string)
    for i in range(l):
        bit_array[max_length - i] = int(binary_string[i])
    return bit_array


def bit_array_to_int(bit_array):
    binary_string = ''.join(str(bit) for bit in bit_array)
    decimal_value = int(binary_string, 2)
    return decimal_value


def reverse_binary_string(binary_string):
    # 将二进制字符串转换为整数
    decimal_value = int(binary_string, 2)

    # 计算反转后的整数值
    reversed_decimal = int(bin(decimal_value)[:1:-1], 2)

    # 将整数值转换回二进制字符串
    reversed_binary_string = bin(reversed_decimal)[2:].zfill(len(binary_string))

    return reversed_binary_string


def verify_generator(g, p, q):
    # 验证g的q次幂是否等于1（mod p）
    if pow(g, q, p) != 1:
        return False

    # 验证g的任何小于q的幂都不等于1（mod p）
    for i in range(1, q):
        if pow(g, i, p) == 1:
            return False

    return True


def generate_pedersen_params(bitsize=2048):
    # 生成大素数q
    q = number.getPrime(bitsize)
    # 生成大素数p，确保p-1是q的倍数
    p = 2 * q + 1
    while not number.isPrime(p):
        q = number.getPrime(bitsize)
        p = 2 * q + 1

    # 生成g，g是p的原根
    g = 0
    for i in range(2, p):
        if verify_generator(i, p, q):
            g = i

    # 随机选择h，使得h是g的一个高阶元素
    h = pow(g, number.getRandomRange(2, p - 1), p)
    print(f"p: {p}")
    print(f"q: {q}")
    print(f"g: {g}")
    print(f"h: {h}")
    return p, q, g, h


# 计算插值多项式(domain = ff(p))
def interpolate(points, p):
    # 初始化变量
    poly = Poly(0, x, domain=FF(p))

    # 对每个点进行拉格朗日插值
    for i in range(len(points)):
        xi, yi = points[i]

        # 计算基础多项式
        L = Poly(1, x, domain=FF(p))
        for j in range(len(points)):
            if i != j:
                xj, _ = points[j]
                L *= Poly(x - xj, x, domain=FF(p)) / (xi - xj)

        # 将基础多项式乘以对应的y值并加到总多项式上
        poly += Poly(yi, x, domain=FF(p)) * L
    return poly


# 计算插值多项式在点x处的取值(domain = ff(p))
def compute_value(poly, x_value, p):
    poly_value_at_x = poly.eval(x_value)
    # 返回简化后的多项式和x_value处的值
    return poly_value_at_x % p


if __name__ == '__main__':
    # 示例：将整数 42 转换为位数组
    bid = 13
    bit_array = int_to_bit_array(bid, 7)
    print(f"位数组表示为：{bit_array}")

    # p_value, q_value = setup(32)
    # print(f"p = {p_value}")
    # print(f"q = {q_value}")
