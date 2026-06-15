"""
Initial Setup: Delete lines 5-12 (discontinued products) from inventory.csv
Task ID: vscode_edit_073
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Desktop'
TASK_ID = 'vscode_edit_073'
OUTPUT = f'{WORKDIR}/inventory.csv'


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
    os.makedirs(WORKDIR, exist_ok=True)

    # 30-line CSV: line 1 header, lines 2-4 active, lines 5-12 discontinued, lines 13-30 active
    # Total: 1 + 3 + 8 + 18 = 30 lines
    lines = [
        # Line 1: header
        "product_id,product_name,category,unit_price,stock_quantity,supplier,status",
        # Lines 2-4: active products
        "P001,Organic Green Tea,Beverages,12.50,340,TeaHouse Co.,active",
        "P002,Stainless Steel Water Bottle,Kitchen,24.99,185,HomeGoods Ltd.,active",
        "P003,Whole Grain Crackers,Snacks,4.75,520,NaturalBite Inc.,active",
        # Lines 5-12: discontinued products
        "P004,Classic Cola 2L,Beverages,2.99,0,SoftDrink Corp.,discontinued",
        "P005,Plastic Straw Set 100pk,Kitchen,1.49,0,EcoFail Supplies,discontinued",
        "P006,Sugary Cereal Loops,Snacks,3.99,0,OldBrand Foods,discontinued",
        "P007,Vinyl Record Cleaner,Electronics,8.75,0,RetroTech Ltd.,discontinued",
        "P008,Fax Machine Paper Roll,Office,5.25,0,LegacyOffice Co.,discontinued",
        "P009,Cassette Tape Blank,Electronics,3.50,0,MediaVault Inc.,discontinued",
        "P010,Overhead Projector Bulb,Office,22.00,0,ClassicAV Supplies,discontinued",
        "P011,Typewriter Ribbon,Office,6.99,0,VintageType Co.,discontinued",
        # Lines 13-30: active products
        "P012,Cold Brew Coffee Concentrate,Beverages,14.99,210,BrewMaster Co.,active",
        "P013,Bamboo Cutting Board,Kitchen,19.95,95,EcoHome Goods,active",
        "P014,Trail Mix Assorted Nuts,Snacks,8.50,430,NutriSnack Ltd.,active",
        "P015,Wireless Earbuds,Electronics,49.99,78,SoundTech Inc.,active",
        "P016,Ergonomic Mouse Pad,Office,15.00,163,DeskPro Supplies,active",
        "P017,Sparkling Mineral Water 6pk,Beverages,6.25,280,AquaFresh Co.,active",
        "P018,Cast Iron Skillet 10in,Kitchen,39.99,47,IronCook Ltd.,active",
        "P019,Protein Bar Variety 12pk,Snacks,22.00,195,FitFuel Inc.,active",
        "P020,USB-C Hub 7-port,Electronics,34.50,112,TechLink Corp.,active",
        "P021,Legal Notepad 3pk,Office,7.99,320,PaperWorks Ltd.,active",
        "P022,Herbal Chamomile Tea 20ct,Beverages,9.75,255,TeaHouse Co.,active",
        "P023,Silicone Spatula Set,Kitchen,11.25,138,KitchenPro Inc.,active",
        "P024,Dark Chocolate Almonds,Snacks,6.50,380,SweetNut Co.,active",
        "P025,Smart Plug Wi-Fi 4pk,Electronics,27.99,89,HomeAuto Ltd.,active",
        "P026,Desk Organizer Bamboo,Office,18.50,74,EcoDesk Supplies,active",
        "P027,Kombucha Original 12oz,Beverages,4.25,310,FermentFresh Co.,active",
        "P028,Non-stick Baking Sheet,Kitchen,13.75,122,BakeRight Ltd.,active",
        "P029,Granola Clusters Honey,Snacks,5.99,445,MorningCrunch Inc.,active",
    ]

    # Verify we have exactly 30 lines
    assert len(lines) == 30, f"Expected 30 lines, got {len(lines)}"

    with open(OUTPUT, 'w') as f:
        f.write('\n'.join(lines) + '\n')

    print(f'Initial file created: {OUTPUT}')
    print(f'Total lines: {len(lines)}')
    print(f'Lines 5-12 are discontinued products (to be deleted by agent)')

    # GUI-ready startup: open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
