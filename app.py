from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="DengueVisor | Perú", page_icon="◉", layout="wide")
with st.sidebar:
    st.markdown("### ◉ DengueVisor")
    st.caption("PERÚ · EXPLORADOR HISTÓRICO")
    dark = st.toggle("Modo oscuro", value=False, key="dark_mode")
bg, surface, ink, muted, border = ("#0e1625", "#18243a", "#edf3fc", "#a8b9cf", "#2d405a") if dark else ("#f3f6fb", "#ffffff", "#172b4d", "#63758c", "#e2e9f2")
st.markdown(f"""<style>
.stApp {{background:{bg};color:{ink};--text-color:{ink};--background-color:{bg};--secondary-background-color:{surface};--primary-color:#167c80}}
[data-testid="stHeader"] {{background:{bg}}}
[data-testid="stSidebar"] {{background:{surface};border-right:1px solid {border}}}
.block-container {{max-width:1480px;padding-top:2.3rem}}
h1,h2,h3,p,label,[data-testid="stWidgetLabel"], [data-testid="stMetricValue"] {{color:{ink}!important}}
[data-testid="stCaptionContainer"] p {{color:{muted}!important}}
[data-testid="stMetric"] {{background:{surface};border:1px solid {border};border-radius:18px;padding:22px;box-shadow:0 4px 18px #10243b06;border-top:3px solid #25a69a}}
[data-testid="stMetricLabel"] p {{color:{muted}!important;font-size:.88rem}}
[data-testid="stMetricValue"] {{font-weight:750;letter-spacing:-.04em}}
div[data-baseweb="input"],div[data-baseweb="select"]>div {{background:{bg}!important;color:{ink}!important;border-color:{border}!important;border-radius:10px}}
[data-testid="stTextInput"] input,[data-testid="stMultiSelect"] [data-baseweb="select"]>div {{background:{bg}!important;color:{ink}!important}}
[data-testid="stTextInput"]>div {{border-radius:12px;border-color:{border}}}
[data-baseweb="popover"] [role="listbox"],[data-baseweb="popover"] [role="option"] {{background:{surface}!important;color:{ink}!important}}
[data-testid="stDownloadButton"] button {{background:#167c80!important;color:#fff!important;border-radius:24px;border:0;padding:10px 22px}}
[data-testid="stDownloadButton"] button p {{color:#fff!important}}
input {{color:{ink}!important}}
span[data-baseweb="tag"] {{background:#d7f2ee!important;color:#125e60!important;border-radius:6px}}
span[data-baseweb="tag"] span {{color:#125e60!important}}
[data-baseweb="tab-list"] {{background:{surface};padding:6px;border-radius:13px;gap:8px;border:1px solid {border};margin:20px 0}}
button[data-baseweb="tab"] {{color:{muted};border-radius:9px;padding:8px 20px}}
button[data-baseweb="tab"][aria-selected="true"] {{background:#e0f3f0;color:#116b65;font-weight:700}}
[data-baseweb="tab-highlight"] {{background:transparent}}
[data-testid="stPlotlyChart"] {{border:1px solid {border};border-radius:16px;overflow:hidden}}
.eyebrow {{color:#16867f;font-size:.75rem;font-weight:800;letter-spacing:.15em;margin-bottom:12px}}
.hero-title {{font-size:2.7rem;font-weight:800;letter-spacing:-.045em;line-height:1.15;color:{ink}}}
.hero-sub {{color:{muted};font-size:1rem;margin:12px 0 26px}}
.hero-banner {{background:linear-gradient(115deg,#083e42,#087f80 70%,#19a496);border-radius:0 0 26px 26px;padding:32px 36px;margin-bottom:34px;box-shadow:0 16px 32px #063c401c}}
.hero-banner .eyebrow {{color:#b9f5e9;font-size:.78rem}}
.hero-banner .hero-title {{color:white;font-size:3.25rem;margin:22px 0}}
.hero-banner .hero-sub {{color:#e3faf6;max-width:850px}}
.source-pill {{display:inline-block;border:1px solid #a9dfd780;border-radius:24px;color:white;padding:8px 14px;margin:0 8px 4px 0;font-size:.8rem}}
[data-testid="stSidebar"] {{background:{'#14262b' if dark else '#edf6f4'}}}
[data-testid="stMetric"] {{min-height:166px;box-shadow:0 8px 24px #163f4108}}
@media(max-width:700px) {{.hero-banner {{padding:24px 20px}} .hero-banner .hero-title {{font-size:2.4rem}}}}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero-banner"><div class="eyebrow">OBSERVATORIO DE NOTIFICACIONES · PERÚ</div><div class="hero-title">DengueVisor</div><div class="hero-sub">Explora notificaciones, tendencias y cobertura con el contexto de cada dato.</div><span class="source-pill">Fuente oficial: MINSA / CDC Perú</span><span class="source-pill">Snapshot histórico · 2020–2025</span></div>', unsafe_allow_html=True)
path = Path(__file__).parent / "data/processed/weekly.csv"
if not path.exists():
    st.error("Ejecuta python pipeline.py para generar los datos")
    st.stop()
df = pd.read_csv(path)
metadata = json.loads(path.with_name("metadata.json").read_text(encoding="utf-8"))
with st.sidebar:
    st.divider()
    st.subheader("Explorar datos")
    search = st.text_input("Buscar departamento")
    options = [d for d in sorted(df.department.unique()) if search.strip().upper() in d]
    selected = st.multiselect("Departamentos", options, default=options[:1], max_selections=5)
    years = st.multiselect("Años", sorted(df.year.unique(),reverse=True), default=sorted(df.year.unique(),reverse=True)[:2])
    diagnoses = st.multiselect("Diagnóstico", ["C","P","S"], default=["C","P","S"], format_func=lambda x:{"C":"Confirmado","P":"Probable","S":"Sospechoso"}[x])
    first,last = st.slider("Semanas",1,53,(1,53))
filtered = df[df.department.isin(selected)&df.year.isin(years)&df.diagnosis.isin(diagnoses)&df.week.between(first,last)]
weekly = filtered.groupby(["year","week"],as_index=False).notifications.sum()
st.subheader("Panorama")
st.caption(f"{', '.join(selected) or 'Sin departamentos'} · Años: {', '.join(map(str, sorted(years))) or 'sin selección'} · Semanas {first:02d}–{last:02d}")
c1,c2,c3,c4 = st.columns(4)
c1.metric("Notificaciones",f"{filtered.notifications.sum():,}",help="Conteo de registros para todos los filtros seleccionados.")
c2.metric("Departamentos",len(selected),help="Hasta cinco departamentos seleccionados; no indica cobertura nacional.")
c3.metric("Semana de mayor registro",f"{int(weekly.loc[weekly.notifications.idxmax(),'week']):02d} / {int(weekly.loc[weekly.notifications.idxmax(),'year'])}" if not weekly.empty else "—",help="Máximo semanal sumando departamentos y diagnósticos elegidos.")
c4.metric("Semanas con registros",len(weekly),help="Combinaciones año-semana con al menos un registro; no demuestra cobertura completa.")
st.caption("Notificaciones registradas, sin ajuste por población. La cobertura disponible puede variar entre años.")
if filtered.empty:
    st.info("No hay registros para los filtros seleccionados")
    st.stop()
trend,comparison,ranking,table = st.tabs(["Tendencia","Comparación","Ranking","Datos"])
def show(fig):
    palette = ["#138b87", "#ea785d", "#6885bc", "#cea048", "#9479af", "#609c45"]
    for i, trace in enumerate(fig.data):
        color = palette[i % len(palette)]
        if trace.type == "pie":
            trace.marker.colors = palette
        else:
            trace.marker.color = color
        if trace.type == "scatter":
            trace.line.color = color
            trace.line.width = 3
            trace.marker.size = 5
    fig.update_layout(template="plotly_dark" if dark else "plotly_white",paper_bgcolor=surface,plot_bgcolor=surface,font=dict(color=ink,family="Arial, sans-serif",size=12),height=410,margin=dict(l=24,r=24,t=32,b=24),legend=dict(orientation="h",y=1.14,x=0),hovermode="x unified")
    fig.update_xaxes(gridcolor=border,zeroline=False,title_font_color=muted)
    fig.update_yaxes(gridcolor=border,zeroline=False,title_font_color=muted)
    st.plotly_chart(fig,width="stretch",theme=None)
with trend:
    st.subheader("Evolución semanal")
    st.caption("Se suman los departamentos y diagnósticos seleccionados. Las semanas sin registro no se imputan como cero.")
    plot_weekly = weekly.copy()
    plot_weekly["year"] = plot_weekly.year.astype(str)
    by_type=filtered.groupby("diagnosis",as_index=False).notifications.sum()
    by_type["classification"] = by_type.diagnosis.map({"C":"Confirmado", "P":"Probable", "S":"Sospechoso"})
    line_column, composition_column = st.columns([2.2, 1])
    with line_column:
        show(px.line(plot_weekly,x="week",y="notifications",color="year",markers=True,labels={"week":"Semana epidemiológica","notifications":"Notificaciones","year":"Año"}))
    with composition_column:
        show(px.pie(by_type, names="classification", values="notifications", hole=.72, title="Clasificación diagnóstica"))
    st.caption("El snapshot puede tener cobertura parcial en un año. Una diferencia entre años no demuestra por sí sola una reducción de incidencia.")
with comparison:
    st.subheader("Comparación de departamentos")
    grouped=filtered.groupby(["department","year"],as_index=False).notifications.sum()
    grouped["year"] = grouped.year.astype(str)
    show(px.bar(grouped,x="department",y="notifications",color="year",barmode="group",labels={"department":"Departamento","notifications":"Notificaciones"}))
    st.info("Los conteos no están ajustados por población.")
with ranking:
    st.subheader("Departamentos con más notificaciones")
    st.caption("Ranking nacional: respeta años, diagnósticos y semanas; incluye todos los departamentos.")
    rank=df[df.year.isin(years)&df.diagnosis.isin(diagnoses)&df.week.between(first,last)].groupby("department",as_index=False).notifications.sum().nlargest(15,"notifications")
    show(px.bar(rank.sort_values("notifications"),x="notifications",y="department",orientation="h",labels={"department":"Departamento","notifications":"Notificaciones"}))
with table:
    st.dataframe(filtered.rename(columns={"year":"Año", "week":"Semana", "department":"Departamento", "diagnosis":"Diagnóstico", "notifications":"Notificaciones"}),width="stretch",hide_index=True)
    st.download_button("Descargar CSV filtrado",filtered.to_csv(index=False),file_name="dengue_filtrado.csv",mime="text/csv")
    st.markdown("[Fuente oficial MINSA](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue)")
    st.caption("Datos provisionales; visualización educativa, sin diagnóstico ni predicción.")
    st.caption(f"Procesamiento UTC: {metadata['generated_at_utc']} · Registros leídos: {metadata.get('source_rows', 'No informado')} · La fecha de procesamiento no equivale a la fecha de actualización del MINSA.")
    annual_path = path.with_name("annual.csv")
    if annual_path.exists():
        st.subheader("Resumen anual · modelo dbt")
        st.caption("Periodo anual disponible en el snapshot; este modelo no aplica el filtro de semanas. Filtra departamentos, años y diagnósticos.")
        annual = pd.read_csv(annual_path)
        annual = annual[annual.department.isin(selected) & annual.year.isin(years) & annual.diagnosis.isin(diagnoses)]
        st.dataframe(annual.rename(columns={"year":"Año", "department":"Departamento", "diagnosis":"Diagnóstico", "notifications":"Notificaciones", "reported_weeks":"Semanas con registro"}), width="stretch", hide_index=True)
