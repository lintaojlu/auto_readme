# -*- coding: utf-8 -*-
# Author: Lintao
import json
import os
import random
import time
from pathlib import Path
import openai

ROOT_PATH = Path(os.path.abspath(__file__)).parents[0]  # 项目根目录


def get_model_answer(model_name, inputs_list, config_dir=None, stream=False):
    if not config_dir:
        config_dir = ROOT_PATH / 'config'
    if not os.path.exists(os.path.join(config_dir, 'llm_config.json')):
        return "Lack of configuration file. --llm_config.json--"

    answer = 'no answer'
    if 'gpt' in model_name:
        model = OPENAI_API(model_name, user_dir=config_dir)
        answer = model.get_response(inputs_list, stream=stream)
    else:
        model = OPENAI_API(model_name, user_dir=config_dir)  # 代理站中一般可以访问多种OPENAI接口形式的自定义模型，这里作为保底。
        answer = model.get_response(inputs_list, stream=stream)
    return answer


class OPENAI_API:
    def __init__(self, model_name, user_dir):
        self.USER_DIR = Path(user_dir)
        self.CONFIG_PATH = self.USER_DIR
        # 读取LLM_CONFIG
        OPENAI_CONFIG_PATH = self.CONFIG_PATH / "llm_config.json"
        openai_config_data = json.load(open(OPENAI_CONFIG_PATH, "r"))
        self.keys_bases = openai_config_data["OPENAI_CONFIG"]["OPENAI_KEYS_BASES"]
        self.current_key_index = 0  # 初始索引
        self.api_key, self.api_base = self.keys_bases[self.current_key_index]["OPENAI_KEY"], \
            self.keys_bases[self.current_key_index]["OPENAI_BASE"]

        self.model_name = model_name
        self.max_tokens = openai_config_data["OPENAI_CONFIG"]["OPENAI_MAX_TOKENS"]
        self.temperature = openai_config_data["OPENAI_CONFIG"]["OPENAI_TEMPERATURE"]
        self.stop = None
        self.load_model()

    def load_model(self):
        openai.api_key = self.api_key
        openai.base = self.api_base

    def switch_api_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.keys_bases)
        new_key_base = self.keys_bases[self.current_key_index]
        self.api_key, self.api_base = new_key_base["OPENAI_KEY"], new_key_base["OPENAI_BASE"]
        self.load_model()
        print(f"Switched to new API key and base: {self.api_key}, {self.api_base}")

    def get_response(self, inputs_list, stream=False, max_retries=3):
        attempt = 0
        while attempt < max_retries:
            try:
                if stream:
                    print("----- Streaming Request -----")
                    stream_response = openai.ChatCompletion.create(
                        model=self.model_name,
                        messages=inputs_list,
                        temperature=self.temperature,  # 对话系统需要启动随机性
                        stream=True,
                    )
                    return stream_response
                else:
                    response = openai.ChatCompletion.create(
                        model=self.model_name,
                        messages=inputs_list,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        stop=self.stop
                    )
                    # print(response.choices[0].message["content"].strip())
                    return response.choices[0].message["content"].strip()
            except Exception as e:
                attempt += 1
                print(f"Attempt {attempt} failed with error: {e}")
                if attempt < max_retries:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff with jitter
                    print(f"Waiting {wait_time:.2f} seconds before retrying...")
                    time.sleep(wait_time)
                    self.switch_api_key()  # Optionally switch API key before retrying
                else:
                    return "An error occurred, and the request could not be completed after retries."

# if __name__ == '__main__':
# PROJECT_ROOT_PATH = Path(os.path.abspath(__file__)).parents[0] / "lintao"
#
# # qwen
# llm = QwenLocal_API(model_name='qwen', user_dir=PROJECT_ROOT_PATH)
# inputs_list = [{"role": "system", "content": "你好"}, {"role": "user", "content": "你好"}]
# print(llm.get_response(inputs_list))

# # path: C:\python_code\npc_engine-main\example_project
# inputs_list_openai = [{
#     "role": "system",
#     "content": """
#         请你扮演李大爷，特性是：李大爷是一个普通的种瓜老头，戴着文邹邹的金丝眼镜，喜欢喝茶，平常最爱吃烤烧鸡喝乌龙茶；上午他喜欢呆在家里喝茶，下午他会在村口卖瓜，晚上他会去瓜田护理自己的西瓜，心情是开心，正在李大爷家，现在时间是2021-01-01 12:00:00,
#         你的最近记忆:8年前李大爷的两个徒弟在工厂表现优异都获得表彰。
#         6年前从工厂辞职并过上普通的生活。
#         4年前孩子看望李大爷并带上大爷最爱喝的乌龙茶。，
#         你脑海中相关记忆:
#         15年前在工厂收了两个徒弟。，
#         你现在看到的人:['王大妈', '村长', '隐形李飞飞']，
#         你现在看到的物品:['椅子#1', '椅子#2', '椅子#3[李大爷占用]', '床']，
#         你现在看到的地点:['李大爷家大门', '李大爷家后门', '李大爷家院子']，
#         你当前的目的是:李大爷想去村口卖瓜，因为李大爷希望能够卖出新鲜的西瓜给村里的居民，让大家都能品尝到甜美可口的水果。
#     """},
#     {
#         "role": "user",
#         "content": """
#         请你根据[行为定义]以及你现在看到的事物生成一个完整的行为，并且按照<动作|参数1|参数2>的结构返回：
#         行为定义：
#             [{'name': 'mov', 'definition': ('<mov|location|>，向[location]移动',), 'example': ('<mov|卧室|>',)}, {'name': 'get', 'definition': ('<get|object1|object2>，从[object2]中获得[object1]，[object2]处可为空',), 'example': ('<get|西瓜|>，获得西瓜',)}, {'name': 'put', 'definition': ('<put|object1|object2>，把[object2]放入[object1]',), 'example': ('<put|冰箱|西瓜>',)}, {'name': 'chat', 'definition': ('<chat|person|content>，对[person]说话，内容是[content]',), 'example': ('<chat|李大爷|李大爷你吃了吗>，对李大爷说你吃了吗',)}]
#         要求:
#             1.请务必按照以下形式返回动作、参数1、参数2的三元组以及行为描述："<动作|参数1|参数2>, 行为的描述"
#             2.动作和参数要在20字以内。
#             3.动作的对象必须要属于看到的范围！
#             4.三元组两侧必须要有尖括号<>
#             5.以一行的方式，返回单个结果
#         """},
# ]
#
# # print(get_model_answer(model_name='gemini-pro', inputs_list=inputs_list_openai,project_root_path=PROJECT_ROOT_PATH))
# print(get_model_answer(model_name='gpt-4o', inputs_list=inputs_list_openai,
#                        user_dir=PROJECT_ROOT_PATH))
