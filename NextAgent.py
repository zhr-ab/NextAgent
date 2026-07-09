from openai import OpenAI

client = OpenAI(api_key="", base_url="https://api.deepseek.com")

model=input("选择模型： deepseek-v4-pro, deepseek-V4-Flash\n")
thinking=input("是否启用思考模式: enabled, disabled\n")
messages=[{"role":"system", "content":input("请输入系统提示词\n")}]
while True: 
    messages.append({"role": "user", "content": input(">>")})
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        extra_body={"thinking": {"type": thinking}}
    ) 

    messages.append(response.choices[0].message)
    #校验
    message=[{"role":"system", "content":"你是一个审核员，负责审核用户说的是否正确，如果正确说：True,错误说：False,修改建议"},
             {"role": "user","content":messages[-1].content}]
    response = client.chat.completions.create(
        model=model,
        messages=message
    ) 
    m=response.choices[0].message
    if(m.content=="True"):
        print("审核通过\n")
        print(messages[-1].content)
    else:
        print(messages[-1].content+"\n")
        print(f"审核失败，原因：{str(m[-1].content).split(",")[1]}")
        while True:
            messages.append({"role": "user", "content": f"不对，{str(m[-1].content).split(",")[1]}"})
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                extra_body={"thinking": {"type": thinking}}
            ) 

            messages.append(response.choices[0].message)
            #校验
            message=[{"role":"system", "content":"你是一个审核员，负责审核用户说的是否正确，如果正确说：True,错误说：False,修改建议"},
                     {"role": "user","content":messages[-1].content}]
            response = client.chat.completions.create(
                model=model,
                messages=message
            ) 
            m=response.choices[0].message
            if(m.content=="True"):
                print("审核通过\n")
                print(messages[-1].content)
                break
