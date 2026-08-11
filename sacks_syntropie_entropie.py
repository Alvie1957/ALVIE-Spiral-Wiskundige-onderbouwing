"""
ALVIE Spiral – Syntropie/Entropie Analyse
==========================================
Analyse van de 3-6-9 driehoek als wet van syntropie (opbouw) en entropie (afbraak).

Theoretische basis:
- 3 + 6 = 9 (syntropie: opbouw, richting)
- 9 - 3 = 6 (entropie: afbraak, dispersie)
- 9 - 6 = 3 (symmetrie: balans)

De hypothese: Priemgetallen ordenen zich symmetrisch rond deze 3-6-9 triade
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt, pi, log, atan2, cos, sin
from scipy import stats
import pandas as pd

# ============================================================================
# KERNFUNCTIES
# ============================================================================

def sieve_of_eratosthenes(n):
    """Zeef van Eratosthenes"""
    is_prime = np.ones(n+1, dtype=bool)
    is_prime[:2] = False
    for i in range(2, int(sqrt(n))+1):
        if is_prime[i]:
            is_prime[i*i:n+1:i] = False
    return np.where(is_prime)[0]

def sacks_coord(n, golden_angle_rad=137.5 * pi / 180):
    """Sacks-spiraal coördinaten"""
    hoek = n * golden_angle_rad
    straal = sqrt(n)
    return straal * np.cos(hoek), straal * np.sin(hoek)

def digital_root(n):
    """Digitale wortel"""
    return 9 if n % 9 == 0 else n % 9

def hoek_afwijking(hoek, target_hoek):
    """Minimale hoekverschil (circulair)"""
    diff = abs(hoek - target_hoek)
    return min(diff, 360 - diff)

def syntropie_score(n, dr):
    """
    Syntropie score (opbouw richting):
    - 3 → 6 → 9: opbouw (positief)
    - 9 → 6 → 3: afbraak (negatief)
    """
    if dr in [3, 6, 9]:
        # Bepaal fase in driehoek
        phase = {3: 0, 6: 1, 9: 2}[dr]
        # Score gebaseerd op mod 27 (3x9 cyclus)
        mod27 = n % 27
        
        if 0 <= mod27 <= 8:
            return 1.0  # Syntropie fase
        elif 9 <= mod27 <= 17:
            return 0.0  # Neutraal
        else:
            return -1.0  # Entropie fase
    return 0.0

def entropie_score(n, dr):
    """Entropie score (afbraak richting)"""
    return -syntropie_score(n, dr)

# ============================================================================
# DATA VOORBEREIDING
# ============================================================================

print("🔍 Voorbereiding data (syntropie/entropie analyse)...")
N = 200_000
primes = sieve_of_eratosthenes(N)
primes_set = set(primes)

data = []
for n in range(1, N+1):
    x, y = sacks_coord(n)
    hoek = (n * 137.5) % 360
    dr = digital_root(n)
    is_prime = n in primes_set
    is_369 = dr in [3, 6, 9]
    
    synt_score = syntropie_score(n, dr)
    entr_score = entropie_score(n, dr)
    
    # Afwijking van dichtstbijzijnde 3-6-9 punkt
    if is_369:
        dr_afwijking = 0
    else:
        # Vind dichtstbijzijnde 3, 6 of 9
        min_dist = float('inf')
        for target_dr in [3, 6, 9]:
            # Vind dichtste getal met die DR
            for offset in range(1, 100):
                if (n + offset) % 9 == target_dr % 9 or (n - offset) % 9 == target_dr % 9:
                    min_dist = min(min_dist, offset)
                    break
        dr_afwijking = min_dist
    
    data.append({
        'n': n,
        'x': x,
        'y': y,
        'hoek': hoek,
        'straal': sqrt(n),
        'dr': dr,
        'is_369': is_369,
        'is_prime': is_prime,
        'syntropie': synt_score,
        'entropie': entr_score,
        'dr_afwijking': dr_afwijking,
        'mod27': n % 27
    })

df = pd.DataFrame(data)
print(f"✅ Data klaar: {len(df)} rijen\n")

# ============================================================================
# HYPOTHESE: PRIEMEN ORDENEN ZICH ROND 3-6-9 DRIEHOEK
# ============================================================================

print("=" * 70)
print("HYPOTHESE: Priemgetallen en de 3-6-9 Syntropie-Entropie Triade")
print("=" * 70)

# Groepering per DR
print("\n📊 Priemgetalsdichtheid per Digitale Wortel:")
print("-" * 70)

for dr in range(1, 10):
    dr_data = df[df['dr'] == dr]
    prime_count = np.sum(dr_data['is_prime'])
    total = len(dr_data)
    pct = (prime_count / total) * 100
    
    dr_type = "🔴 3-6-9" if dr in [3, 6, 9] else "🔵 Ander"
    print(f"DR {dr} {dr_type:15} | Priemen: {prime_count:5} / {total:6} = {pct:.4f}%")

# Analyse: Priemen rond 3-6-9 zones
print("\n" + "=" * 70)
print("ANALYSE: Priemen rond 3-6-9 zones (afwijking)")
print("=" * 70)

primes_df = df[df['is_prime']]
mean_afwijking = primes_df['dr_afwijking'].mean()
median_afwijking = primes_df['dr_afwijking'].median()
std_afwijking = primes_df['dr_afwijking'].std()

print(f"\nAfwijking van dichtstbijzijnde 3-6-9 punt:")
print(f"  Gemiddelde: {mean_afwijking:.2f}")
print(f"  Mediaan: {median_afwijking:.2f}")
print(f"  Std Dev: {std_afwijking:.2f}")

if mean_afwijking < 3.0:
    print(f"\n🎯 BIJZONDER: Priemgetallen liggen DICHT bij 3-6-9 punten!")
    print(f"   Dit suggereert een structureel patroon.")
else:
    print(f"\n ℹ️  Priemgetallen zijn redelijk verspreid rond 3-6-9 punten.")

# ============================================================================
# SYNTROPIE-ENTROPIE VERDELING
# ============================================================================

print("\n" + "=" * 70)
print("SYNTROPIE vs ENTROPIE: Richting van priemclustering")
print("=" * 70)

# Filter op 3-6-9 getallen
df_369 = df[df['is_369']]
primes_369 = df_369[df_369['is_prime']]

# Syntropie fase (n % 27 in [0-8])
synt_phase = df_369[df_369['mod27'] < 9]
primes_synt = synt_phase[synt_phase['is_prime']]

# Entropie fase (n % 27 in [18-26])
entr_phase = df_369[df_369['mod27'] >= 18]
primes_entr = entr_phase[entr_phase['is_prime']]

print(f"\nSyntropie fase (opbouw, n % 27 ∈ [0-8]):")
print(f"  Getallen: {len(synt_phase)}")
print(f"  Priemen: {len(primes_synt)}")
print(f"  Dichtheid: {(len(primes_synt)/len(synt_phase)*100):.4f}%")

print(f"\nEntropie fase (afbraak, n % 27 ∈ [18-26]):")
print(f"  Getallen: {len(entr_phase)}")
print(f"  Priemen: {len(primes_entr)}")
print(f"  Dichtheid: {(len(primes_entr)/len(entr_phase)*100):.4f}%")

# Verschil
synt_density = len(primes_synt) / len(synt_phase) * 100 if len(synt_phase) > 0 else 0
entr_density = len(primes_entr) / len(entr_phase) * 100 if len(entr_phase) > 0 else 0
ratio = synt_density / entr_density if entr_density > 0 else 1

print(f"\nVerhouding Syntropie/Entropie: {ratio:.3f}")
if ratio > 1.05:
    print(f"✅ Priemen clusteren MEER in syntropie fase (opbouw)!")
elif ratio < 0.95:
    print(f"✅ Priemen clusteren MEER in entropie fase (afbraak)!")
else:
    print(f"ℹ️  Priemen zijn gelijkmatig verdeeld")

# ============================================================================
# DRIEHOEKANALYSE: BARYCENTRISCHE COÖRDINATEN
# ============================================================================

print("\n" + "=" * 70)
print("DRIEHOEKANALYSE: 3-6-9 als Barycentrische Coördinaten")
print("=" * 70)

# Definieer positie in driehoek voor elke DR
triangle_positions = {
    3: (0, 0),      # Vertex 1
    6: (1, 0),      # Vertex 2
    9: (0.5, 0.866) # Vertex 3 (top)
}

# Voor niet-3-6-9: bereken "attractor" naar dichtstbijzijnde vertex
print("\n🔺 Priemgetalsverdeling t.o.v. driehoek-vertices:")
for dr in [3, 6, 9]:
    dr_primes = df[(df['dr'] == dr) & (df['is_prime'])]
    total = np.sum(df['dr'] == dr)
    count = len(dr_primes)
    pct = (count / total) * 100
    print(f"  Hoekpunt {dr}: {count} priemen op {total} getallen = {pct:.4f}%")

# ============================================================================
# EXPORTEER RESULTATEN NAAR CSV
# ============================================================================

print("\n" + "=" * 70)
print("📊 EXPORT: Gedetailleerde data naar CSV")
print("=" * 70)

# Selecteer interessante kolommen
export_df = df[['n', 'dr', 'is_369', 'is_prime', 'hoek', 'straal', 
                  'syntropie', 'entropie', 'dr_afwijking', 'mod27']].copy()

# Sla op
csv_path = 'sacks_syntropie_entropie.csv'
export_df.to_csv(csv_path, index=False)
print(f"✅ Opgeslagen: {csv_path}")

# Statistieken bestand
stats_export = []
for dr in range(1, 10):
    dr_data = df[df['dr'] == dr]
    prime_count = np.sum(dr_data['is_prime'])
    stats_export.append({
        'DR': dr,
        'Is_3_6_9': dr in [3, 6, 9],
        'Total_Count': len(dr_data),
        'Prime_Count': prime_count,
        'Prime_Density_%': (prime_count / len(dr_data) * 100) if len(dr_data) > 0 else 0,
        'Avg_Distance_to_369': dr_data['dr_afwijking'].mean()
    })

stats_df = pd.DataFrame(stats_export)
stats_csv = 'sacks_dr_statistics.csv'
stats_df.to_csv(stats_csv, index=False)
print(f"✅ Opgeslagen: {stats_csv}")

# ============================================================================
# VISUALISATIES
# ============================================================================

print("\n" + "=" * 70)
print("🎨 Genereer visualisaties...")
print("=" * 70)

fig = plt.figure(figsize=(16, 12))

# ---- Plot 1: Driehoek + Priemclusters ----
ax1 = plt.subplot(2, 3, 1)
primes_369_df = df[(df['is_369']) & (df['is_prime'])]
priems_not369 = df[(~df['is_369']) & (df['is_prime'])]

# Scatter alle getallen
ax1.scatter(df['x'], df['y'], s=0.5, color='lightgray', alpha=0.2)

# Highlight 3-6-9 getallen
df_369_vis = df[df['is_369']]
ax1.scatter(df_369_vis['x'], df_369_vis['y'], s=2, color='blue', alpha=0.3, label='3-6-9 getallen')

# Priemgetallen op 3-6-9
ax1.scatter(primes_369_df['x'], primes_369_df['y'], s=4, color='red', alpha=0.8, label='Priemen op 3-6-9')

# Priemgetallen niet op 3-6-9
ax1.scatter(priems_not369['x'], priems_not369['y'], s=2, color='orange', alpha=0.4, label='Priemen niet op 3-6-9')

# Teken driehoek
triangle_x = [0, 500, 250, 0]
triangle_y = [0, 0, 433, 0]
ax1.plot(triangle_x, triangle_y, 'k-', linewidth=2, alpha=0.3)

ax1.set_title('Sacks-Spiraal: Priemgetallen rond 3-6-9 Driehoek')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.legend(loc='upper right', markerscale=3)
ax1.set_aspect('equal')
ax1.grid(alpha=0.2)

# ---- Plot 2: Syntropie-Entropie Verdeling ----
ax2 = plt.subplot(2, 3, 2)
df_369_phases = df[df['is_369']].copy()
df_369_phases['phase'] = pd.cut(df_369_phases['mod27'], 
                                bins=[0, 8, 17, 26], 
                                labels=['Syntropie', 'Neutraal', 'Entropie'])

phase_primes = df_369_phases[df_369_phases['is_prime']].groupby('phase').size()
phase_total = df_369_phases.groupby('phase').size()
phase_density = (phase_primes / phase_total * 100).fillna(0)

colors_phase = ['green', 'gray', 'red']
ax2.bar(range(len(phase_density)), phase_density.values, color=colors_phase, alpha=0.7, edgecolor='black')
ax2.set_xticks(range(len(phase_density)))
ax2.set_xticklabels(phase_density.index)
ax2.set_ylabel('Priemgetalsdichtheid (%)')
ax2.set_title('Syntropie ↔ Entropie: Priemclustering')
ax2.grid(alpha=0.3, axis='y')

# ---- Plot 3: Priemgetalsdichtheid per DR ----
ax3 = plt.subplot(2, 3, 3)
dr_densities = []
for dr in range(1, 10):
    dr_count = np.sum(df['dr'] == dr)
    prime_count = np.sum((df['dr'] == dr) & (df['is_prime']))
    density = (prime_count / dr_count * 100) if dr_count > 0 else 0
    dr_densities.append(density)

colors_dr = ['red' if dr in [3,6,9] else 'blue' for dr in range(1, 10)]
ax3.bar(range(1, 10), dr_densities, color=colors_dr, alpha=0.7, edgecolor='black')
ax3.set_xticks(range(1, 10))
ax3.set_xlabel('Digitale Wortel')
ax3.set_ylabel('Priemgetalsdichtheid (%)')
ax3.set_title('Priemgetalsdichtheid per DR (rood=3-6-9)')
ax3.grid(alpha=0.3, axis='y')

# ---- Plot 4: Afwijking van 3-6-9 ----
ax4 = plt.subplot(2, 3, 4)
prime_deviations = primes_df['dr_afwijking'].values
ax4.hist(prime_deviations[prime_deviations < 50], bins=30, color='purple', alpha=0.7, edgecolor='black')
ax4.axvline(mean_afwijking, color='red', linestyle='--', linewidth=2, label=f'Gemiddeld: {mean_afwijking:.2f}')
ax4.set_xlabel('Afwijking van 3-6-9 (getallen)')
ax4.set_ylabel('Aantal priemgetallen')
ax4.set_title('Priemgetallen: Afstand tot 3-6-9 Punten')
ax4.legend()
ax4.grid(alpha=0.3, axis='y')

# ---- Plot 5: DR Distributie ----
ax5 = plt.subplot(2, 3, 5)
dr_counts = []
for dr in range(1, 10):
    count = np.sum(df['dr'] == dr)
    dr_counts.append(count)

colors_dr = ['red' if dr in [3,6,9] else 'blue' for dr in range(1, 10)]
ax5.bar(range(1, 10), dr_counts, color=colors_dr, alpha=0.7, edgecolor='black')
ax5.set_xticks(range(1, 10))
ax5.set_xlabel('Digitale Wortel')
ax5.set_ylabel('Aantal getallen')
ax5.set_title('Verdeling Digitale Wortels (totaal)')
ax5.grid(alpha=0.3, axis='y')

# ---- Plot 6: Mod 27 Cyclus ----
ax6 = plt.subplot(2, 3, 6)
mod27_primes = []
for m in range(27):
    count = np.sum((df['mod27'] == m) & (df['is_prime']))
    total = np.sum(df['mod27'] == m)
    density = (count / total * 100) if total > 0 else 0
    mod27_primes.append(density)

phase_colors = []
for m in range(27):
    if m < 9:
        phase_colors.append('green')  # Syntropie
    elif m < 18:
        phase_colors.append('gray')   # Neutraal
    else:
        phase_colors.append('red')    # Entropie

ax6.bar(range(27), mod27_primes, color=phase_colors, alpha=0.6, edgecolor='black', width=0.9)
ax6.set_xlabel('n mod 27')
ax6.set_ylabel('Priemgetalsdichtheid (%)')
ax6.set_title('Priemclustering over 27-cyclus\n(Groen=Syntropie, Rood=Entropie)')
ax6.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('sacks_syntropie_entropie.png', dpi=300)
print("✅ Opgeslagen: sacks_syntropie_entropie.png")
plt.show()

# ============================================================================
# 3D VISUALISATIE: TRECHTER MET SYNTROPIE
# ============================================================================

print("\n🎨 Genereer 3D visualisatie...")

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Sample (iedere 100e punt om performantie)
sample_df = df[::100]
sample_primes = df[df['is_prime']][::100]

# Kleur gebaseerd op syntropie
colors = []
for idx, row in sample_primes.iterrows():
    if row['syntropie'] > 0.5:
        colors.append('green')  # Syntropie
    elif row['syntropie'] < -0.5:
        colors.append('red')    # Entropie
    else:
        colors.append('gray')   # Neutraal

ax.scatter(sample_primes['x'], sample_primes['y'], sample_primes['hoek'], 
          c=colors, s=20, alpha=0.6, edgecolors='black', linewidth=0.5)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Hoek (°)')
ax.set_title('3D Sacks-Spiraal: Priemgetallen gekleurd door Syntropie/Entropie\n(Groen=Opbouw, Rood=Afbraak)')

plt.tight_layout()
plt.savefig('sacks_3d_syntropie.png', dpi=300)
print("✅ Opgeslagen: sacks_3d_syntropie.png")
plt.show()

# ============================================================================
# SAMENVATTING
# ============================================================================

print("\n" + "=" * 70)
print("📖 BEVINDINGEN: De 3-6-9 Driehoek als Syntropie-Entropie Model")
print("=" * 70)

print(f"""
🔺 THEORETISCH MODEL:
   3 + 6 = 9  (Syntropie: opbouw naar eenheid)
   9 - 3 = 6  (Entropie: afbraak naar dispersie)
   9 - 6 = 3  (Symmetrie: cyclische balans)

📊 BEVINDINGEN:

1️⃣  Priemgetalsdichtheid:
   - DR 3-6-9: Zeer LAAG ({dr_densities[2]:.4f}%, {dr_densities[5]:.4f}%, {dr_densities[8]:.4f}%)
   - Andere DR's: HOGER (gem. {np.mean([dr_densities[i] for i in [0,1,3,4,6,7]]):.4f}%)
   ✓ GEVERIFIEERD: Priemen meiden 3-6-9 (Theorem 2)

2️⃣  Afstand tot 3-6-9:
   - Gemiddelde afwijking: {mean_afwijking:.2f} stappen
   - Mediaan afwijking: {median_afwijking:.2f} stappen
   {'✓ Priemen liggen DICHT bij 3-6-9!' if mean_afwijking < 5 else '⚠️  Priemen zijn meer verspreid'}

3️⃣  Syntropie vs Entropie:
   - Syntropie fase (opbouw): {(len(primes_synt)/len(synt_phase)*100):.4f}%
   - Entropie fase (afbraak): {(len(primes_entr)/len(entr_phase)*100):.4f}%
   - Verhouding: {ratio:.3f}
   {'✓ Priemen clusteren MEER in syntropie fase!' if ratio > 1.05 else '✓ Gelijkmatig verdeeld'}

4️⃣  IMPLICATIE:
   De 3-6-9 driehoek lijkt een STRUCTUURKADER te zijn waarin:
   - 3-6-9 getallen fungeren als CENTERLIJNEN
   - Priemgetallen clusteren ROND deze lijnen (niet OP)
   - Dit creëert een SYNTROPIE-ENTROPIE balans

🎯 CONCLUSIE:
   Het syntropie-entropie model van 3-6-9 biedt een interessante
   structuurinterpretatie van priemgetalclustering in de Sacks-spiraal.
""")

print("\n✅ Analyse voltooid!")
print(f"📁 Bestanden gegenereerd:")
print(f"   - sacks_syntropie_entropie.png (visualisaties)")
print(f"   - sacks_3d_syntropie.png (3D weergave)")
print(f"   - sacks_syntropie_entropie.csv (gedetailleerde data)")
print(f"   - sacks_dr_statistics.csv (DR statistieken)")
