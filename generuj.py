import urllib.request
import json
import datetime

# 1. Stiahneme poradie mini-ligy 28856
league_url = "https://fantasy.premierleague.com/api/leagues-classic/28856/standings/"
req_league = urllib.request.Request(
    league_url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) FPLBot/1.0'}
)

fpl_html = ""
try:
    with urllib.request.urlopen(req_league, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
        standings = data['standings']['results'][:5] # Top 5 tímov
        
        # Nájdeme index a body tvojho tímu Ødeargod
        my_team_idx = -1
        my_team_points = 0
        for idx, team in enumerate(standings):
            if team['entry_name'] == "Ødeargod":
                my_team_idx = idx
                my_team_points = team['total']
                break
        
        for idx, team in enumerate(standings, 1):
            team_name = team['entry_name']
            total_points = team['total']
            is_my_team = team_name == "Ødeargod"
            
            diff_text = ""
            if not is_my_team and my_team_idx != -1:
                diff = total_points - my_team_points
                if idx < my_team_idx + 1:
                    # Sú pred tebou (strata -> červená, napr. -9 b)
                    missing = total_points - my_team_points
                    diff_text = f'<span class="text-[10px] font-bold text-red-400 ml-1">(-{missing})</span>'
                else:
                    # Sú za tebou (náskok -> zelená, napr. +4 b)
                    ahead = my_team_points - total_points
                    diff_text = f'<span class="text-[10px] font-bold text-emerald-400 ml-1">(+{ahead})</span>'

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
                    <span class="text-slate-200">{idx}. {team_name} {diff_text}</span>
                    <span class="font-bold text-slate-300">{total_points} b</span>
                </div>
                '''
except Exception as e:
    fpl_html = f'<div class="text-xs text-amber-300 p-2">FPL dáta nedostupné</div>'

# 2. Stiahneme najbližší deadline
static_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
req_static = urllib.request.Request(
    static_url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) FPLBot/1.0'}
)

deadline_str = "Neznámy"
try:
    with urllib.request.urlopen(req_static, timeout=10) as response:
        static_data = json.loads(response.read().decode('utf-8'))
        for event in static_data['events']:
            if event['is_next']:
                dl_utc = datetime.datetime.strptime(event['deadline_time'], "%Y-%m-%dT%H:%M:%SZ")
                dl_sk = dl_utc + datetime.timedelta(hours=2)
                deadline_str = dl_sk.strftime("%d. %m. o %H:%M")
                break
except Exception:
    pass

fpl_html += f'''
<div class="mt-2 pt-2 border-t border-white/10 text-[11px] text-amber-300 flex justify-between items-center px-1">
    <span>⏳ Najbližší deadline:</span>
    <span class="font-bold text-white">{deadline_str}</span>
</div>
'''

# 3. Zápis do index.html
with open("index.html", "r", encoding="utf-8") as f:
    template = f.read()

final_html = template.replace("<!-- FPL_DATA_PLACEHOLDER -->", fpl_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("FPL Mini-liga s rozdielmi bodov úspešne aktualizovaná!")
