"""
CHAPITRE 1.3 - PRÉSENTATION DES DONNÉES
Charge tous les datasets et affiche des statistiques.
Sauvegarde une figure dans rapport/figures/
"""

import os, sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)
DATA_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

datasets = {}

print("=" * 65)
print("1.3 PRÉSENTATION DES DONNÉES")
print("=" * 65)

# TENNIS
print("\n📁 TENNIS (source : Jeff Sackmann / tennis_atp & tennis_wta)")
try:
    atp_p = pd.read_csv(os.path.join(DATA_ROOT, "tennis", "atp_players_2024.csv"))
    atp_m = pd.read_csv(os.path.join(DATA_ROOT, "tennis", "atp_matches_2024.csv"))
    wta_p = pd.read_csv(os.path.join(DATA_ROOT, "tennis", "wta_players_2024.csv"))
    wta_m = pd.read_csv(os.path.join(DATA_ROOT, "tennis", "wta_matches_2024.csv"))
    print(f"  ATP – Joueurs : {len(atp_p):>5} | Matchs : {len(atp_m):>5}")
    print(f"  WTA – Joueurs : {len(wta_p):>5} | Matchs : {len(wta_m):>5}")
    print(f"  Surfaces ATP  : {sorted(atp_m['surface'].dropna().unique().tolist())}")
    print(f"  Tournois ATP  : {atp_m['tourney_name'].nunique()} tournois distincts")
    datasets["Tennis"] = {"joueurs": len(atp_p)+len(wta_p), "matchs": len(atp_m)+len(wta_m), "equipes": 0}
except Exception as e:
    print(f"  Erreur : {e}")

# FOOTBALL
print("\n📁 FOOTBALL (source : European Soccer Database / Kaggle)")
try:
    fp = pd.read_csv(os.path.join(DATA_ROOT, "football_european_leagues", "player.csv"))
    fm = pd.read_csv(os.path.join(DATA_ROOT, "football_european_leagues", "match.csv"))
    ft = pd.read_csv(os.path.join(DATA_ROOT, "football_european_leagues", "team.csv"))
    fl = pd.read_csv(os.path.join(DATA_ROOT, "football_european_leagues", "league.csv"))
    saisons = sorted(fm['season'].dropna().unique().tolist())
    print(f"  Joueurs : {len(fp):>5} | Matchs : {len(fm):>5} | Équipes : {len(ft):>5}")
    print(f"  Ligues  : {len(fl)} | Saisons : {saisons[0]} → {saisons[-1]}")
    datasets["Football"] = {"joueurs": len(fp), "matchs": len(fm), "equipes": len(ft)}
except Exception as e:
    print(f"  Erreur : {e}")

# BASKETBALL
print("\n📁 BASKETBALL (source : NBA Stats / Kaggle)")
try:
    bp = pd.read_csv(os.path.join(DATA_ROOT, "basketball", "basketball_player.csv"))
    bg = pd.read_csv(os.path.join(DATA_ROOT, "basketball", "basketball_game.csv"))
    bt = pd.read_csv(os.path.join(DATA_ROOT, "basketball", "basketball_team.csv"))
    print(f"  Joueurs : {len(bp):>5} | Matchs : {len(bg):>5} | Équipes : {len(bt):>5}")
    datasets["Basketball"] = {"joueurs": len(bp), "matchs": len(bg), "equipes": len(bt)}
except Exception as e:
    print(f"  Erreur : {e}")

# BADMINTON
print("\n📁 BADMINTON")
try:
    bap = pd.read_csv(os.path.join(DATA_ROOT, "badminton", "player.csv"))
    bam = pd.read_csv(os.path.join(DATA_ROOT, "badminton", "match.csv"))
    print(f"  Joueurs : {len(bap):>5} | Matchs : {len(bam):>5}")
    datasets["Badminton"] = {"joueurs": len(bap), "matchs": len(bam), "equipes": 0}
except Exception as e:
    print(f"  Erreur : {e}")

# VOLLEYBALL
print("\n📁 VOLLEYBALL (JO Paris 2024)")
try:
    vpw = pd.read_csv(os.path.join(DATA_ROOT, "volleyball", "volleyball_player_women.csv"))
    vpm = pd.read_csv(os.path.join(DATA_ROOT, "volleyball", "volleyball_player_men.csv"))
    vmw = pd.read_csv(os.path.join(DATA_ROOT, "volleyball", "volleyball_match_women.csv"))
    vmm = pd.read_csv(os.path.join(DATA_ROOT, "volleyball", "volleyball_match_men.csv"))
    print(f"  Joueuses (F) : {len(vpw):>4} | Joueurs (H) : {len(vpm):>4}")
    print(f"  Matchs (F)   : {len(vmw):>4} | Matchs (H)  : {len(vmm):>4}")
    datasets["Volleyball"] = {"joueurs": len(vpw)+len(vpm), "matchs": len(vmw)+len(vmm), "equipes": 0}
except Exception as e:
    print(f"  Erreur : {e}")

# Tableau récapitulatif
print("\n" + "=" * 65)
print(f"{'Sport':<15} {'Joueurs':>10} {'Matchs':>10} {'Équipes':>10}")
print("─" * 50)
for sport, s in datasets.items():
    print(f"{sport:<15} {s['joueurs']:>10,} {s['matchs']:>10,} {s['equipes']:>10,}")

# Figure
if datasets:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sports  = list(datasets.keys())
    joueurs = [datasets[s]["joueurs"] for s in sports]
    matchs  = [datasets[s]["matchs"]  for s in sports]
    colors  = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336']
    for ax, vals, titre in zip(axes, [joueurs, matchs],
                                ["Joueurs par sport", "Matchs par sport"]):
        ax.bar(sports, vals, color=colors)
        ax.set_title(titre)
        ax.tick_params(axis='x', rotation=15)
        for i, v in enumerate(vals):
            ax.text(i, v + max(vals)*0.01, f"{v:,}", ha='center', fontsize=9)
    plt.suptitle("Répartition des données", fontsize=14, fontweight='bold')
    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_01_3_donnees.png")
    plt.savefig(path, dpi=150, bbox_inches='tight')
    print(f"\n✅ Figure sauvegardée : {path}")
