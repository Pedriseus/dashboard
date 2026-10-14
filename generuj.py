import urllib.request
import json
import datetime

subreddits = ['Slovakia', 'Gunners']
html_subs = ""

for sub in subreddits:
    # Použijeme oficiálny JSON endpoint s dobrou User-Agent hlavičkou
    url = f"https://www.reddit.com/r/{sub}/top.json?t=day&limit=5&raw_json=1"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) DashboardBot/3.0'}
    )
    
    posts_html = ""
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            for child in data['data']['children']:
                p = child['data']
                if p.get('stickied'): continue
                title = p['title'].replace('"', '&quot;')
                permalink = f"https://www.reddit.com{p['permalink']}"
                score = p['score']
                comments = p['num_comments']
                
                posts_html += f'''
                <a href="{permalink}" target="_blank" class="block p-3 rounded-lg bg-slate-800/60 hover:bg-slate-800 border border-slate-700/50 transition flex justify-between items-start gap-3 mb-2">
                    <div class="space-y-1.5 flex-1 min-w-0">
                        <h4 class="text-white text-sm font-medium leading-snug hover:text-sky-400 transition">{title}</h4>
                        <div class="text-xs text-slate-400">💬 {comments} komentárov</div>
                    </div>
                    <div class="flex flex-col items-center justify-center min-w-[54px] py-1 px-2 rounded bg-slate-900 text-amber-400 font-bold text-xs shrink-0">
                        <span>▲</span>
                        <span>{score}</span>
                    </div>
                </a>
                '''
    except Exception as e:
        posts_html = f'''
        <div class="p-4 rounded-lg bg-red-950/40 border border-red-600/40 text-red-200 text-sm">
            Chyba sťahovania: {e}<br>
            <a href="https://www.reddit.com/r/{sub}/top/?t=day" target="_blank" class="text-sky-400 underline mt-2 inline-block">Otvoriť r/{sub} priamo ↗</a>
        </div>
        '''

    html_subs += f'''
    <div class="space-y-3">
        <div class="flex items-center justify-between border-b border-slate-700 pb-2">
            <h3 class="font-bold text-sky-400 text-lg">r/{sub}</h3>
            <span class="text-xs text-slate-400">Top 24h</span>
        </div>
        <div class="space-y-2">{posts_html}</div>
    </div>
    '''

with open("index.html", "r", encoding="utf-8") as f:
    template = f.read()

# Ak v index.html ešte nemáš placeholder, uistite sa, že tam je <!-- REDDIT_DATA_PLACEHOLDER -->
final_html = template.replace("<!-- REDDIT_DATA_PLACEHOLDER -->", html_subs)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("index.html bol úspešne vygenerovaný pythonom!")
