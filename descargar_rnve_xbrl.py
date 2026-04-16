#!/usr/bin/env python3
"""
DESCARGADOR DE EEFF DESDE RNVE - SUPERFINANCIERA
=================================================

Descarga archivos XBRL directamente del RNVE para los 5 emisores
y extrae datos de balance sheet (Deuda CP, Deuda LP, Acciones).

USO:
    python descargar_rnve_xbrl.py

REQUISITOS:
    pip install requests beautifulsoup4 lxml pandas

SALIDA:
    eeff_rnve_real.csv  (tabla con todos los datos)
    eeff_rnve_{emisor}.zip  (archivos XBRL raw para referencia)
"""

import os
import re
import json
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
from xml.etree import ElementTree as ET
from io import BytesIO
import zipfile

# ============================================================================
# CONFIG
# ============================================================================

EMISORES = {
    'Ecopetrol':      {'bvc': 'ECOPETROL', 'cik': '0001309402'},
    'Bancolombia':    {'bvc': 'BANCOLOMBIA', 'cik': '0001071236'},
    'Grupo Sura':     {'bvc': 'GRUPOSURA', 'cik': None},
    'Cementos Argos': {'bvc': 'CEMARGOS', 'cik': None},
    'Grupo Nutresa':  {'bvc': 'NUTRESA', 'cik': None},
}

AÑOS_RANGO = range(2017, 2022)  # 2017-2021

RNVE_BASE_URL = 'https://simev.superfinanciera.gov.co'
RNVE_DOWNLOAD_ENDPOINT = '/Reportes/api/reporteEstadosFinancieros'

# ============================================================================
# UTILIDADES
# ============================================================================

def crear_session():
    """Crea una sesión requests con headers realistas."""
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': RNVE_BASE_URL
    })
    return s

def buscar_emisor_rnve(session, ticker_bvc):
    """
    Busca el CIK/ID de un emisor en el RNVE.
    Retorna dict con {nit, cik, nombre} o None si no encuentra.
    """
    url = f'{RNVE_BASE_URL}/reportes/api/emisor/buscar'
    params = {'q': ticker_bvc}
    try:
        resp = session.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data and isinstance(data, list) and len(data) > 0:
            return data[0]  # Primer resultado
        return None
    except Exception as e:
        print(f'  ✗ Error buscando {ticker_bvc}: {e}')
        return None

def descargar_xbrl_anual(session, nit, año, tipo_info='IFRS'):
    """
    Descarga archivo XBRL anual de un emisor.
    Retorna bytes (ZIP) o None si falla.
    """
    url = f'{RNVE_BASE_URL}{RNVE_DOWNLOAD_ENDPOINT}'
    params = {
        'nit': nit,
        'año': año,
        'tipoInfo': tipo_info,
        'formato': 'xbrl'
    }
    try:
        resp = session.get(url, params=params, timeout=15)
        resp.raise_for_status()
        if len(resp.content) > 1000:  # Archivo válido (>1KB)
            return resp.content
        return None
    except Exception as e:
        print(f'    ✗ Error descargando {año}: {e}')
        return None

def parsear_xbrl(content_bytes, año):
    """
    Parsea archivo XBRL y extrae:
      deuda_cp (Passivos Corrientes / CL)
      deuda_lp (Pasivos No Corrientes / NCL)
      acciones (Acciones en circulación)
    
    Retorna dict {deuda_cp, deuda_lp, acciones} o {} si falla.
    """
    try:
        # Abrir ZIP interno
        zf = zipfile.ZipFile(BytesIO(content_bytes))
        xbrl_files = [f for f in zf.namelist() if f.endswith('.xml')]
        
        if not xbrl_files:
            return {}
        
        # Leer archivo principal (usualmente el primero)
        xbrl_content = zf.read(xbrl_files[0])
        root = ET.fromstring(xbrl_content)
        
        # Namespaces comunes en XBRL IFRS
        ns = {
            'ifrs': 'http://xbrl.ifrs.org/taxonomy/2017-07-31/ifrs-full',
            'us-gaap': 'http://fasb.org/us-gaap/2017-01-31',
            'xbrli': 'http://www.xbrl.org/2003/instance'
        }
        
        # Buscar contextos del final del año
        contexto_cierre = None
        for ctx in root.findall('.//xbrli:context', ns) or []:
            if f'{año}-12-31' in ctx.get('id', ''):
                contexto_cierre = ctx.get('id')
                break
        
        if not contexto_cierre:
            # Fallback: primer contexto disponible
            ctxs = root.findall('.//xbrli:context', ns)
            if ctxs:
                contexto_cierre = ctxs[0].get('id')
        
        resultado = {}
        
        # Extraer valores
        for elem in root.iter():
            # Pasivos Corrientes (IFRS)
            if 'Liabilities' in elem.tag and 'Current' in elem.tag:
                if contexto_cierre and contexto_cierre in elem.get('contextRef', ''):
                    try:
                        resultado['deuda_cp'] = float(elem.text or 0)
                    except:
                        pass
            
            # Pasivos No Corrientes (IFRS)
            elif 'Liabilities' in elem.tag and 'NonCurrent' in elem.tag:
                if contexto_cierre and contexto_cierre in elem.get('contextRef', ''):
                    try:
                        resultado['deuda_lp'] = float(elem.text or 0)
                    except:
                        pass
            
            # Acciones
            elif 'SharesOutstanding' in elem.tag or 'CommonStockSharesOutstanding' in elem.tag:
                if contexto_cierre and contexto_cierre in elem.get('contextRef', ''):
                    try:
                        resultado['acciones'] = float(elem.text or 0)
                    except:
                        pass
        
        return resultado
    
    except Exception as e:
        print(f'    Error parseando XBRL: {e}')
        return {}

# ============================================================================
# MAIN
# ============================================================================

def main():
    print('\n' + '='*70)
    print('DESCARGADOR DE EEFF DESDE RNVE - SUPERFINANCIERA')
    print('='*70 + '\n')
    
    session = crear_session()
    datos_consolidados = []
    
    for emisor_nombre, emisor_info in EMISORES.items():
        ticker_bvc = emisor_info['bvc']
        print(f'\n📊 {emisor_nombre} (BVC: {ticker_bvc})')
        print('-' * 70)
        
        # Buscar en RNVE
        print(f'  Buscando en RNVE...', end=' ', flush=True)
        info = buscar_emisor_rnve(session, ticker_bvc)
        
        if not info:
            print('✗ No encontrado')
            continue
        
        nit = info.get('nit')
        print(f'✓ NIT: {nit}')
        
        # Descargar para cada año
        for año in AÑOS_RANGO:
            print(f'  {año}: ', end='', flush=True)
            
            # Descargar XBRL
            xbrl_bytes = descargar_xbrl_anual(session, nit, año, 'IFRS')
            
            if not xbrl_bytes:
                print('✗ sin datos')
                continue
            
            print('✓ descargado', end=' ')
            
            # Guardar ZIP para referencia
            zip_name = f'eeff_rnve_{emisor_nombre.replace(" ", "_")}_{año}.zip'
            with open(zip_name, 'wb') as f:
                f.write(xbrl_bytes)
            
            # Parsear
            campos = parsear_xbrl(xbrl_bytes, año)
            
            if campos:
                print(f'→ parseado')
                datos_consolidados.append({
                    'emisor': emisor_nombre,
                    'año': año,
                    'deuda_cp_rnve': campos.get('deuda_cp'),
                    'deuda_lp_rnve': campos.get('deuda_lp'),
                    'acciones_rnve': campos.get('acciones'),
                })
            else:
                print('✗ error parsing')
    
    # Guardar CSV
    if datos_consolidados:
        df = pd.DataFrame(datos_consolidados)
        df = df.sort_values(['emisor', 'año']).reset_index(drop=True)
        
        salida = 'eeff_rnve_real.csv'
        df.to_csv(salida, index=False, encoding='utf-8-sig')
        
        print('\n' + '='*70)
        print(f'✓ Descarga completada: {salida}')
        print('='*70 + '\n')
        print(df.to_string(index=False))
        print(f'\nRegistros: {len(df)} (año x emisor)')
        print('\n→ Copia este archivo a:')
        print('  parte_1/eeff_rnve_real.csv')
    else:
        print('\n✗ No se descargó ningún dato')

if __name__ == '__main__':
    main()
