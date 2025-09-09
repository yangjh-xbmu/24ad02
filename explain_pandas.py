import os
from dotenv import load_dotenv
import requests
import json

def load_deepseek_api_key():
    """从.env文件加载DeepSeek API密钥"""
    load_dotenv()
    api_key = os.getenv('deepseek_api_key')
    if not api_key:
        raise ValueError("未找到DeepSeek API密钥，请检查.env文件")
    return api_key

def explain_pandas_with_deepseek(api_key):
    """使用DeepSeek API解释pandas库"""
    prompt = """请用中文详细解释Python的pandas库，包括：
1. pandas是什么以及它的主要用途
2. 核心数据结构（Series和DataFrame）
3. 常用的数据操作功能（读取数据、数据清洗、数据筛选、分组聚合等）
4. 常用的函数和方法
5. 实际应用场景和示例

请提供详细的解释和实用的代码示例。"""
    
    # 重试机制
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"第 {attempt + 1} 次尝试调用API...")
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'deepseek-chat',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.7,
                'max_tokens': 2000
            }
            
            # 增加超时时间
            response = requests.post('https://api.deepseek.com/v1/chat/completions', 
                                    headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.Timeout:
            if attempt == max_retries - 1:
                raise Exception("API调用超时，请检查网络连接")
            print("请求超时，正在重试...")
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"调用DeepSeek API时发生错误：{e}")
            print(f"发生错误：{e}，正在重试...")

def save_explanation_to_file(explanation):
    """将解释保存到文件"""
    with open('pandas_explanation.md', 'w', encoding='utf-8') as f:
        f.write("# Pandas库详细解释\n\n")
        f.write(explanation)
    print("解释已保存到 pandas_explanation.md")

def main():
    """主函数"""
    print("开始使用DeepSeek API解释pandas库...")
    
    try:
        # 加载API密钥
        api_key = load_deepseek_api_key()
        print("成功加载DeepSeek API密钥")
        
        # 调用API获取pandas解释
        print("正在调用DeepSeek API...")
        explanation = explain_pandas_with_deepseek(api_key)
        
        # 保存结果
        save_explanation_to_file(explanation)
        print("任务完成！")
        
    except Exception as e:
        print(f"错误：{e}")

if __name__ == "__main__":
    main()