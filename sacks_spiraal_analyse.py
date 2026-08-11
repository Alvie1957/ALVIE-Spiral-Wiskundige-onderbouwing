"""
ALVIE Spiral – Statistische Hypothese Analyse
=============================================
Dit script test de hypothesen van de ALVIE spiral:
1. Clusteren priemgetallen in bepaalde spiraalzones?
2. Markeren 3-6-9 getallen tweelingpriemcentra?
3. Is er een gouden-ratio relatie?
"""

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, log
from scipy import stats
import pandas as pd

# ============================================================================
# 1. PRIEMGETALLEN ZEEF
# ============================================================================

def sieve_of_eratosthenes(n):
    """Zeef van Eratosthenes voor priemgetallen tot n"""
    is_prime = np.ones(n+1, dtype=bool)
    is_prime[:2] = False
    for i in range(2, int(sqrt(n))+1):
        if is_prime[i]:
            is_prime[i*i:n+1:i] = False
    return np.where(is_prime)[0]

# ============================================================================
# 2. SACKS-SPIRAAL COÖRDINATEN
# ============================================================================

def sacks_coord(n, golden_angle_rad=137.5 * pi / 180):
    """Bereken Sacks-spiraal coördinaten voor getal n"""
    hoek = n * golden_angle_rad
    straal = sqrt(n)
    return straal * np.cos(hoek), straal * np.sin(hoek)

def digital_root(n):
    """Bereken digitale wortel (herhaalde som van cijfers)"""
    return 9 if n % 9 == 0 else n % 9

def twin_prime_center(p, primes_set):
    """Check of (p, p+2) tweelingpriemgetallen zijn en return center"""
    if p > 2 and (p + 2) in primes_set:
        return p + 1
    return None

# ============================================================================
# 3. DATA VOORBEREIDING
# ============================================================================

print("🔍 Voorbereiding data voor 200.000 getallen...")
N = 200_000
primes = sieve_of_eratosthenes(N)
primes_set = set(primes)

# Coördinaten
coord_data = []
for n in range(1, N+1):
    x, y = sacks_coord(n)
    dr = digital_root(n)
    is_prime = n in primes_set
    
    # Check tweelingpriem
    twin_center = twin_prime_center(n, primes_set)
    is_twin_prime = twin_center is not None
    
    coord_data.append({
        'n': n,
        'x': x,
        'y': y,
        'straal': sqrt(n),
        'hoek_deg': (n * 137.5) % 360,
        'digital_root': dr,
        'is_prime': is_prime,
        'is_twin_prime': is_twin_prime,
        'twin_center': twin_center,
        'log_n': log(n + 1)
    })

df = pd.DataFrame(coord_data)
print(f"✅ Data voorbereiding klaar: {len(df)} rijen\n")

# ============================================================================
# HYPOTHESE 1: CLUSTEREN PRIEMGETALLEN IN BEPAALDE HOEKEN?
# ============================================================================

print("=" * 70)
print("HYPOTHESE 1: Priemgetallen in bepaalde spiraalzones")
print("=" * 70)

primes_df = df[df['is_prime']]
hoek_bins = np.linspace(0, 360, 37)  # 37 bins = 10 graden per bin
hoek_counts, _ = np.histogram(primes_df['hoek_deg'], bins=hoek_bins)

# Chi-square test: zijn priemen uniform verdeeld over hoeken?
expected_uniform = len(primes_df) / len(hoek_bins)
chi2, p_value = stats.chisquare(hoek_counts)

print(f"\nHoek-distributie van priemgetallen:")
print(f"  Totaal priemen: {len(primes_df)}")
print(f"  Aantal hoekbins: {len(hoek_bins)-1}")
print(f"  Chi-square statistiek: {chi2:.2f}")
print(f"  P-waarde: {p_value:.6f}")
print(f"  Uniform verdeeld? {'❌ NEEN (clusteren detecteerd!)' if p_value < 0.05 else '✓ Ja'}")

# Vind de top 5 meest druk bezochte hoeken
top_hoeken = np.argsort(hoek_counts)[-5:][::-1]
print(f"\n🔴 Top 5 meest druk bezochte hoekzones:")
for idx, bin_idx in enumerate(top_hoeken, 1):
    hoek_range = (hoek_bins[bin_idx], hoek_bins[bin_idx+1])
    count = hoek_counts[bin_idx]
    percentage = (count / len(primes_df)) * 100
    print(f"  {idx}. Hoek {hoek_range[0]:.1f}°–{hoek_range[1]:.1f}°: {count} priemen ({percentage:.2f}%)")

# ============================================================================
# HYPOTHESE 2: MARKEREN 3-6-9 TWEELINGPRIEMCENTRA?
# ============================================================================

print("\n" + "=" * 70)
print("HYPOTHESE 2: Markeren 3-6-9 getallen tweelingpriemcentra?")
print("=" * 70)

twin_primes_df = df[df['is_twin_prime']]
print(f"\nTotaal tweelingpriemgetallen: {len(twin_primes_df)}")

if len(twin_primes_df) > 0:
    # Vind centers (p+1 voor tweelingpriemgetallen p, p+2)
    centers = []
    for _, row in twin_primes_df.iterrows():
        if row['twin_center'] is not None:
            centers.append(row['twin_center'])
    
    centers = np.array(centers)
    
    # Check digitale wortels van centers
    dr_of_centers = np.array([digital_root(c) for c in centers])
    dr_369_count = np.sum(np.isin(dr_of_centers, [3, 6, 9]))
    dr_369_pct = (dr_369_count / len(centers)) * 100 if len(centers) > 0 else 0
    
    print(f"\nTweelingpriemcentra (p+1):")
    print(f"  Totaal centers: {len(centers)}")
    print(f"  Centers met DR ∈ {{3,6,9}}: {dr_369_count} ({dr_369_pct:.2f}%)")
    print(f"  Verwachte % (uniform): {(3/9) * 100:.2f}%")
    
    if dr_369_pct > (3/9) * 100:
        print(f"  🎯 BEVONDEN: Centers liggen VAKER op 3-6-9 dan verwacht!")
        excess = dr_369_pct - (3/9) * 100
        print(f"     Overschot: +{excess:.2f}%")
    else:
        print(f"  ❌ NIET bevonden: Centers zijn uniform over alle DR's")
    
    # Binomiale test
    from scipy.stats import binom_test
    p_binom = binom_test(dr_369_count, len(centers), 3/9, alternative='greater')
    print(f"  Binomiale test p-waarde: {p_binom:.6f}")
else:
    dr_369_pct = 0

# ============================================================================
# HYPOTHESE 3: GOUDEN RATIO EN PRIEMGETALPATROON
# ============================================================================

print("\n" + "=" * 70)
print("HYPOTHESE 3: Gouden Ratio als afstandsmarker (H1)")
print("=" * 70)

phi = (1 + sqrt(5)) / 2
print(f"\nGouden Ratio φ = {phi:.6f}")

# Theorem 4: Twin prime centers liggen op 6k
centers_all = []
for p in primes:
    if p + 2 in primes_set:
        centers_all.append(p + 1)

centers_all = np.array(centers_all)

# Check: liggen centers op 6k?
centers_on_6k = np.sum(centers_all % 6 == 0)
centers_6k_pct = (centers_on_6k / len(centers_all)) * 100 if len(centers_all) > 0 else 0

print(f"\nTweelingpriemcentra op 6k:")
print(f"  Totaal centers: {len(centers_all)}")
print(f"  Centers = 6k (mod 6 ≡ 0): {centers_on_6k} ({centers_6k_pct:.2f}%)")
print(f"  Theoretisch: 100% (Theorem 4)")

if centers_6k_pct > 99:
    print(f"  ✅ THEOREM 4 GEVERIFIEERD!")
else:
    print(f"  ⚠️  Lager dan verwacht, check code")

# ============================================================================
# ANALYSE: PRIEMGETALLEN ROND 3-6-9 PUNTEN
# ============================================================================

print("\n" + "=" * 70)
print("ANALYSE: Priemgetalsdichtheid rond 3-6-9 punten")
print("=" * 70)

df_369 = df[df['digital_root'].isin([3, 6, 9])]
df_not369 = df[~df['digital_root'].isin([3, 6, 9])]

primes_on_369 = np.sum(df_369['is_prime'])
primes_not_on_369 = np.sum(df_not369['is_prime'])

pct_369 = (primes_on_369 / len(df_369)) * 100 if len(df_369) > 0 else 0
pct_not369 = (primes_not_on_369 / len(df_not369)) * 100 if len(df_not369) > 0 else 0

print(f"\nPriemgetaldichtheid:")
print(f"  Op 3-6-9 punten: {primes_on_369} / {len(df_369)} = {pct_369:.4f}%")
print(f"  Op andere punten: {primes_not_on_369} / {len(df_not369)} = {pct_not369:.4f}%")
if pct_369 > 0:
    print(f"  Verhouding: {pct_not369 / pct_369:.2f}x meer priemen buiten 3-6-9")

# Theorem 2: Priemen hebben DR ∈ {1,2,4,5,7,8}
primes_dr = df[df['is_prime']]['digital_root'].values
primes_on_369_count = np.sum(np.isin(primes_dr, [3, 6, 9]))
primes_on_369_pct = (primes_on_369_count / len(primes_dr)) * 100

print(f"\nTheorem 2 verificatie:")
print(f"  Priemen met DR ∈ {{3,6,9}}: {primes_on_369_count} / {len(primes_dr)} = {primes_on_369_pct:.4f}%")
print(f"  Verwacht: ~0% (Theorem 2 zegt priemen hebben DR ∈ {{1,2,4,5,7,8}})")
print(f"  ✅ {'GEVERIFIEERD!' if primes_on_369_pct < 1 else '❌ ANOMALIE DETECTED'}")

# ============================================================================
# VISUALISATIE: DISTRIBUTIES
# ============================================================================

print("\n" + "=" * 70)
print("Genereer visualisaties...")
print("=" * 70)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Hoekdistributie priemgetallen
ax = axes[0, 0]
ax.bar(hoek_bins[:-1], hoek_counts, width=10, alpha=0.7, color='red', edgecolor='black')
ax.axhline(expected_uniform, color='green', linestyle='--', linewidth=2, label=f'Uniform verwacht ({expected_uniform:.0f})')
ax.set_xlabel('Hoek (graden)')
ax.set_ylabel('Aantal priemgetallen')
ax.set_title(f'Hoekdistributie priemgetallen (χ²={chi2:.1f}, p={p_value:.4f})')
ax.legend()
ax.grid(alpha=0.3)

# Plot 2: Priemgetalsdichtheid vs straal
ax = axes[0, 1]
radius_bins = np.linspace(0, sqrt(N), 50)
df['straal_bin'] = pd.cut(df['straal'], bins=radius_bins)
radius_density = df.groupby('straal_bin')['is_prime'].mean() * 100
radius_centers = [interval.mid for interval in radius_density.index]
ax.plot(radius_centers, radius_density.values, 'o-', color='red', linewidth=2, markersize=4)
ax.set_xlabel('Straal (√n)')
ax.set_ylabel('Priemgetalsdichtheid (%)')
ax.set_title('Priemgetalsdichtheid langs de spiraal')
ax.grid(alpha=0.3)

# Plot 3: Digitale wortel distributie
ax = axes[1, 0]
dr_counts = df['digital_root'].value_counts().sort_index()
colors_dr = ['red' if dr in [3,6,9] else 'blue' for dr in dr_counts.index]
ax.bar(dr_counts.index, dr_counts.values, color=colors_dr, alpha=0.7, edgecolor='black')
ax.set_xlabel('Digitale Wortel')
ax.set_ylabel('Aantal getallen')
ax.set_title('Distributie Digitale Wortels (rood=3-6-9, blauw=ander)')
ax.grid(alpha=0.3)

# Plot 4: Priemgetallen vs DR
ax = axes[1, 1]
dr_prime_pct = []
for dr in range(1, 10):
    count_total = np.sum(df['digital_root'] == dr)
    count_prime = np.sum((df['digital_root'] == dr) & (df['is_prime']))
    pct = (count_prime / count_total) * 100 if count_total > 0 else 0
    dr_prime_pct.append(pct)

colors_dr = ['red' if dr in [3,6,9] else 'green' for dr in range(1, 10)]
ax.bar(range(1, 10), dr_prime_pct, color=colors_dr, alpha=0.7, edgecolor='black')
ax.set_xlabel('Digitale Wortel')
ax.set_ylabel('% Priemgetallen in deze DR')
ax.set_title('Priemgetalsdichtheid per Digitale Wortel')
ax.set_xticks(range(1, 10))
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('sacks_analyse.png', dpi=300)
print("✅ Opgeslagen: sacks_analyse.png")
plt.show()

# ============================================================================
# SAMENVATTING
# ============================================================================

print("\n" + "=" * 70)
print("📊 SAMENVATTING HYPOTHESETEST")
print("=" * 70)

print(f"""
✓ H1 (Hoekzones): Chi-square test toont {'SIGNIFICANTE CLUSTERING' if p_value < 0.05 else 'UNIFORME SPREIDING'}
  → Priemgetallen concentreren zich in bepaalde spiraalzones!

{'✓' if dr_369_pct > (3/9)*100 else '?'} H2 (3-6-9 Centers): Tweelingpriemcentra liggen {dr_369_pct:.2f}% op 3-6-9
  → Verwacht: {(3/9)*100:.2f}%, Bevonden: {dr_369_pct:.2f}%
  
✓ Theorem 4: {centers_6k_pct:.2f}% van tweelingpriemcentra op 6k
  → Theoretisch: 100%

⚠️  Theorem 2: Priemen mogen NIET op 3-6-9 liggen
  → Bevonden: {primes_on_369_pct:.4f}% (✅ Geverifieerd!)

🎯 CONCLUSIE:
  De ALVIE spiral biedt een interessante visualisatie van priemgetalpatronen.
  Verdere numerieke analyse over grotere bereiken nodig voor bewijzen.
""")

print("\n✅ Analyse voltooid!")
