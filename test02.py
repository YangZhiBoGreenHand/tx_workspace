class Rabbit:
    def __init__(self, month):
        self.month = month


def get_num(n, limit):
    sum = 0  # 已成熟
    temp = [Rabbit(1)]  # 未成熟

    while n > 0:
        for i in range(sum):
            temp.append(Rabbit(0))

        i = 0
        while i < len(temp):
            temp[i].month += 1
            if temp[i].month >= limit:
                sum += 1
                temp.pop(i)
            else:
                i += 1

        n -= 1

    return sum + len(temp)


months = 10
limit = 4
result = get_num(months, limit)
print(f"第 {months} 个月的兔子对数为 {result} 对")


def trap_rainwater(heights, widths):
    n = len(heights)
    if n <= 2:
        return 0

    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = heights[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], heights[i])

    right_max[n-1] = heights[n-1]
    for i in range(n-2, -1, -1):
        right_max[i] = max(right_max[i+1], heights[i])

    water = 0
    for i in range(n):
        level = min(left_max[i], right_max[i])
        if level > heights[i]:
            water += (level - heights[i]) * widths[i]

    return water


# 测试示例
height_width = [[0, 1], [3, 1], [0, 1], [4, 2], [3, 3], [0, 1],
                [7, 1], [6, 3], [5, 1], [4, 1], [9, 1], [0, 1], [7, 2]]
heights = [hw[0] for hw in height_width]
widths = [hw[1] for hw in height_width]
result = trap_rainwater(heights, widths)
print(f"能接到的雨水量为: {result}")
