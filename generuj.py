import urllib.request
import json

# FPL API pre ligu ID 28856
url = "https://fantasy.premierleague.com/api/leagues-classic/28856/standings/"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) FPLBot/1.0'}
)

fpl_html = ""
try:
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
        standings = data['standings']['results'][:5] # Vezme Top 5 tímov
        
        for idx, team in enumerate(standings, 1):
            team_name = team['entry_name']
            total_points = team['total']
            is_my_team = team_name == "Ødeargod"
            
            if is_my_team:
                fpl_html += f'''
                <div class="flex justify-between items-center bg-[#EF0107]/50 border border-[#ff3b41] px-2.5 py-1.5 rounded shadow-sm">
                    <span class="font-bold text-white flex items-center gap-1.5">
                        <span>⭐</span> {idx}. {team_name}
                    </span>
                    <span class="font-black gold-text">{total_points} b</span>
                </div>
                '''
            else:
                fpl_html += f'''
                <div class="flex justify-between items-center bg-white/5 px-2.5 py-1.5 rounded">
                    <span class="text-slate-200">{idx}. {team_name}</span>
                    <span class="font-bold text-slate-300">{total_points} b</span>
                </div>
                '''
except Exception as e:
    fpl_html = f'<div class="text-xs text-amber-300 p-2">Nepodarilo sa načítať FPL: {e}</div>'

# Načítame index.html a nahradíme placeholder
with open("index.html", "r", encoding="utf-8") as f:
    template = f.read()

final_html = template.replace("<!-- FPL_DATA_PLACEHOLDER -->", fpl_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("FPL Mini-liga bola úspešne aktualizovaná!")
