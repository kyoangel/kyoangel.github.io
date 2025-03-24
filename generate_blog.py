from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import datetime
from git import Repo

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# 目標網站 (Hacker News)
HN_URL = "https://news.ycombinator.com/"

def fetch_hn_articles():
    #"""爬取 Hacker News 首頁技術文章標題與連結"""
    response = requests.get(HN_URL, timeout=5)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.select(".athing"):
        title = item.select_one(".titleline a").text
        link = item.select_one(".titleline a")["href"]
        articles.append({"title": title, "link": link})

    return articles[:5]  # 取前 5 篇技術文章

def fetch_article_content(url):
    #"""爬取指定技術文章的內文"""
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 嘗試抓取 HTML 內的文字內容
    paragraphs = soup.find_all("p")
    content = "\n".join(p.text for p in paragraphs[:5])  # 取前 5 段內文

    return content if content else "無法擷取內容"

# 2. 讓 AI 生成 Markdown 文章
def generate_blog_post(topic, content):
    prompt = f"請根據以下技術標題與內文撰寫一篇詳細的技術文章：\n\n標題:{topic}\n\n內文： {content}，請用專業且流暢的語氣撰寫"

    response = client.chat.completions.create(
        model="llama-3-8b-gpt-4o-ru1.0",
        messages=[{"role": "system", "content": "請使用繁體中文而非簡體中文撰寫，最後寫上警語提醒是AI撰文"},
                  {"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# 3. 自動存成 Markdown 並 Git Push
def save_and_push_markdown(content, topic):
    topic = topic.replace('–','').replace(' ', '-').replace(':', '-').replace("--",'-').lower()
    date_str = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    filename = f"_posts/{date_str}-{topic}.md"

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
    articles = fetch_hn_articles()  # 取得科技趨勢
    if articles:
        # Get titles from the first three articles
        blog_topic = articles[0]["title"]  # Join titles with commas
        print(f"獲取的主題是：{blog_topic}")
        new_content = fetch_article_content(articles[0]["link"])
        blog_post = generate_blog_post(blog_topic, new_content)  # 產生文章
        save_and_push_markdown(blog_post, blog_topic)  # 存檔並 push
    else:
        print("未能獲取最新科技新聞")

