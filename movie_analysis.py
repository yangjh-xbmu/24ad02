import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import requests
import json
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 加载环境变量
load_dotenv()
DEEPSEEK_API_KEY = os.getenv('deepseek_api_key')

def read_movie_data():
    """读取电影数据文件"""
    try:
        file_path = os.path.join('data', 'movie_data_cleaned.csv')
        df = pd.read_csv(file_path)
        print(f"成功读取数据，共{len(df)}条记录")
        return df
    except FileNotFoundError:
        print("错误：找不到数据文件")
        return None
    except Exception as e:
        print(f"读取数据时发生错误：{e}")
        return None

def analyze_movie_data(df):
    """分析电影数据，返回评分最高的10部电影"""
    if df is None:
        return None
    
    # 数据清洗：去除空值，确保评分列是数值类型
    df_clean = df.dropna(subset=['average'])
    df_clean['average'] = pd.to_numeric(df_clean['average'], errors='coerce')
    df_clean = df_clean.dropna(subset=['average'])
    
    # 按评分从高到低排序
    top_movies = df_clean.sort_values('average', ascending=False).head(10)
    return top_movies

def plot_top_movies(top_movies):
    """绘制评分最高的10部电影柱状图"""
    plt.figure(figsize=(12, 8))
    
    # 创建柱状图
    bars = plt.bar(range(len(top_movies)), top_movies['average'], 
                   color=plt.cm.viridis(range(len(top_movies))))
    
    # 设置标题和标签
    plt.title('评分最高的10部电影', fontsize=16, fontweight='bold')
    plt.xlabel('电影排名', fontsize=12)
    plt.ylabel('评分', fontsize=12)
    
    # 设置x轴标签
    plt.xticks(range(len(top_movies)), [f"第{i+1}名" for i in range(len(top_movies))], rotation=45)
    
    # 在每个柱子上添加数值标签
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.1f}', ha='center', va='bottom', fontsize=10)
    
    # 添加图例
    movie_titles = [f"{title[:15]}..." if len(title) > 15 else title 
                   for title in top_movies['title']]
    plt.legend(bars, movie_titles, title="电影名称", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('top_movies_plot.png', dpi=300, bbox_inches='tight')
    plt.show()

def get_movie_introduction(movie_info, api_key):
    """使用DeepSeek API获取电影介绍"""
    if not api_key:
        print("警告：未找到DeepSeek API密钥")
        return "无法获取电影介绍：缺少API密钥"
    
    prompt = f"请用中文详细介绍这部电影：{movie_info['title']}。"
    if 'country' in movie_info and pd.notna(movie_info['country']):
        prompt += f" 国家：{movie_info['country']}"
    if 'genre' in movie_info and pd.notna(movie_info['genre']):
        prompt += f" 类型：{movie_info['genre']}"
    if 'release_date' in movie_info and pd.notna(movie_info['release_date']):
        prompt += f" 上映日期：{movie_info['release_date']}"
    
    prompt += "。请提供电影的剧情简介、主要演员、导演信息以及为什么这部电影评分如此之高。"
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.7,
            'max_tokens': 1000
        }
        
        response = requests.post('https://api.deepseek.com/v1/chat/completions', 
                                headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
        
    except Exception as e:
        print(f"调用DeepSeek API时发生错误：{e}")
        return f"无法获取电影介绍：{str(e)}"

def main():
    """主函数"""
    print("开始电影数据分析...")
    
    # 读取数据
    df = read_movie_data()
    if df is None:
        return
    
    # 分析数据
    top_movies = analyze_movie_data(df)
    if top_movies is None or len(top_movies) == 0:
        print("没有找到有效的电影数据")
        return
    
    print("\n评分最高的10部电影：")
    print(top_movies[['title', 'average', 'country', 'release_date']].to_string(index=False))
    
    # 绘制图表
    plot_top_movies(top_movies)
    print("图表已保存为 top_movies_plot.png")
    
    # 获取评分最高电影的详细介绍
    best_movie = top_movies.iloc[0]
    print(f"\n正在获取评分最高电影的详细介绍：{best_movie['title']}")
    
    introduction = get_movie_introduction(best_movie, DEEPSEEK_API_KEY)
    
    # 写入intro.md文件
    with open('intro.md', 'w', encoding='utf-8') as f:
        f.write(f"# {best_movie['title']} 详细介绍\n\n")
        f.write(f"**评分**: {best_movie['average']}\n")
        f.write(f"**国家**: {best_movie.get('country', '未知')}\n")
        f.write(f"**类型**: {best_movie.get('genre', '未知')}\n")
        f.write(f"**上映日期**: {best_movie.get('release_date', '未知')}\n")
        f.write(f"**投票数**: {best_movie.get('votes', '未知')}\n\n")
        f.write("## 电影介绍\n\n")
        f.write(introduction)
    
    print("电影介绍已保存到 intro.md")

if __name__ == "__main__":
    main()