# --- HEALY VECTOR LABS | SCORE ENGINE v1.2 ---
# TARGET: NHL PLAYOFF KINETIC ALPHA (SABRES SPECIAL)
import math
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from textblob import TextBlob

def apply_feds_decay(signal, timestamp):
    """FEDS Entropy: Signal rot via e^(-2t)"""
    t = (time.time() - timestamp) / 86400
    return signal * math.exp(-2 * t)

class SCORE_Engine:
    def __init__(self, team, opponent, p_round):
        self.team, self.opponent = team.upper(), opponent.upper()
        self.round = int(p_round)

    def audit_vectors(self):
        print(f"\n[!] IGNITING RSS PIPELINE FOR {self.team} VS {self.opponent}...")
        queries = [
            f"{self.team} vs {self.opponent} playoff",
            f"Ukko-Pekka Luukkonen Sabres",
            f"Tage Thompson 40 goals"
        ]
        headlines = []
        for q in queries:
            try:
                # Bypassing third-party libs to hit the raw XML feed directly
                url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    root = ET.fromstring(response.read())
                    # Grab top 5 fresh headlines per query
                    for item in root.findall('.//item/title')[:5]:
                        if item.text: headlines.append(item.text)
            except Exception as e:
                continue # If a feed drops, we keep moving
        
        if not headlines:
            print("[?] RSS feeds blocked. Using baseline sentiment.")
            return 0.5
        
        print(f"[+] Successfully pulled {len(headlines)} kinetic data points.")
        scores = [apply_feds_decay(TextBlob(h).sentiment.polarity, time.time()) for h in headlines]
        return round((sum(scores)/len(scores) + 1) / 2, 2)

    def get_dtm(self, tier):
        """VARIABLE 5: Dynamic Threat Multiplier"""
        intensity = 1.1 + (self.round * 0.05)
        tax = 0.15 if int(tier) == 1 else 0.05
        return round(intensity + tax, 2)

if __name__ == "__main__":
    print("\n--- SCORE ENGINE v1.2: RSS PIPELINE ---")
    t, o = input("TEAM (BUF): "), input("OPPONENT: ")
    r, tier = input("ROUND (1-4): "), input("OPPONENT TIER (1-2): ")
    
    engine = SCORE_Engine(t, o, r)
    sentiment = engine.audit_vectors()
    dtm = engine.get_dtm(tier)
    reality_floor = round(sentiment * dtm, 3)

    print(f"\n--- SCORE KINETIC ALPHA ---")
    print(f"MATCHUP: {t} vs {o} | DTM: {dtm}")
    print(f"REALITY FLOOR: {reality_floor}")
    
    if reality_floor > 0.85:
        print("VERDICT: HIGH STRIKE PROBABILITY (SABRES HEATER).")
    else:
        print("VERDICT: HOLD POSITION.")

