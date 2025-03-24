from openai import OpenAI
import requests
import feedparser
import os
import datetime
from git import Repo

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# 1. 取得最新科技趨勢（從 Hacker News RSS）
def get_tech_news():
    url = "https://hnrss.org/frontpage"
    feed = feedparser.parse(url)
    top_articles = [entry["title"] for entry in feed.entries[:5]]
    return top_articles

# 2. 讓 AI 生成 Markdown 文章
def generate_blog_post(topic):
    prompt = f"請根據最新科技趨勢撰寫一篇技術部落格文章，主題：{topic}，格式為 Markdown"

    response = client.chat.completions.create(
        model="llama-3-8b-gpt-4o-ru1.0",
        messages=[{"role": "system", "content": "你是一個技術部落客，專門使用繁體中文撰寫最新科技趨勢文章。請不用把思考步驟寫出來，請以有趣幽默的口吻撰文"},
                  {"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# 3. 自動存成 Markdown 並 Git Push
def save_and_push_markdown(content, topic):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
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
        blog_topic = tech_news[0]  # 選第一個熱門趨勢
        print(f"獲取的主題是：{blog_topic}")
        blog_post = generate_blog_post(blog_topic)  # 產生文章
        save_and_push_markdown(blog_post, blog_topic)  # 存檔並 push
    else:
        print("未能獲取最新科技新聞")

