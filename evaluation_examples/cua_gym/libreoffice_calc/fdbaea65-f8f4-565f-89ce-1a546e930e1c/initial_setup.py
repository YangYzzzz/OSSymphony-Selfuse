"""
Initial Setup: Create a European-style semicolon-delimited CSV file and open LibreOffice Calc
Task ID: calc_gsi_029
Domain: libreoffice_calc
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_029'
CSV_FILE = f'{WORKDIR}/european_sales.csv'

def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)

def create_initial():
    # Create a semicolon-delimited CSV with UTF-8 special characters
    # European-style data with accented names, euro symbol, etc.
    csv_content = """\
Employee ID;Full Name;Department;City;Quarterly Sales (\u20ac);Commission Rate;Start Date;Notes
1001;S\u00e9bastien Lefebvre;Ventes;Paris;45230.50;0.12;2023-01-15;Top performer r\u00e9gion Nord
1002;M\u00fcller, Hans-J\u00fcrgen;Vertrieb;M\u00fcnchen;38750.00;0.10;2022-06-01;Gro\u00dfkunden-Manager
1003;Mar\u00eda Jos\u00e9 Garc\u00eda;Ventas;Madrid;52100.75;0.15;2021-11-20;Directora de zona sur
1004;Fran\u00e7oise Dubois;Marketing;Lyon;29800.25;0.08;2023-03-10;Sp\u00e9cialiste digital
1005;Lars \u00d8stergaard;Salg;K\u00f8benhavn;41500.00;0.11;2022-09-05;Nordisk regionchef
1006;Gra\u017cyna Kowalska;Sprzeda\u017c;Warszawa;33200.50;0.09;2023-07-22;Nowy cz\u0142onek zespo\u0142u
1007;Alessandra Bianchi;Vendite;Milano;47800.00;0.13;2021-04-18;Responsabile clienti Premium
1008;J\u00f6rg Schr\u00f6der;Einkauf;K\u00f6ln;28500.75;0.07;2022-12-01;Einkaufsabteilung Leiter
1009;Bj\u00f6rn Lindstr\u00f6m;F\u00f6rs\u00e4ljning;Stockholm;39600.25;0.10;2023-05-14;Skandinavisk mark.ansvarig
1010;\u00c9lodie Moreau;Comptabilit\u00e9;Bruxelles;26400.00;0.06;2022-02-28;Analyste financi\u00e8re senior
1011;Tom\u00e1\u0161 Nov\u00e1k;Obchod;Praha;31750.50;0.09;2023-08-10;St\u0159edoevropsk\u00fd t\u00fdm
1012;Cec\u00edlia Ferreira;Vendas;Lisboa;35900.75;0.10;2021-10-05;Mercado ib\u00e9rico
1013;Andr\u00e9 Fontaine;Logistique;Marseille;22800.00;0.05;2023-02-17;Responsable entrep\u00f4t Sud
1014;Kl\u00e1ra Szab\u00f3;\u00c9rt\u00e9kes\u00edt\u00e9s;Budapest;29100.25;0.08;2022-07-30;K\u00f6z\u00e9p-eur\u00f3pai iroda
1015;Nikolaos Papadopoulos;Poliseis;Athina;27600.50;0.07;2023-04-01;Mesogeiako tmima"""

    with open(CSV_FILE, 'w', encoding='utf-8') as f:
        f.write(csv_content)

    print(f'CSV file created: {CSV_FILE}')

    # Verify file exists and has content
    size = os.path.getsize(CSV_FILE)
    print(f'File size: {size} bytes')

    # Open LibreOffice Calc (empty) so the agent can open the CSV via File > Open
    launch_gui('libreoffice --calc', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc with DISPLAY=:0')

create_initial()
