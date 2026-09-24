import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# 1. Page Configuration & Custom Cinematic Dark Styling
st.set_page_config(page_title="Titan Broadcast Network", page_icon="🦖", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    h1 { color: #ff4b4b !important; font-family: 'Impact', sans-serif; letter-spacing: 2px; }
    .titan-card { border-left: 5px solid #ff4b4b; padding-left: 15px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦖 TITAN BROADCAST NETWORK")
st.markdown("### *Live Tracking Feed: Godzilla & The Monsters of the MonsterVerse*")

# 2. Sidebar Filters
TITANS = ["All Titans", "Godzilla", "Kong", "Mothra", "Rodan", "King Ghidorah", "Tiamat", "Scylla", "Mechagodzilla"]
selected_titan = st.sidebar.selectbox("🎯 Target Specific Titan:", TITANS)
search_keyword = st.sidebar.text_input("🔍 Search Intel Keywords:", "").lower()

# 3. Web Scraper (Optimised for Online Servers using Standard Headers)
@st.cache_data(ttl=900) # Caches data for 15 minutes to stay fast and avoid blocking
def fetch_monster_news():
    articles = []
    url = "https://google.com"
    
    # Fake a standard browser header so the online server isn't instantly rejected
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all("item")
        
        for item in items:
            title = item.title.text if item.title else "Unknown Report"
            link = item.link.text if item.link else "#"
            pub_date = item.pubDate.text if item.pubDate else ""
            source = item.source.text if item.source else "Monarch Database"
            
            clean_title = re.sub(r'\s-\s.*$', '', title)
            
            articles.append({
                "title": clean_title,
                "link": link,
                "date": pub_date,
                "source": source
            })
    except Exception as e:
        st.error(f"Error intercepting Monarch communications: {e}")
        
    return articles

# 4. Processing Feed Data
raw_articles = fetch_monster_news()
filtered_articles = []

monster_keywords = ["godzilla", "kong", "titan", "kaiju", "mothra", "rodan", "ghidorah", "monsterverse", "gxg"]

for art in raw_articles:
    title_lower = art["title"].lower()
    
    if not any(kw in title_lower for kw in monster_keywords):
        continue
    if selected_titan != "All Titans" and selected_titan.lower() not in title_lower:
        continue
    if search_keyword and search_keyword not in title_lower:
        continue
        
    filtered_articles.append(art)

# 5. Display News
if not filtered_articles:
    st.info("⚠️ No active Titan signatures detected matching your filter criteria.")
else:
    st.sidebar.metric(label="Active Visual Signatures", value=len(filtered_articles))
    
    for article in filtered_articles:
        st.markdown(f'<div class="titan-card">', unsafe_allow_html=True)
        st.markdown(f"### 🔴 [{article['title']}]({article['link']})")
        st.caption(f"**Source:** {article['source']} | **Intercepted:** {article['date']}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")

st.sidebar.markdown("---")
st.sidebar.caption(f"Monarch Outpost Sensor Status: **ONLINE**")
st.sidebar.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
