from openai import OpenAI
import requests
import feedparser
import os
import datetime
from git import Repo

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# 1. 取得最新科技趨勢（從 Hacker News RSS）
def get_tech_news():
    rss_url = "https://hnrss.org/frontpage"
    feed = feedparser.parse(rss_url)
    
    articles = []
    
    for entry in feed.entries:
        item_id = entry.link.split("=")[-1]  # 從 link 取出 HN ID
        api_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        
        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            item_data = response.json()
            
            score = item_data.get("score", 0)  # 文章分數
            comments = item_data.get("descendants", 0)  # 評論數
            
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "score": score,
                "comments": comments
            })
        except requests.RequestException:
            continue  # 如果 API 請求失敗，跳過這篇文章
    
    # 依據分數 + 評論數排序，取前 5 名
    sorted_articles = sorted(articles, key=lambda x: (x["score"], x["comments"]), reverse=True)
    
    return sorted_articles[:5]

# 2. 讓 AI 生成 Markdown 文章
def generate_blog_post(topic):
    prompt = f"請根據最新科技趨勢撰寫一篇技術部落格文章，主題如下：{topic}，從中挑選一個合適的主題來撰文，格式為 Markdown"

    response = client.chat.completions.create(
        model="llama-3-8b-gpt-4o-ru1.0",
        messages=[{"role": "system", "content": "你是一個技術部落客，專門使用繁體中文而非簡體中文撰寫最新科技趨勢文章。請以有趣幽默的口吻撰文，最後寫上警語提醒是AI撰文"},
                  {"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# 3. 自動存成 Markdown 並 Git Push
def save_and_push_markdown(content, topic):
    date_str = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    filename = f"_posts/{date_str}-{topic.replace(' ', '-').lower()}.md"

    with open(filename, "w", encoding="utf-8") as f:
        markdown_head = f"---\nlayout: post\nauthor: KAI\ntitle: {topic}\ncategories: TechNotes News\n---\n"
        f.write(markdown_head)
        f.write(content)

    repo = Repo(".")
    repo.git.add("_posts/")
    repo.git.commit("-m", f"Auto-generated blog post: {topic}")
    repo.git.push("origin", "master")
   

# 執行流程
if __name__ == "__main__":
    tech_news = get_tech_news()  # 取得科技趨勢
    if tech_news:
        blog_topic = f"{tech_news[0]}, {tech_news[1], {tech_news[2]}}"  # 選第一個熱門趨勢
        print(f"獲取的主題是：{blog_topic}")
        blog_post = generate_blog_post(blog_topic)  # 產生文章
        save_and_push_markdown(blog_post, blog_topic)  # 存檔並 push
    else:
        print("未能獲取最新科技新聞")

