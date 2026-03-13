import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Payment Acceptance Rate Analyser",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-container { background: #f8f9fa; border-radius: 8px; padding: 1rem; text-align: center; }
    .metric-label { font-size: 12px; color: #6c757d; margin-bottom: 4px; }
    .metric-value { font-size: 28px; font-weight: 600; }
    .metric-sub { font-size: 11px; color: #adb5bd; margin-top: 2px; }
    .insight-box { background: #e8f4f8; border-left: 4px solid #1565C0; padding: 0.75rem 1rem;
                   border-radius: 0 8px 8px 0; margin: 0.5rem 0; font-size: 14px; }
    .warning-box { background: #fff3e0; border-left: 4px solid #E65100; padding: 0.75rem 1rem;
                   border-radius: 0 8px 8px 0; margin: 0.5rem 0; font-size: 14px; }
    .success-box { background: #e8f5e9; border-left: 4px solid #2E7D32; padding: 0.75rem 1rem;
                   border-radius: 0 8px 8px 0; margin: 0.5rem 0; font-size: 14px; }
    h1 { font-size: 1.6rem !important; }
    h2 { font-size: 1.2rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Data generation (cached) ──────────────────────────────────────────────────
@st.cache_data
def generate_data(n=250_000, seed=42):
    np.random.seed(seed)

    payment_methods = ['Credit Card', 'Debit Card', 'iDEAL', 'PayPal', 'Klarna', 'Prepaid Card']
    pm_weights      = [0.35, 0.25, 0.15, 0.12, 0.08, 0.05]

    countries        = ['Netherlands', 'Germany', 'France', 'United Kingdom', 'Belgium',
                        'Spain', 'Italy', 'Sweden', 'Poland', 'Austria']
    country_weights  = [0.18, 0.20, 0.14, 0.16, 0.07, 0.08, 0.07, 0.04, 0.04, 0.02]

    decline_reasons  = ['Insufficient funds', 'Do not honour', 'Stolen card',
                        'Expired card', 'Invalid card number', 'Suspected fraud',
                        'Exceeds withdrawal limit', 'Card not supported']

    df = pd.DataFrame()
    df['payment_method'] = np.random.choice(payment_methods, n, p=pm_weights)
    df['country']        = np.random.choice(countries, n, p=country_weights)
    hour_probs = np.array([0.02,0.015,0.01,0.01,0.01,0.015,0.03,0.05,0.06,0.06,
                           0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.055,0.05,
                           0.045,0.04,0.035,0.025])
    hour_probs = hour_probs / hour_probs.sum()
    df['hour']           = np.random.choice(range(24), n, p=hour_probs)
    df['day_of_week']    = np.random.choice(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], n,
                               p=[0.16,0.16,0.16,0.16,0.16,0.10,0.10])
    df['amount']         = np.where(
        df['payment_method'].isin(['iDEAL','PayPal']),
        np.random.lognormal(4.0, 1.0, n).clip(1, 2000),
        np.random.lognormal(4.2, 1.1, n).clip(1, 5000)
    ).round(2)

    df['amount_bucket'] = pd.cut(df['amount'],
        bins=[0, 25, 50, 100, 250, 500, 1000, 99999],
        labels=['€0-25','€25-50','€50-100','€100-250','€250-500','€500-1k','€1k+'])

    base_accept = {'iDEAL':0.980,'PayPal':0.952,'Debit Card':0.921,
                   'Credit Card':0.887,'Klarna':0.863,'Prepaid Card':0.812}
    country_mod = {'Netherlands':+0.020,'Sweden':+0.015,'Germany':+0.010,'Austria':+0.005,
                   'Belgium':0.000,'United Kingdom':-0.005,'France':-0.010,
                   'Spain':-0.020,'Italy':-0.025,'Poland':-0.030}

    def amount_mod(a):
        if a < 25:   return +0.010
        if a < 100:  return +0.005
        if a < 250:  return  0.000
        if a < 500:  return -0.015
        if a < 1000: return -0.035
        return -0.065

    def hour_mod(h):
        if 1 <= h <= 5:  return -0.030
        if 6 <= h <= 8:  return -0.010
        if 9 <= h <= 18: return +0.005
        return 0.000

    accept_prob = (
        df['payment_method'].map(base_accept)
        + df['country'].map(country_mod)
        + df['amount'].apply(amount_mod)
        + df['hour'].apply(hour_mod)
    ).clip(0.05, 0.999)

    df['authorized'] = (np.random.rand(n) < accept_prob).astype(int)

    decline_reason_weights = [0.30,0.20,0.08,0.12,0.08,0.10,0.08,0.04]
    df['decline_reason'] = np.where(
        df['authorized'] == 0,
        np.random.choice(decline_reasons, n, p=decline_reason_weights),
        'N/A'
    )
    return df


@st.cache_data
def run_retry_simulation(df):
    np.random.seed(99)
    hard_codes = ['Stolen card','Suspected fraud','Invalid card number','Expired card','Card not supported']
    recoverable_codes = ['Insufficient funds','Do not honour','Exceeds withdrawal limit']
    alt_method = {'Credit Card':'PayPal','Debit Card':'PayPal','Prepaid Card':'PayPal',
                  'Klarna':'PayPal','PayPal':'Credit Card','iDEAL':'PayPal'}
    business_hours = list(range(9, 19))

    declined = df[df['authorized'] == 0].copy()

    # Naive
    def naive_success(row):
        return np.random.rand() < (0.02 if row['decline_reason'] in hard_codes else 0.15)
    declined['naive_success'] = declined.apply(naive_success, axis=1)

    # Smart
    def smart_eligible(row):
        return row['decline_reason'] not in hard_codes and row['hour'] in business_hours

    def smart_method(row):
        if row['amount'] > 250 and row['payment_method'] in ['Credit Card','Debit Card','Prepaid Card']:
            return alt_method.get(row['payment_method'], row['payment_method'])
        return row['payment_method']

    def smart_success(row):
        if not row['smart_eligible']:
            return False
        base = 0.38 if row['decline_reason'] in recoverable_codes else 0.18
        if row['smart_method'] != row['payment_method']:
            base += 0.12
        if row['hour'] in business_hours:
            base += 0.05
        return np.random.rand() < min(base, 0.90)

    declined['smart_eligible'] = declined.apply(smart_eligible, axis=1)
    declined['smart_method']   = declined.apply(smart_method, axis=1)
    declined['smart_success']  = declined.apply(smart_success, axis=1)

    return declined


# ── Load data ────────────────────────────────────────────────────────────────
df = generate_data()
declined_df = run_retry_simulation(df)

overall_auth_rate = df['authorized'].mean() * 100

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💳 Filters")
    st.markdown("---")

    selected_countries = st.multiselect(
        "Countries",
        options=sorted(df['country'].unique()),
        default=sorted(df['country'].unique())
    )
    selected_methods = st.multiselect(
        "Payment methods",
        options=sorted(df['payment_method'].unique()),
        default=sorted(df['payment_method'].unique())
    )
    hour_range = st.slider("Hour of day", 0, 23, (0, 23))

    st.markdown("---")
    st.markdown("### 📖 About")
    st.markdown("""
    This dashboard analyses payment authorization rates across 250,000 synthetic European transactions.

    Built to demonstrate payments analytics skills relevant to roles at companies like Adyen.

    **[View on GitHub](https://github.com/your-username/payment-acceptance-rate)**
    """)

# ── Apply filters ────────────────────────────────────────────────────────────
mask = (
    df['country'].isin(selected_countries) &
    df['payment_method'].isin(selected_methods) &
    df['hour'].between(hour_range[0], hour_range[1])
)
fdf = df[mask]

if len(fdf) == 0:
    st.warning("No data matches your current filters. Please adjust the sidebar selections.")
    st.stop()

filtered_auth_rate = fdf['authorized'].mean() * 100
filtered_declined  = (fdf['authorized'] == 0).sum()

# ── Navigation ───────────────────────────────────────────────────────────────
pages = ["Overview", "By Country", "Decline Analysis", "Time Patterns", "Retry Simulation"]
page  = st.sidebar.radio("Navigate", pages, index=0)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.title("💳 Payment Acceptance Rate Analyser")
    st.caption("250,000 synthetic European transactions · Nick Zwart · ABN AMRO Fraud Data Analyst")
    st.markdown("---")

    # KPI row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Transactions", f"{len(fdf):,}")
    with col2:
        delta = filtered_auth_rate - overall_auth_rate
        st.metric("Authorization Rate", f"{filtered_auth_rate:.2f}%",
                  delta=f"{delta:+.2f}pp vs overall" if abs(delta) > 0.01 else None)
    with col3:
        st.metric("Declined", f"{filtered_declined:,}",
                  delta=f"{filtered_declined/len(fdf)*100:.1f}% decline rate",
                  delta_color="inverse")
    with col4:
        avg_amt = fdf['amount'].mean()
        st.metric("Avg Transaction", f"€{avg_amt:.2f}")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Authorization rate by payment method")
        pm_stats = fdf.groupby('payment_method').agg(
            transactions=('authorized','count'),
            auth_rate=('authorized','mean')
        ).assign(auth_rate=lambda x: x['auth_rate']*100).sort_values('auth_rate', ascending=True)

        fig, ax = plt.subplots(figsize=(7, 4))
        colors = ['#2E7D32' if r >= 95 else '#1565C0' if r >= 88 else '#C62828'
                  for r in pm_stats['auth_rate']]
        bars = ax.barh(pm_stats.index, pm_stats['auth_rate'], color=colors, edgecolor='white')
        ax.set_xlim(75, 102)
        ax.axvline(filtered_auth_rate, color='gray', linestyle='--', alpha=0.5,
                   label=f'Overall ({filtered_auth_rate:.1f}%)')
        ax.legend(fontsize=9)
        ax.set_xlabel('Authorization Rate (%)')
        for bar, val in zip(bars, pm_stats['auth_rate']):
            ax.text(val + 0.2, bar.get_y() + bar.get_height()/2,
                    f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

        best_pm = pm_stats['auth_rate'].idxmax()
        worst_pm = pm_stats['auth_rate'].idxmin()
        gap = pm_stats['auth_rate'].max() - pm_stats['auth_rate'].min()
        st.markdown(f'<div class="insight-box">💡 <b>{best_pm}</b> leads at {pm_stats["auth_rate"].max():.1f}% vs <b>{worst_pm}</b> at {pm_stats["auth_rate"].min():.1f}% — a {gap:.1f}pp gap. For Dutch merchants, routing to iDEAL first is the single highest-impact checkout change available.</div>', unsafe_allow_html=True)

    with col_right:
        st.subheader("Transaction volume by payment method")
        pm_vol = fdf.groupby('payment_method').size().sort_values(ascending=True)

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.barh(pm_vol.index, pm_vol.values, color='#B5D4F4', edgecolor='white')
        ax.set_xlabel('Transactions')
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))
        for i, v in enumerate(pm_vol.values):
            ax.text(v + 100, i, f'{v:,}', va='center', fontsize=9)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

        top_vol = pm_vol.idxmax()
        st.markdown(f'<div class="insight-box">💡 <b>{top_vol}</b> accounts for the largest share of volume. High-volume methods with lower auth rates represent the biggest absolute opportunity for improvement.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: BY COUNTRY
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "By Country":
    st.title("🌍 Authorization Rate by Country")
    st.markdown("---")

    country_stats = fdf.groupby('country').agg(
        transactions=('authorized','count'),
        auth_rate=('authorized','mean')
    ).assign(auth_rate=lambda x: x['auth_rate']*100).sort_values('auth_rate', ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Authorization rate by country")
        fig, ax = plt.subplots(figsize=(7, 5))
        colors = ['#2E7D32' if r >= 92 else '#1565C0' if r >= 88 else '#C62828'
                  for r in country_stats['auth_rate']]
        bars = ax.barh(country_stats.index[::-1], country_stats['auth_rate'][::-1],
                       color=colors[::-1], edgecolor='white')
        ax.set_xlim(80, 102)
        ax.axvline(filtered_auth_rate, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlabel('Authorization Rate (%)')
        for bar, val in zip(bars, country_stats['auth_rate'][::-1]):
            ax.text(val + 0.2, bar.get_y() + bar.get_height()/2,
                    f'{val:.1f}%', va='center', fontsize=9, fontweight='bold')
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("Heatmap: country x payment method")
        heatmap_data = fdf.groupby(['country','payment_method'])['authorized'].mean().unstack() * 100
        heatmap_data = heatmap_data.reindex(country_stats.index)
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.heatmap(heatmap_data, ax=ax, annot=True, fmt='.1f', cmap='RdYlGn',
                    vmin=75, vmax=100, linewidths=0.5,
                    cbar_kws={'label':'Auth Rate (%)', 'shrink':0.8})
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.tick_params(axis='x', rotation=30, labelsize=9)
        ax.tick_params(axis='y', labelsize=9)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    best_c  = country_stats.index[0]
    worst_c = country_stats.index[-1]
    gap_c   = country_stats['auth_rate'].iloc[0] - country_stats['auth_rate'].iloc[-1]
    st.markdown(f'<div class="insight-box">💡 <b>{best_c}</b> leads at {country_stats["auth_rate"].iloc[0]:.1f}% while <b>{worst_c}</b> lags at {country_stats["auth_rate"].iloc[-1]:.1f}% — a {gap_c:.1f}pp gap. Market-specific issuer routing or local payment method promotion (e.g. BLIK for Poland) could close this gap.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Country summary table")
    display_df = country_stats.copy()
    display_df['auth_rate'] = display_df['auth_rate'].round(2).astype(str) + '%'
    display_df.columns = ['Transactions', 'Authorization Rate']
    st.dataframe(display_df, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DECLINE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Decline Analysis":
    st.title("📉 Decline Reason Analysis")
    st.markdown("---")

    declined = fdf[fdf['authorized'] == 0]
    hard_codes = ['Stolen card','Suspected fraud','Invalid card number','Expired card','Card not supported']

    if len(declined) == 0:
        st.info("No declined transactions in current filter selection.")
    else:
        decline_counts = declined['decline_reason'].value_counts()
        decline_pct    = decline_counts / len(declined) * 100

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Decline reason distribution")
            fig, ax = plt.subplots(figsize=(7, 4))
            colors = ['#C62828' if r in hard_codes else '#F57C00'
                      for r in decline_counts.index]
            bars = ax.barh(decline_counts.index, decline_pct, color=colors, edgecolor='white')
            ax.set_xlabel('Share of Declines (%)')
            for bar, val in zip(bars, decline_pct):
                ax.text(val + 0.2, bar.get_y() + bar.get_height()/2,
                        f'{val:.1f}%', va='center', fontsize=9)
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='#C62828', label='Hard decline (do not retry)'),
                Patch(facecolor='#F57C00', label='Soft decline (potentially recoverable)')
            ]
            ax.legend(handles=legend_elements, fontsize=8, loc='lower right')
            fig.tight_layout()
            st.pyplot(fig)
            plt.close()

        with col2:
            st.subheader("Decline reasons by payment method")
            dr_pm = declined.groupby(['payment_method','decline_reason']).size().unstack(fill_value=0)
            dr_pm_pct = dr_pm.div(dr_pm.sum(axis=1), axis=0) * 100
            fig, ax = plt.subplots(figsize=(7, 4))
            dr_pm_pct.plot(kind='bar', ax=ax, stacked=True, colormap='Set2',
                           edgecolor='white', linewidth=0.5)
            ax.set_xlabel('')
            ax.set_ylabel('Share of Declines (%)')
            ax.tick_params(axis='x', rotation=30)
            ax.legend(fontsize=7, bbox_to_anchor=(1.01, 1), loc='upper left')
            fig.tight_layout()
            st.pyplot(fig)
            plt.close()

        fixable = ['Expired card','Invalid card number','Card not supported']
        fixable_pct = decline_pct[decline_pct.index.isin(fixable)].sum()
        soft_pct = decline_pct[~decline_pct.index.isin(hard_codes)].sum()

        st.markdown(f'<div class="success-box">✅ <b>{fixable_pct:.1f}%</b> of declines are directly fixable (expired/invalid card). Prompting customers to update their details or offering an alternative method at the point of decline can recover these.</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="warning-box">⚠️ <b>{soft_pct:.1f}%</b> are soft declines worth retrying with smart logic. Hard declines (stolen card, fraud) should never be retried — doing so risks issuer friction that degrades your overall acceptance rate.</div>', unsafe_allow_html=True)

        st.markdown("---")
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Amount bucket analysis")
            amount_stats = fdf.groupby('amount_bucket', observed=True)['authorized'].mean() * 100
            fig, ax = plt.subplots(figsize=(7, 3.5))
            colors = ['#2E7D32' if r >= 93 else '#1565C0' if r >= 88 else '#C62828'
                      for r in amount_stats]
            ax.bar(amount_stats.index.astype(str), amount_stats.values,
                   color=colors, edgecolor='white')
            ax.set_ylim(75, 102)
            ax.axhline(filtered_auth_rate, color='gray', linestyle='--', alpha=0.5)
            ax.set_ylabel('Authorization Rate (%)')
            for i, v in enumerate(amount_stats.values):
                ax.text(i, v + 0.3, f'{v:.1f}%', ha='center', fontsize=9, fontweight='bold')
            fig.tight_layout()
            st.pyplot(fig)
            plt.close()

        with col4:
            st.subheader("Auth rate by amount and method")
            am_pm = fdf.groupby(['amount_bucket','payment_method'], observed=True)['authorized'].mean().unstack() * 100
            fig, ax = plt.subplots(figsize=(7, 3.5))
            am_pm.plot(ax=ax, marker='o', markersize=4, linewidth=2)
            ax.set_ylabel('Authorization Rate (%)')
            ax.set_xlabel('')
            ax.tick_params(axis='x', rotation=20)
            ax.legend(fontsize=8, bbox_to_anchor=(1.01,1), loc='upper left')
            fig.tight_layout()
            st.pyplot(fig)
            plt.close()

        drop = amount_stats.iloc[0] - amount_stats.iloc[-1]
        st.markdown(f'<div class="insight-box">💡 Authorization rate drops <b>{drop:.1f}pp</b> from the lowest to highest amount bucket. iDEAL and PayPal maintain stronger rates at higher amounts — worth promoting for high-value transactions where card declines are most likely.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: TIME PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Time Patterns":
    st.title("🕐 Time-of-Day & Day-of-Week Patterns")
    st.markdown("---")

    hourly = fdf.groupby('hour')['authorized'].mean() * 100
    dow_order = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    daily = fdf.groupby('day_of_week')['authorized'].mean().reindex(dow_order) * 100

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Authorization rate by hour")
        fig, ax = plt.subplots(figsize=(7, 4))
        hour_colors = ['#C62828' if 1 <= h <= 5 else '#1565C0' for h in range(24)]
        ax.bar(range(24), hourly.reindex(range(24)).fillna(filtered_auth_rate),
               color=hour_colors, edgecolor='white')
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Authorization Rate (%)')
        ax.set_xticks(range(0, 24, 2))
        ax.set_xticklabels([f'{h}:00' for h in range(0, 24, 2)], rotation=45, fontsize=8)
        ax.axhline(filtered_auth_rate, color='gray', linestyle='--', alpha=0.5)
        ax.fill_betweenx([hourly.min() - 1, hourly.max() + 1], 1, 5,
                          alpha=0.08, color='red', label='High-risk window')
        ax.set_ylim(hourly.min() - 2, hourly.max() + 2)
        ax.legend(fontsize=9)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("Authorization rate by day of week")
        fig, ax = plt.subplots(figsize=(7, 4))
        dow_colors = ['#C62828' if d in ['Sat','Sun'] else '#1565C0' for d in dow_order]
        ax.bar(daily.index, daily.values, color=dow_colors, edgecolor='white')
        ax.set_ylabel('Authorization Rate (%)')
        ax.axhline(filtered_auth_rate, color='gray', linestyle='--', alpha=0.5)
        ax.set_ylim(daily.min() - 2, daily.max() + 2)
        for i, (day, val) in enumerate(daily.items()):
            ax.text(i, val + 0.1, f'{val:.1f}%', ha='center', fontsize=9)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    overnight = hourly[hourly.index.isin(range(1, 6))].mean()
    peak      = hourly[hourly.index.isin(range(9, 19))].mean()
    gap_t     = peak - overnight

    st.markdown(f'<div class="warning-box">⚠️ Overnight auth rate (01:00-05:00): <b>{overnight:.1f}%</b> vs peak hours (09:00-18:00): <b>{peak:.1f}%</b> — a <b>{gap_t:.1f}pp gap</b>. Retry logic should deprioritise overnight attempts, especially for high-value card transactions and subscription billing.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Hourly heatmap: auth rate by method and hour")
    pivot = fdf.groupby(['payment_method','hour'])['authorized'].mean().unstack() * 100
    fig, ax = plt.subplots(figsize=(14, 4))
    sns.heatmap(pivot, ax=ax, cmap='RdYlGn', vmin=80, vmax=100,
                linewidths=0.3, annot=False,
                cbar_kws={'label':'Auth Rate (%)', 'shrink':0.8})
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('')
    ax.tick_params(axis='x', labelsize=8)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown('<div class="insight-box">💡 The heatmap shows that iDEAL remains consistently high across all hours, while card-based methods show clear overnight deterioration. This pattern is driven by issuer fraud scoring being more conservative during off-hours.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: RETRY SIMULATION
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Retry Simulation":
    st.title("🔁 Retry Simulation: Naive vs Smart Strategy")
    st.markdown("""
    A declined transaction is not necessarily lost revenue. Most merchants retry declines naively —
    immediately, same method, regardless of decline code. This page simulates what intelligent retry
    logic recovers compared to that baseline.
    """)
    st.markdown("---")

    # Summary metrics
    naive_recovered = declined_df['naive_success'].sum()
    naive_revenue   = declined_df.loc[declined_df['naive_success'], 'amount'].sum()
    naive_attempts  = len(declined_df)
    naive_eff       = naive_recovered / naive_attempts * 100

    smart_attempts  = declined_df['smart_eligible'].sum()
    smart_recovered = declined_df['smart_success'].sum()
    smart_revenue   = declined_df.loc[declined_df['smart_success'], 'amount'].sum()
    smart_eff       = smart_recovered / max(smart_attempts, 1) * 100

    extra_txns    = smart_recovered - naive_recovered
    extra_revenue = smart_revenue - naive_revenue

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Naive: recovered", f"{naive_recovered:,}", f"from {naive_attempts:,} attempts")
    with col2:
        st.metric("Smart: recovered", f"{smart_recovered:,}", f"from {smart_attempts:,} attempts")
    with col3:
        st.metric("Extra transactions", f"+{extra_txns:,}", "smart vs naive")
    with col4:
        st.metric("Extra revenue", f"+€{extra_revenue:,.0f}", "smart vs naive")

    st.markdown("---")

    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Head-to-head comparison")
        fig, axes = plt.subplots(1, 3, figsize=(9, 3.5))
        strategies = ['Naive', 'Smart']
        colors     = ['#B5D4F4', '#2E7D32']

        axes[0].bar(strategies, [naive_recovered, smart_recovered], color=colors, edgecolor='white')
        axes[0].set_title('Recovered\ntransactions', fontsize=10, fontweight='bold')
        for i, v in enumerate([naive_recovered, smart_recovered]):
            axes[0].text(i, v + 5, f'{v:,}', ha='center', fontsize=9, fontweight='bold')

        axes[1].bar(strategies, [naive_revenue, smart_revenue], color=colors, edgecolor='white')
        axes[1].set_title('Recovered\nrevenue', fontsize=10, fontweight='bold')
        axes[1].yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'€{x/1000:.0f}k'))
        for i, v in enumerate([naive_revenue, smart_revenue]):
            axes[1].text(i, v + 200, f'€{v/1000:.0f}k', ha='center', fontsize=9, fontweight='bold')

        axes[2].bar(strategies, [naive_eff, smart_eff], color=colors, edgecolor='white')
        axes[2].set_title('Retry\nefficiency', fontsize=10, fontweight='bold')
        for i, v in enumerate([naive_eff, smart_eff]):
            axes[2].text(i, v + 0.3, f'{v:.1f}%', ha='center', fontsize=9, fontweight='bold')

        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_r:
        st.subheader("Recovery by decline reason")
        breakdown = declined_df.groupby('decline_reason').agg(
            naive=('naive_success','sum'),
            smart=('smart_success','sum')
        ).sort_values('smart', ascending=True)

        fig, ax = plt.subplots(figsize=(7, 3.5))
        x = np.arange(len(breakdown))
        w = 0.35
        ax.barh(x - w/2, breakdown['naive'], w, label='Naive', color='#B5D4F4', edgecolor='white')
        ax.barh(x + w/2, breakdown['smart'], w, label='Smart', color='#2E7D32', edgecolor='white', alpha=0.85)
        ax.set_yticks(x)
        ax.set_yticklabels(breakdown.index, fontsize=9)
        ax.set_xlabel('Recovered transactions')
        ax.legend(fontsize=9)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.subheader("How smart retry works")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("**Rule 1: Skip hard declines**")
        st.markdown("""
        Hard decline codes (stolen card, suspected fraud, invalid number, expired card)
        are never retried. Retrying these wastes attempts and risks lowering your overall
        acceptance rate by signalling desperation to issuers.
        """)
    with col_b:
        st.markdown("**Rule 2: Retry during business hours**")
        st.markdown("""
        Retries are scheduled during 09:00-18:00 when issuer authorization rates are
        highest. Overnight retries face a measurably higher decline rate, particularly
        for soft decline codes like insufficient funds.
        """)
    with col_c:
        st.markdown("**Rule 3: Alternative method routing**")
        st.markdown("""
        For high-value card failures (>€250), the customer is offered PayPal as an
        alternative rather than retrying the same card. This recovers transactions that
        would be lost to repeated same-method failures.
        """)

    wasted = naive_attempts - smart_attempts
    st.markdown(f'<div class="success-box">✅ Smart retry skips <b>{wasted:,}</b> wasted attempts on hard declines, recovering <b>+{extra_txns:,} transactions</b> worth <b>+€{extra_revenue:,.0f}</b> more than naive retry — at <b>{smart_eff - naive_eff:.1f}pp higher efficiency</b>.</div>', unsafe_allow_html=True)
