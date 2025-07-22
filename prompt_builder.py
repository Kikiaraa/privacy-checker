# prompt_builder.py

def build_prompt(data_item: str, usage: str, kb_text: str) -> str:
    prompt = f"""你是一个隐私合规助手。以下是知识库内容：
-----
{kb_text}
-----
现在用户提供了一个待判断的数据项和使用场景，请判断该项是否属于敏感个人信息，并说明理由。

【数据项】{data_item}
【使用场景】{usage}

请用简洁、专业的语言作答，分为以下两部分：
1.是否属于敏感个人信息（是/否/不确定）
2.理由。
"""
    return prompt
