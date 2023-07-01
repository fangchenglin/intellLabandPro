import tkinter as tk
from tkinter import ttk

class Rule:
    def __init__(self, condition, result):
        self.condition = condition
        self.result = result

class Fact:
    def __init__(self, value):
        self.value = value

class KnowledgeBase:
    def __init__(self):
        self.facts = []
        self.rules = []

    def declare(self, fact):
        self.facts.append(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def infer(self, fact):
        matching_rules = [rule for rule in self.rules if rule.condition == fact.value]

        if matching_rules:
            results = []
            for rule in matching_rules:
                for res in rule.result:
                    results.extend(self.infer(Fact(res)))
            return results
        else:
            return [fact]

def infer_result():
    letter = input_entry.get()
    results = kb.infer(Fact(letter))
    final_result = [fact.value for fact in results if isinstance(fact, Fact)]
    if final_result:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, final_result[-1])
    else:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "No result found.")

# 创建知识库
kb = KnowledgeBase()
kb.add_rule(Rule('A', ['B', 'C']))
kb.add_rule(Rule('B', ['D', 'E']))
kb.add_rule(Rule('C', ['F']))
kb.add_rule(Rule('D', ['G']))
kb.add_rule(Rule('E', ['H']))
kb.add_rule(Rule('F', ['I', 'J']))
kb.declare(Fact('A'))

# 创建图形界面
window = tk.Tk()
window.title("推理机")

# 设置样式
style = ttk.Style()
style.configure("TFrame", background="#f7f7f7")
style.configure("TButton", background="#e0e0e0", padding=10)
style.configure("TLabel", background="#f7f7f7", font=("Helvetica", 12))
style.configure("TEntry", padding=5, font=("Helvetica", 12))

# 创建框架
main_frame = ttk.Frame(window)
main_frame.pack(pady=20)

# 输入框
input_label = ttk.Label(main_frame, text="输入字母:")
input_label.grid(row=0, column=0, padx=10, pady=5)
input_entry = ttk.Entry(main_frame, width=20)
input_entry.grid(row=0, column=1, padx=10, pady=5)

# 推理按钮
infer_button = ttk.Button(main_frame, text="推理", command=infer_result)
infer_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# 结果文本框
result_label = ttk.Label(main_frame, text="推理结果:")
result_label.grid(row=2, column=0, padx=10, pady=5)
result_text = tk.Text(main_frame, height=2, width=20)
result_text.grid(row=2, column=1, padx=10, pady=5)

window.mainloop()
import tkinter as tk
from tkinter import ttk

class Rule:
    def __init__(self, condition, result):
        self.condition = condition
        self.result = result

class Fact:
    def __init__(self, value):
        self.value = value

class KnowledgeBase:
    def __init__(self):
        self.facts = []
        self.rules = []

    def declare(self, fact):
        self.facts.append(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def infer(self, fact):
        matching_rules = [rule for rule in self.rules if rule.condition == fact.value]

        if matching_rules:
            results = []
            for rule in matching_rules:
                for res in rule.result:
                    results.extend(self.infer(Fact(res)))
            return results
        else:
            return [fact]

def infer_result():
    letter = input_entry.get()
    results = kb.infer(Fact(letter))
    final_result = [fact.value for fact in results if isinstance(fact, Fact)]
    if final_result:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, final_result[-1])
    else:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "No result found.")

# 创建知识库
kb = KnowledgeBase()
kb.add_rule(Rule('A', ['B', 'C']))
kb.add_rule(Rule('B', ['D', 'E']))
kb.add_rule(Rule('C', ['F']))
kb.add_rule(Rule('D', ['G']))
kb.add_rule(Rule('E', ['H']))
kb.add_rule(Rule('F', ['I', 'J']))
kb.declare(Fact('A'))

# 创建图形界面
window = tk.Tk()
window.title("推理机")

# 设置样式
style = ttk.Style()
style.configure("TFrame", background="#f7f7f7")
style.configure("TButton", background="#e0e0e0", padding=10)
style.configure("TLabel", background="#f7f7f7", font=("Helvetica", 12))
style.configure("TEntry", padding=5, font=("Helvetica", 12))

# 创建框架
main_frame = ttk.Frame(window)
main_frame.pack(pady=20)

# 输入框
input_label = ttk.Label(main_frame, text="输入字母:")
input_label.grid(row=0, column=0, padx=10, pady=5)
input_entry = ttk.Entry(main_frame, width=20)
input_entry.grid(row=0, column=1, padx=10, pady=5)

# 推理按钮
infer_button = ttk.Button(main_frame, text="推理", command=infer_result)
infer_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# 结果文本框
result_label = ttk.Label(main_frame, text="推理结果:")
result_label.grid(row=2, column=0, padx=10, pady=5)
result_text = tk.Text(main_frame, height=2, width=20)
result_text.grid(row=2, column=1, padx=10, pady=5)

window.mainloop()
