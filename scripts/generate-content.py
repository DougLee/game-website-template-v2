import requests
import json

def call_grok_api(prompt):
    """
    调用Grok API生成SEO数据
    """
    url = 'https://api.x.ai/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer xai-rdElRL5kW9VGE6dNGQ6IUOUZrglAVHiwk7wtdcevjY7VU2DP0Cu2Nts21q4RGfpyRTeWFolX0i4qdbIw'
    }
    data = {
        'messages': [
            {
                'role': 'system',
                'content': 'You are a SEO expert assistant.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'model': 'grok-2-latest',  # 请确认此模型名称是否正确
        'stream': False,
        'temperature': 0
    }
    
    try:
        # 设置超时：10秒连接超时，30秒读取超时
        response = requests.post(url, headers=headers, json=data, timeout=(10, 30))
        response.raise_for_status()  # 检查 HTTP 状态码（如 400, 401, 500 等）
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        # print(f"原始响应内容: {content}")  # 调试用，查看原始返回

        # 清理和验证返回的内容
        content = content.strip('`').strip()
        if content.startswith('json'):
            content = content.replace('json', '', 1).strip()
        
        # 尝试解析 JSON
        json.loads(content)
        return content
    
    except requests.exceptions.Timeout as e:
        print(f"API 调用超时: {str(e)}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 错误: {e.response.status_code} - {e.response.text}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {str(e)}，原始内容: {content}")
        return None
    except Exception as e:
        print(f"未知错误: {str(e)}")
        return None

# 测试调用
if __name__ == "__main__":
    prompt = "Generate a list of SEO keywords for a tech blog. 输出json格式"
    result = call_grok_api(prompt)
    if result:
        print(f"成功返回: {result}")