# test_run.py

from kimi_request import call_kimi
from prompt_builder import build_prompt

def main():
    with open("kb_text.txt", "r", encoding="utf-8") as f:
        kb_text = f.read()

    data_item = input("请输入要判断的数据项：")
    usage = input("请描述使用场景：")

    prompt = build_prompt(data_item, usage, kb_text)
    result = call_kimi(prompt)
    print("\n🧠 Kimi 判断结果如下：\n")
    print(result)

if __name__ == "__main__":
    main()
