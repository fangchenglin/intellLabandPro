import random


class Rule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

    def match(self, facts):
        return self.condition(facts)

    def execute(self, facts):
        return self.action(facts)


class InferenceEngine:
    def __init__(self, rules):
        self.rules = rules

    def infer(self, facts):
        
        for rule in self.rules:
            if rule.match(facts):
                 rule.execute(facts)
                 matched = True
                 break
            


# 定义规则条件和动作
def condition_1(facts):
    east_west_ratio = facts['WECars'] / facts['TotalCars']
    return east_west_ratio == 0.5

def action_1(facts):
    facts['switchTime'] = 30

def condition_2(facts):
    east_west_ratio = facts['WECars'] / facts['TotalCars']
    return east_west_ratio > 0.5

def action_2(facts):
    facts['switchTime'] = 40

def condition_3(facts):
    east_west_ratio = facts['WECars'] / facts['TotalCars']
    return east_west_ratio < 0.5

def action_3(facts):
    facts['switchTime'] = 20


# 创建规则对象
rules = [
    Rule(condition_1, action_1),
    Rule(condition_2, action_2),
    Rule(condition_3, action_3)
]

# 创建推理引擎对象
inference_engine = InferenceEngine(rules)

# 定义初始车辆信息和绿灯时间
car_info = {
    'WECars': 30,
    'TotalCars': 60,
    'switchTime':30

}

# 进行推理
for minute in range(10):  # 模拟10分钟
    # 随机生成新的车辆数
    car_info['WECars'] = random.randint(0, 50)
    car_info['TotalCars'] = random.randint(0, 100)

    # 进行推理
    inference_engine.infer(car_info)

    # 输出结果
    print(f"Minute {minute+1}: Switch time for east-west direction - {car_info['switchTime']} seconds")

    # 等待1秒，模拟时间流逝
