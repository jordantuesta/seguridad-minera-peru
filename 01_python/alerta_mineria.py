"""
=============================================================
SISTEMA DE ALERTA AUTOMÁTICA - SEGURIDAD MINERA PERÚ
=============================================================
Pipeline: Python (limpieza) → Power BI (análisis) → Python (alerta)
Autor: Jordan Tuesta
Fuente de datos: MINEM 2002-2021 | 901 registros
=============================================================
"""

import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
#from google.colab import files
#archivo = files.upload() -- Estos dos pasos los puede ejecutar si necesita subir un archivo con nombre diferente pero mismas columnas!
# CONFIGURACIÓN - Editar antes de ejecutar
REMITENTE = "jordantuesta@gmail.com" # Ingresar su correo remitente.
CONTRASENA = "haoq pany omjt luvc"   # Ingresar la contraseña de aplicaciones obtenida desde el gmail.
DESTINATARIO = "jordantuesta@gmail.com"       # Ingresar separado por ";" los correos de interés.
RUTA_CSV = "accidentes_FINAL_powerbi.csv"  # Si cambia el nombre del archivo modifiquelo aquí.

# PASO 1 - Cargar y preparar datos
def cargar_datos(ruta):
    df = pd.read_csv(ruta, encoding="utf-8")
    df.columns = df.columns.str.strip().str.upper()
    df["AÑO"] = pd.to_numeric(df["AÑO"], errors="coerce")
    df["MES"] = pd.to_numeric(df["MES"], errors="coerce")
    return df

# PASO 2 - Calcular métricas
def calcular_metricas(df):
    # Excluir años del gap (2017-2019) del promedio histórico
    df_sin_gap = df[~df["AÑO"].isin([2017, 2018, 2019])]

    # Promedio mensual histórico
    accidentes_por_mes = (
        df_sin_gap.groupby(["AÑO", "MES"])
        .size()
        .reset_index(name="TOTAL")
    )
    promedio_historico = accidentes_por_mes["TOTAL"].mean()

    # Simular "mes actual" con el último mes disponible en el dataset
    ultimo_año = int(df["AÑO"].max())
    ultimo_mes = int(df[df["AÑO"] == ultimo_año]["MES"].max())
    accidentes_mes_actual = len(
        df[(df["AÑO"] == ultimo_año) & (df["MES"] == ultimo_mes)]
    )

    # Causa principal del período
    causa_top = df["CAUSA_AGRUPADA"].value_counts().idxmax()
    casos_causa_top = df["CAUSA_AGRUPADA"].value_counts().max()

    # Departamento más afectado
    depto_top = df["DEPARTAMENTO"].value_counts().idxmax()

    return {
        "promedio_historico": round(promedio_historico, 2),
        "accidentes_mes_actual": accidentes_mes_actual,
        "ultimo_año": ultimo_año,
        "ultimo_mes": ultimo_mes,
        "causa_top": causa_top,
        "casos_causa_top": casos_causa_top,
        "depto_top": depto_top,
        "total_historico": len(df),
        "es_alerta": accidentes_mes_actual > promedio_historico
    }

# PASO 3 - Generar HTML del email

def generar_html(m):
    if m["es_alerta"]:
        color_header = "#D85A30"
        icono = "🔴"
        estado = "ALERTA"
        mensaje_estado = f"Se registraron <strong>{m['accidentes_mes_actual']}</strong> accidentes en el período analizado, superando el promedio histórico mensual de <strong>{m['promedio_historico']}</strong> casos."
        color_badge = "#FAECE7"
        color_badge_texto = "#993C1D"
    else:
        color_header = "#1D9E75"
        icono = "🟢"
        estado = "NORMAL"
        mensaje_estado = f"Se registraron <strong>{m['accidentes_mes_actual']}</strong> accidentes en el período analizado, dentro del promedio histórico mensual de <strong>{m['promedio_historico']}</strong> casos."
        color_badge = "#EAF3DE"
        color_badge_texto = "#27500A"

    nombres_meses = {
        1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",
        5:"Mayo",6:"Junio",7:"Julio",8:"Agosto",
        9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"
    }
    nombre_mes = nombres_meses.get(m["ultimo_mes"], str(m["ultimo_mes"]))
 # Para la creación del archivo de html pueden pedirle a cualquier IA que con un modelo del correo que deseen e insertando el codigo de hasta arriba para que les haga una vista personalizada.
    html = f"""
<!DOCTYPE html>
<html>
<body style="font-family:Segoe UI,Arial,sans-serif;background:#F0F4F8;padding:20px;margin:0">
  <div style="max-width:600px;margin:auto;background:#fff;border-radius:10px;overflow:hidden;border:1px solid #E0E5EC">

    <!-- Header -->
    <div style="background:#1A3A5C;padding:18px 22px">
      <h2 style="color:#fff;margin:0;font-size:16px;font-weight:500">
        ⛏ Sistema de Alerta · Seguridad Minera Perú
      </h2>
      <p style="color:#8FBCD4;margin:5px 0 0;font-size:11px">
        Elaborado por Jordan Tuesta · Pipeline automatizado con Python
      </p>
    </div>

    <!-- Estado principal -->
    <div style="padding:20px 22px">
      <div style="background:{color_badge};border-left:4px solid {color_header};padding:14px 16px;border-radius:6px;margin-bottom:18px">
        <strong style="color:{color_badge_texto};font-size:15px">{icono} {estado}: {nombre_mes} {m['ultimo_año']}</strong>
        <p style="color:{color_badge_texto};margin:8px 0 0;font-size:13px">{mensaje_estado}</p>
      </div>

      <!-- Tabla de métricas -->
      <table style="width:100%;border-collapse:collapse;font-size:13px">
        <tr style="background:#F0F4F8">
          <td style="padding:8px 12px;color:#7A8A9A;font-size:10px;text-transform:uppercase;font-weight:500">Métrica</td>
          <td style="padding:8px 12px;color:#7A8A9A;font-size:10px;text-transform:uppercase;font-weight:500">Valor</td>
          <td style="padding:8px 12px;color:#7A8A9A;font-size:10px;text-transform:uppercase;font-weight:500">Estado</td>
        </tr>
        <tr style="border-bottom:1px solid #F0F4F8">
          <td style="padding:9px 12px;color:#1A3A5C">Accidentes del período</td>
          <td style="padding:9px 12px;font-weight:600;color:{color_header};font-size:15px">{m['accidentes_mes_actual']}</td>
          <td style="padding:9px 12px">
            <span style="background:{color_badge};color:{color_badge_texto};padding:3px 10px;border-radius:20px;font-size:10px;font-weight:500">{icono} {estado}</span>
          </td>
        </tr>
        <tr style="border-bottom:1px solid #F0F4F8">
          <td style="padding:9px 12px;color:#1A3A5C">Promedio histórico mensual</td>
          <td style="padding:9px 12px;font-weight:500;color:#1A3A5C">{m['promedio_historico']}</td>
          <td style="padding:9px 12px">
            <span style="background:#E6F1FB;color:#0C447C;padding:3px 10px;border-radius:20px;font-size:10px">Referencia</span>
          </td>
        </tr>
        <tr style="border-bottom:1px solid #F0F4F8">
          <td style="padding:9px 12px;color:#1A3A5C">Causa principal histórica</td>
          <td style="padding:9px 12px;font-weight:500;color:#1A3A5C">{m['causa_top']}</td>
          <td style="padding:9px 12px">
            <span style="background:#FAEEDA;color:#633806;padding:3px 10px;border-radius:20px;font-size:10px">{m['casos_causa_top']} casos (27%)</span>
          </td>
        </tr>
        <tr>
          <td style="padding:9px 12px;color:#1A3A5C">Dpto. más afectado</td>
          <td style="padding:9px 12px;font-weight:500;color:#1A3A5C">{m['depto_top']}</td>
          <td style="padding:9px 12px">
            <span style="background:#E6F1FB;color:#0C447C;padding:3px 10px;border-radius:20px;font-size:10px">Región Centro</span>
          </td>
        </tr>
      </table>

      <!-- Hallazgo clave -->
      <div style="background:#EAF3DE;border-left:3px solid #1D9E75;border-radius:4px;padding:10px 14px;margin-top:16px">
        <strong style="color:#0F6E56;font-size:12px">💡 Hallazgo clave del análisis histórico:</strong>
        <p style="color:#27500A;font-size:11px;margin:5px 0 0;line-height:1.5">
          Desprendimiento de rocas representa el 27% de los {m['total_historico']} accidentes históricos.
          Concentrado en Región Centro (minería subterránea). Una intervención focalizada
          en esta causa reduciría el 27% de las muertes históricas.
        </p>
      </div>
    </div>

    <!-- Footer -->
    <div style="background:#1A3A5C;padding:12px 22px">
      <p style="color:#8FBCD4;font-size:10px;margin:0;line-height:1.6">
        Generado automáticamente · {datetime.now().strftime('%d/%m/%Y %H:%M')}<br>
        Pipeline: Python (limpieza + alerta) → Power BI (análisis interactivo)<br>
        Datos: MINEM 2002–2021 · {m['total_historico']} registros · Jordan Tuesta
      </p>
    </div>

  </div>
</body>
</html>
"""
    return html

# PASO 4 - Enviar email via Gmail SMTP

def enviar_email(metricas, remitente, contrasena, destinatario):
    nombres_meses = {
        1:"Ene",2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",
        7:"Jul",8:"Ago",9:"Sep",10:"Oct",11:"Nov",12:"Dic"
    }
    mes_str = nombres_meses.get(metricas["ultimo_mes"], str(metricas["ultimo_mes"]))
    icono = "🔴" if metricas["es_alerta"] else "🟢"
    estado = "ALERTA" if metricas["es_alerta"] else "Normal"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"{icono} Seguridad Minera · {estado} · {mes_str} {metricas['ultimo_año']} · {metricas['accidentes_mes_actual']} accidentes"
    msg["From"] = remitente
    msg["To"] = destinatario

    html = generar_html(metricas)
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, contrasena)
            servidor.sendmail(remitente, destinatario, msg.as_string())
        print(f"✅ Email enviado exitosamente a {destinatario}")
        print(f"   Estado: {icono} {estado}")
        print(f"   Accidentes período: {metricas['accidentes_mes_actual']}")
        print(f"   Promedio histórico: {metricas['promedio_historico']}")
    except Exception as e:
        print(f"❌ Error al enviar email: {e}")
        print("   Verifica la contraseña de aplicación de Gmail (ver instrucciones)")

# PASO 5 - Ejecutar pipeline completo

if __name__ == "__main__":
    print("=" * 55)
    print("SISTEMA DE ALERTA - SEGURIDAD MINERA PERÚ")
    print("Autor: Jordan Tuesta")
    print("=" * 55)

    print("\n📂 Cargando datos MINEM...")
    df = cargar_datos(RUTA_CSV)
    print(f"   {len(df)} registros cargados · {df['AÑO'].nunique()} años")

    print("\n📊 Calculando métricas...")
    metricas = calcular_metricas(df)
    print(f"   Promedio histórico mensual: {metricas['promedio_historico']}")
    print(f"   Período analizado: {metricas['ultimo_mes']}/{metricas['ultimo_año']}")
    print(f"   Accidentes en período: {metricas['accidentes_mes_actual']}")
    print(f"   Estado: {'🔴 ALERTA' if metricas['es_alerta'] else '🟢 Normal'}")

    print("\n📧 Enviando email de alerta...")
    enviar_email(metricas, REMITENTE, CONTRASENA, DESTINATARIO)

    print("\n✅ Pipeline completado exitosamente")
    print("=" * 55)
