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
        # Extract ID from comments URL instead of link
        comments_url = entry.comments
        item_id = comments_url.split("item?id=")[-1]
        api_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        
        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            item_data = response.json()
            
            if item_data is None:
                continue
                
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
    prompt = f"請根據 hacker news 中今天最熱門的文章標題：{topic}，來發想一個跟AI科技有關的文章，格式為 Markdown，請想像一下關於這個主題有可能運用到什麼AI技術應用，並嘗試給出可能的做法"

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
        # Get titles from the first three articles
        titles = [article["title"] for article in tech_news[:3]]
        blog_topic = titles[0]  # Join titles with commas
        print(f"獲取的主題是：{blog_topic}")
        blog_post = generate_blog_post(blog_topic)  # 產生文章
        save_and_push_markdown(blog_post, blog_topic)  # 存檔並 push
    else:
        print("未能獲取最新科技新聞")

