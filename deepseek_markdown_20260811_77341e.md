# The Mathematics Behind the ALVIE Spiral

## 1. Definitions

### 1.1 The Sacks Spiral
For each natural number \( n \ge 1 \), its position in the Sacks spiral is given by:

\[
x_n = \sqrt{n} \cdot \cos(n \cdot 137.5^\circ)
\]
\[
y_n = \sqrt{n} \cdot \sin(n \cdot 137.5^\circ)
\]

The angle \( 137.5^\circ \) is the **golden angle**, derived from the Golden Ratio \( \phi \):

\[
\phi = \frac{1 + \sqrt{5}}{2} \approx 1.618034
\]
\[
137.5^\circ = 360^\circ \cdot \frac{1}{\phi^2}
\]

### 1.2 Ring Index
For the square Ulam spiral, the ring index \( r(n) \) is:

\[
r(n) = \left\lceil \frac{\sqrt{n}}{2} \right\rceil
\]

Ring \( r \) contains \( 8r \) numbers, from \((2r-1)^2 + 1\) to \((2r+1)^2\).

### 1.3 Digital Root
The digital root \( \operatorname{dr}(n) \) is the repeated sum of digits:

\[
\operatorname{dr}(n) = 
\begin{cases}
9 & \text{if } n \bmod 9 = 0 \\
n \bmod 9 & \text{otherwise}
\end{cases}
\]

### 1.4 The 3-6-9 Set
\[
A = \{ n \in \mathbb{N} \mid \operatorname{dr}(n) \in \{3,6,9\} \}
\]

### 1.5 Prime Set
\[
\mathbb{P} = \{ n \in \mathbb{N} \mid n \text{ is prime} \}
\]

---

## 2. Fundamental Theorems

### Theorem 1 – 6k ± 1
For every prime number \( p > 3 \):

\[
p = 6k \pm 1 \quad (k \in \mathbb{N})
\]

**Proof:** Every integer can be written as \( 6k + r \) with \( r \in \{0,1,2,3,4,5\} \). The values \( r = 0,2,3,4 \) are always divisible by 2 or 3. Only \( r = 1 \) and \( r = 5 \) remain.

### Theorem 2 – Digital Roots of Primes
For every prime \( p > 3 \):

\[
\operatorname{dr}(p) \in \{1,2,4,5,7,8\}
\]

**Proof:** This follows directly from Theorem 1 and modular arithmetic (mod 9).

### Theorem 3 – The 1/7 Cycle
The set \( \{1,2,4,5,7,8\} \) is exactly the set of digits in the repeating decimal expansion of \( 1/7 \):

\[
\frac{1}{7} = 0.\overline{142857}
\]

### Theorem 4 – Twin Prime Centers
For every twin prime pair \( (p, p+2) \), the center is:

\[
c = p + 1 = 6k \quad (k \in \mathbb{N})
\]

And therefore:

\[
\operatorname{dr}(c) \in \{3,6,9\}
\]

---

## 3. Hypotheses (Testable)

### Hypothesis H1 – The Golden Ratio as Distance Marker
For each ring \( r \), define the **Golden Point**:

\[
P(r) = (2r-1)^2 + \frac{8r}{\phi}
\]

**Hypothesis:** The number \( \lfloor P(r) \rfloor \) or \( \lceil P(r) \rceil \) lies within a distance of 2 from a twin prime center \( 6k \).

### Hypothesis H2 – Spiral Arms
In the Sacks spiral, prime numbers with the same digital root and the same \( p \bmod 7 \)-class form **visible spiral arms** that can be approximated by a logarithmic curve.

---

## 4. Measurable Quantities

| Quantity | Definition | Meaning |
|----------|------------|---------|
| \( V_q(r) \) | \( \frac{\#\{p \in \mathbb{P} \cap \text{ring } r\}}{8r} \) | Fraction of primes in ring \( r \) |
| \( G(r) \) | \( \frac{1}{8r} \sum_{n \in \text{ring } r} \min_{a \in A} \| (x_n,y_n) - (x_a,y_a) \| \) | Average distance to the nearest 3-6-9 position |
| \( F(k) \) | Number of twin primes with center \( 6k \) in a window of size \( m \) | Frequency of twin prime centers |

---

## 5. References

- Ulam, S. (1963). The Ulam Spiral.
- Sacks, R. (1994). The Sacks Spiral.
- Riemann, B. (1859). Über die Anzahl der Primzahlen unter einer gegebenen Grösse.
- West, G. (2017). Scale.