import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.widgets import RadioButtons, Button, TextBox
from matplotlib.lines import Line2D
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# --- [FIX 1] Import WebDriverWait and Expected Conditions ---
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import re
import os

# --- [CONFIGURATION] ---
# Initial number of shares (will be updated by command)
SHARES = 1 
# Initial Ticker
current_ticker = "BTC_USD"
# Path to your stock list
CSV_FILE_PATH = "ind_nifty500list.csv"

# --- [SETUP] Check for CSV and create it if not found ---
if not os.path.exists(CSV_FILE_PATH):
    print(f"'{CSV_FILE_PATH}' not found. Creating it from internal data.")
    csv_content = """Company Name,Industry,Symbol,Series,ISIN Code
360 ONE WAM Ltd.,Financial Services,360ONE,EQ,INE466L01038
3M India Ltd.,Diversified,3MINDIA,EQ,INE470A01017
ABB India Ltd.,Capital Goods,ABB,EQ,INE117A01022
ACC Ltd.,Construction Materials,ACC,EQ,INE012A01025
ACME Solar Holdings Ltd.,Power,ACMESOLAR,EQ,INE622W01025
AIA Engineering Ltd.,Capital Goods,AIAENG,EQ,INE212H01026
APL Apollo Tubes Ltd.,Capital Goods,APLAPOLLO,EQ,INE702C01027
AU Small Finance Bank Ltd.,Financial Services,AUBANK,EQ,INE949L01017
AWL Agri Business Ltd.,Fast Moving Consumer Goods,AWL,EQ,INE699H01024
Aadhar Housing Finance Ltd.,Financial Services,AADHARHFC,EQ,INE883F01010
Aarti Industries Ltd.,Chemicals,AARTIIND,EQ,INE769A01020
Aavas Financiers Ltd.,Financial Services,AAVAS,EQ,INE216P01012
Abbott India Ltd.,Healthcare,ABBOTINDIA,EQ,INE358A01014
Action Construction Equipment Ltd.,Capital Goods,ACE,EQ,INE731H01025
Adani Energy Solutions Ltd.,Power,ADANIENSOL,EQ,INE931S01010
Adani Enterprises Ltd.,Metals & Mining,ADANIENT,EQ,INE423A01024
Adani Green Energy Ltd.,Power,ADANIGREEN,EQ,INE364U01010
Adani Ports and Special Economic Zone Ltd.,Services,ADANIPORTS,EQ,INE742F01042
Adani Power Ltd.,Power,ADANIPOWER,EQ,INE814H01011
Adani Total Gas Ltd.,Oil Gas & Consumable Fuels,ATGL,EQ,INE399L01023
Aditya Birla Capital Ltd.,Financial Services,ABCAPITAL,EQ,INE674K01013
Aditya Birla Fashion and Retail Ltd.,Consumer Services,ABFRL,EQ,INE647O01011
Aditya Birla Real Estate Ltd.,Forest Materials,ABREL,EQ,INE055A01016
Aditya Birla Sun Life AMC Ltd.,Financial Services,ABSLAMC,EQ,INE404A01024
Aegis Logistics Ltd.,Oil Gas & Consumable Fuels,AEGISLOG,EQ,INE208C01025
Afcons Infrastructure Ltd.,Construction,AFCONS,EQ,INE101I01011
Affle 3i Ltd.,Information Technology,AFFLE,EQ,INE00WC01027
Ajanta Pharmaceuticals Ltd.,Healthcare,AJANTPHARM,EQ,INE031B01049
Akums Drugs and Pharmaceuticals Ltd.,Healthcare,AKUMS,EQ,INE09XN01023
Alembic Pharmaceuticals Ltd.,Healthcare,APLLTD,EQ,INE901L01018
Alivus Life Sciences Ltd.,Healthcare,ALIVUS,EQ,INE03Q201024
Alkem Laboratories Ltd.,Healthcare,ALKEM,EQ,INE540L01014
Alkyl Amines Chemicals Ltd.,Chemicals,ALKYLAMINE,EQ,INE150B01039
Alok Industries Ltd.,Textiles,ALOKINDS,EQ,INE270A01029
Amara Raja Energy & Mobility Ltd.,Automobile and Auto Components,ARE&M,EQ,INE885A01032
Amber Enterprises India Ltd.,Consumer Durables,AMBER,EQ,INE371P01015
Ambuja Cements Ltd.,Construction Materials,AMBUJACEM,EQ,INE079A01024
Anand Rathi Wealth Ltd.,Financial Services,ANANDRATHI,EQ,INE463V01026
Anant Raj Ltd.,Realty,ANANTRAJ,EQ,INE242C01024
Angel One Ltd.,Financial Services,ANGELONE,EQ,INE732I01013
Apar Industries Ltd.,Capital Goods,APARINDS,EQ,INE372A01015
Apollo Hospitals Enterprise Ltd.,Healthcare,APOLLOHOSP,EQ,INE437A01024
Apollo Tyres Ltd.,Automobile and Auto Components,APOLLOTYRE,EQ,INE438A01022
Aptus Value Housing Finance India Ltd.,Financial Services,APTUS,EQ,INE852O01025
Asahi India Glass Ltd.,Automobile and Auto Components,ASAHIINDIA,EQ,INE439A01020
Ashok Leyland Ltd.,Capital Goods,ASHOKLEY,EQ,INE208A01029
Asian Paints Ltd.,Consumer Durables,ASIANPAINT,EQ,INE021A01026
Aster DM Healthcare Ltd.,Healthcare,ASTERDM,EQ,INE914M01019
AstraZenca Pharma India Ltd.,Healthcare,ASTRAZEN,EQ,INE203A01020
Astral Ltd.,Capital Goods,ASTRAL,EQ,INE006I01046
Atul Ltd.,Chemicals,ATUL,EQ,INE100A01010
Aurobindo Pharma Ltd.,Healthcare,AUROPHARMA,EQ,INE406A01037
Authum Investment & Infrastructure Ltd.,Financial Services,AIIL,EQ,INE206F01022
Avenue Supermarts Ltd.,Consumer Services,DMART,EQ,INE192R01011
Axis Bank Ltd.,Financial Services,AXISBANK,EQ,INE238A01034
BASF India Ltd.,Chemicals,BASF,EQ,INE373A01013
BEML Ltd.,Capital Goods,BEML,EQ,INE258A01016
BLS International Services Ltd.,Consumer Services,BLS,EQ,INE153T01027
BSE Ltd.,Financial Services,BSE,EQ,INE118H01025
Bajaj Auto Ltd.,Automobile and Auto Components,BAJAJ-AUTO,EQ,INE917I01010
Bajaj Finance Ltd.,Financial Services,BAJFINANCE,EQ,INE296A01032
Bajaj Finserv Ltd.,Financial Services,BAJAJFINSV,EQ,INE918I01026
Bajaj Holdings & Investment Ltd.,Financial Services,BAJAJHLDNG,EQ,INE118A01012
Bajaj Housing Finance Ltd.,Financial Services,BAJAJHFL,EQ,INE377Y01014
Balkrishna Industries Ltd.,Automobile and Auto Components,BALKRISIND,EQ,INE787D01026
Balrampur Chini Mills Ltd.,Fast Moving Consumer Goods,BALRAMCHIN,EQ,INE119A01028
Bandhan Bank Ltd.,Financial Services,BANDHANBNK,EQ,INE545U01014
Bank of Baroda,Financial Services,BANKBARODA,EQ,INE028A01039
Bank of India,Financial Services,BANKINDIA,EQ,INE084A01016
Bank of Maharashtra,Financial Services,MAHABANK,EQ,INE457A01014
Bata India Ltd.,Consumer Durables,BATAINDIA,EQ,INE176A01028
Bayer Cropscience Ltd.,Chemicals,BAYERCROP,EQ,INE462A01022
Berger Paints India Ltd.,Consumer Durables,BERGEPAINT,EQ,INE463A01038
Bharat Dynamics Ltd.,Capital Goods,BDL,EQ,INE171Z01026
Bharat Electronics Ltd.,Capital Goods,BEL,EQ,INE263A01024
Bharat Forge Ltd.,Automobile and Auto Components,BHARATFORG,EQ,INE465A01025
Bharat Heavy Electricals Ltd.,Capital Goods,BHEL,EQ,INE257A01026
Bharat Petroleum Corporation Ltd.,Oil Gas & Consumable Fuels,BPCL,EQ,INE029A01011
Bharti Airtel Ltd.,Telecommunication,BHARTIARTL,EQ,INE397D01024
Bharti Hexacom Ltd.,Telecommunication,BHARTIHEXA,EQ,INE343G01021
Bikaji Foods International Ltd.,Fast Moving Consumer Goods,BIKAJI,EQ,INE00E101023
Biocon Ltd.,Healthcare,BIOCON,EQ,INE376G01013
Birlasoft Ltd.,Information Technology,BSOFT,EQ,INE836A01035
Blue Dart Express Ltd.,Services,BLUEDART,EQ,INE233B01017
Blue Star Ltd.,Consumer Durables,BLUESTARCO,EQ,INE472A01039
Bombay Burmah Trading Corporation Ltd.,Fast Moving Consumer Goods,BBTC,EQ,INE050A01025
Bosch Ltd.,Automobile and Auto Components,BOSCHLTD,EQ,INE323A01026
Brainbees Solutions Ltd.,Consumer Services,FIRSTCRY,EQ,INE02RE01045
Brigade Enterprises Ltd.,Realty,BRIGADE,EQ,INE791I01019
Britannia Industries Ltd.,Fast Moving Consumer Goods,BRITANNIA,EQ,INE216A01030
C.E. Info Systems Ltd.,Information Technology,MAPMYINDIA,EQ,INE0BV301023
CCL Products (I) Ltd.,Fast Moving Consumer Goods,CCL,EQ,INE421D01022
CESC Ltd.,Power,CESC,EQ,INE486A01021
CG Power and Industrial Solutions Ltd.,Capital Goods,CGPOWER,EQ,INE067A01029
CRISIL Ltd.,Financial Services,CRISIL,EQ,INE007A01025
Campus Activewear Ltd.,Consumer Durables,CAMPUS,EQ,INE278Y01022
Can Fin Homes Ltd.,Financial Services,CANFINHOME,EQ,INE477A01020
Canara Bank,Financial Services,CANBK,EQ,INE476A01022
Caplin Point Laboratories Ltd.,Healthcare,CAPLIPOINT,EQ,INE475E01026
Capri Global Capital Ltd.,Financial Services,CGCL,EQ,INE180C01042
Carborundum Universal Ltd.,Capital Goods,CARBORUNIV,EQ,INE120A01034
Castrol India Ltd.,Oil Gas & Consumable Fuels,CASTROLIND,EQ,INE172A01027
Ceat Ltd.,Automobile and Auto Components,CEATLTD,EQ,INE482A01020
Central Bank of India,Financial Services,CENTRALBK,EQ,INE483A01010
Central Depository Services (India) Ltd.,Financial Services,CDSL,EQ,INE736A01011
Century Plyboards (India) Ltd.,Consumer Durables,CENTURYPLY,EQ,INE348B01021
Cera Sanitaryware Ltd,Consumer Durables,CERA,EQ,INE739E01017
Chalet Hotels Ltd.,Consumer Services,CHALET,EQ,INE427F01016
Chambal Fertilizers & Chemicals Ltd.,Chemicals,CHAMBLFERT,EQ,INE085A01013
Chennai Petroleum Corporation Ltd.,Oil Gas & Consumable Fuels,CHENNPETRO,EQ,INE178A01016
Cholamandalam Financial Holdings Ltd.,Financial Services,CHOLAHLDNG,EQ,INE149A01033
Cholamandalam Investment and Finance Company Ltd.,Financial Services,CHOLAFIN,EQ,INE121A01024
Cipla Ltd.,Healthcare,CIPLA,EQ,INE059A01026
City Union Bank Ltd.,Financial Services,CUB,EQ,INE491A01021
Clean Science and Technology Ltd.,Chemicals,CLEAN,EQ,INE227W01023
Coal India Ltd.,Oil Gas & Consumable Fuels,COALINDIA,EQ,INE522F01014
Cochin Shipyard Ltd.,Capital Goods,COCHINSHIP,EQ,INE704P01025
Coforge Ltd.,Information Technology,COFORGE,EQ,INE591G01025
Cohance Lifesciences Ltd.,Healthcare,COHANCE,EQ,INE03QK01018
Colgate Palmolive (India) Ltd.,Fast Moving Consumer Goods,COLPAL,EQ,INE259A01022
Computer Age Management Services Ltd.,Financial Services,CAMS,EQ,INE596I01012
Concord Biotech Ltd.,Healthcare,CONCORDBIO,EQ,INE338H01029
Container Corporation of India Ltd.,Services,CONCOR,EQ,INE111A01025
Coromandel International Ltd.,Chemicals,COROMANDEL,EQ,INE169A01031
Craftsman Automation Ltd.,Automobile and Auto Components,CRAFTSMAN,EQ,INE00LO01017
CreditAccess Grameen Ltd.,Financial Services,CREDITACC,EQ,INE741K01010
Crompton Greaves Consumer Electricals Ltd.,Consumer Durables,CROMPTON,EQ,INE299U01018
Cummins India Ltd.,Capital Goods,CUMMINSIND,EQ,INE298A01020
Cyient Ltd.,Information Technology,CYIENT,EQ,INE136B01020
DCM Shriram Ltd.,Diversified,DCMSHRIRAM,EQ,INE499A01024
DLF Ltd.,Realty,DLF,EQ,INE271C01023
DOMS Industries Ltd.,Fast Moving Consumer Goods,DOMS,EQ,INE321T01012
Dabur India Ltd.,Fast Moving Consumer Goods,DABUR,EQ,INE016A01026
Dalmia Bharat Ltd.,Construction Materials,DALBHARAT,EQ,INE00R701025
Data Patterns (India) Ltd.,Capital Goods,DATAPATTNS,EQ,INE0IX101010
Deepak Fertilisers & Petrochemicals Corp. Ltd.,Chemicals,DEEPAKFERT,EQ,INE501A01019
Deepak Nitrite Ltd.,Chemicals,DEEPAKNTR,EQ,INE288B01029
Delhivery Ltd.,Services,DELHIVERY,EQ,INE148O01028
Devyani International Ltd.,Consumer Services,DEVYANI,EQ,INE872J01023
Divi's Laboratories Ltd.,Healthcare,DIVISLAB,EQ,INE361B01024
Dixon Technologies (India) Ltd.,Consumer Durables,DIXON,EQ,INE935N01020
Dr. Lal Path Labs Ltd.,Healthcare,LALPATHLAB,EQ,INE600L01024
Dr. Reddy's Laboratories Ltd.,Healthcare,DRREDDY,EQ,INE089A01031
Dummy Valor Estate Ltd.,Consumer Services,DUMMYDBRLT,BE,DUM879I01012
E.I.D. Parry (India) Ltd.,Fast Moving Consumer Goods,EIDPARRY,EQ,INE126A01031
EIH Ltd.,Consumer Services,EIHOTEL,EQ,INE230A01023
Eicher Motors Ltd.,Automobile and Auto Components,EICHERMOT,EQ,INE066A01021
Elecon Engineering Co. Ltd.,Capital Goods,ELECON,EQ,INE205B01031
Elgi Equipments Ltd.,Capital Goods,ELGIEQUIP,EQ,INE285A01027
Emami Ltd.,Fast Moving Consumer Goods,EMAMILTD,EQ,INE548C01032
Emcure Pharmaceuticals Ltd.,Healthcare,EMCURE,EQ,INE168P01015
Endurance Technologies Ltd.,Automobile and Auto Components,ENDURANCE,EQ,INE913H01037
Engineers India Ltd.,Construction,ENGINERSIN,EQ,INE510A01028
Eris Lifesciences Ltd.,Healthcare,ERIS,EQ,INE406M01024
Escorts Kubota Ltd.,Capital Goods,ESCORTS,EQ,INE042A01014
Eternal Ltd.,Consumer Services,ETERNAL,EQ,INE758T01015
Exide Industries Ltd.,Automobile and Auto Components,EXIDEIND,EQ,INE302A01020
FSN E-Commerce Ventures Ltd.,Consumer Services,NYKAA,EQ,INE388Y01029
Federal Bank Ltd.,Financial Services,FEDERALBNK,EQ,INE171A01029
Fertilisers and Chemicals Travancore Ltd.,Chemicals,FACT,EQ,INE188A01015
Finolex Cables Ltd.,Capital Goods,FINCABLES,EQ,INE235A01022
Finolex Industries Ltd.,Capital Goods,FINPIPE,EQ,INE183A01024
Firstsource Solutions Ltd.,Services,FSL,EQ,INE684F01012
Five-Star Business Finance Ltd.,Financial Services,FIVESTAR,EQ,INE128S01021
Fortis Healthcare Ltd.,Healthcare,FORTIS,EQ,INE061F01013
GAIL (India) Ltd.,Oil Gas & Consumable Fuels,GAIL,EQ,INE129A01019
GE Vernova T&D India Ltd.,Capital Goods,GVT&D,EQ,INE200A01026
GMR Airports Ltd.,Services,GMRAIRPORT,EQ,INE776C01039
Garden Reach Shipbuilders & Engineers Ltd.,Capital Goods,GRSE,EQ,INE382Z01011
General Insurance Corporation of India,Financial Services,GICRE,EQ,INE481Y01014
Gillette India Ltd.,Fast Moving Consumer Goods,GILLETTE,EQ,INE322A01010
Gland Pharma Ltd.,Healthcare,GLAND,EQ,INE068V01023
Glaxosmithkline Pharmaceuticals Ltd.,Healthcare,GLAXO,EQ,INE159A01016
Glenmark Pharmaceuticals Ltd.,Healthcare,GLENMARK,EQ,INE935A01035
Global Health Ltd.,Healthcare,MEDANTA,EQ,INE474Q01031
Go Digit General Insurance Ltd.,Financial Services,GODIGIT,EQ,INE03JT01014
Godawari Power & Ispat Ltd.,Capital Goods,GPIL,EQ,INE177H01039
Godfrey Phillips India Ltd.,Fast Moving Consumer Goods,GODFRYPHLP,EQ,INE260B01028
Godrej Agrovet Ltd.,Fast Moving Consumer Goods,GODREJAGRO,EQ,INE850D01014
Godrej Consumer Products Ltd.,Fast Moving Consumer Goods,GODREJCP,EQ,INE102D01028
Godrej Industries Ltd.,Diversified,GODREJIND,EQ,INE233A01035
Godrej Properties Ltd.,Realty,GODREJPROP,EQ,INE484J01027
Granules India Ltd.,Healthcare,GRANULES,EQ,INE101D01020
Graphite India Ltd.,Capital Goods,GRAPHITE,EQ,INE371A01025
Grasim Industries Ltd.,Construction Materials,GRASIM,EQ,INE047A01021
Gravita India Ltd.,Metals & Mining,GRAVITA,EQ,INE024L01027
Great Eastern Shipping Co. Ltd.,Services,GESHIP,EQ,INE017A01032
Gujarat Fluorochemicals Ltd.,Chemicals,FLUOROCHEM,EQ,INE09N301011
Gujarat Gas Ltd.,Oil Gas & Consumable Fuels,GUJGASLTD,EQ,INE844O01030
Gujarat Mineral Development Corporation Ltd.,Metals & Mining,GMDCLTD,EQ,INE131A01031
Gujarat Narmada Valley Fertilizers and Chemicals Ltd.,Chemicals,GNFC,EQ,INE113A01013
Gujarat Pipavav Port Ltd.,Services,GPPL,EQ,INE517F01014
Gujarat State Petronet Ltd.,Oil Gas & Consumable Fuels,GSPL,EQ,INE246F01010
H.E.G. Ltd.,Capital Goods,HEG,EQ,INE545A01024
HBL Engineering Ltd.,Capital Goods,HBLENGINE,EQ,INE292B01021
HCL Technologies Ltd.,Information Technology,HCLTECH,EQ,INE860A01027
HDFC Asset Management Company Ltd.,Financial Services,HDFCAMC,EQ,INE127D01025
HDFC Bank Ltd.,Financial Services,HDFCBANK,EQ,INE040A01034
HDFC Life Insurance Company Ltd.,Financial Services,HDFCLIFE,EQ,INE795G01014
HFCL Ltd.,Telecommunication,HFCL,EQ,INE548A01028
Happiest Minds Technologies Ltd.,Information Technology,HAPPSTMNDS,EQ,INE419U01012
Havells India Ltd.,Consumer Durables,HAVELLS,EQ,INE176B01034
Hero MotoCorp Ltd.,Automobile and Auto Components,HEROMOTOCO,EQ,INE158A01026
Himadri Speciality Chemical Ltd.,Chemicals,HSCL,EQ,INE019C01026
Hindalco Industries Ltd.,Metals & Mining,HINDALCO,EQ,INE038A01020
Hindustan Aeronautics Ltd.,Capital Goods,HAL,EQ,INE066F01020
Hindustan Copper Ltd.,Metals & Mining,HINDCOPPER,EQ,INE531E01026
Hindustan Petroleum Corporation Ltd.,Oil Gas & Consumable Fuels,HINDPETRO,EQ,INE094A01015
Hindustan Unilever Ltd.,Fast Moving Consumer Goods,HINDUNILVR,EQ,INE030A01027
Hindustan Zinc Ltd.,Metals & Mining,HINDZINC,EQ,INE267A01025
Hitachi Energy India Ltd.,Capital Goods,POWERINDIA,EQ,INE07Y701011
Home First Finance Company India Ltd.,Financial Services,HOMEFIRST,EQ,INE481N01025
Honasa Consumer Ltd.,Fast Moving Consumer Goods,HONASA,EQ,INE0J5401028
Honeywell Automation India Ltd.,Capital Goods,HONAUT,EQ,INE671A01010
Housing & Urban Development Corporation Ltd.,Financial Services,HUDCO,EQ,INE031A01017
Hyundai Motor India Ltd.,Automobile and Auto Components,HYUNDAI,EQ,INE0V6F01027
ICICI Bank Ltd.,Financial Services,ICICIBANK,EQ,INE090A01021
ICICI Lombard General Insurance Company Ltd.,Financial Services,ICICIGI,EQ,INE765G01017
ICICI Prudential Life Insurance Company Ltd.,Financial services,ICICIPRULI,EQ,INE726G01019
IDBI Bank Ltd.,Financial Services,IDBI,EQ,INE008A01015
IDFC First Bank Ltd.,Financial Services,IDFCFIRSTB,EQ,INE092T01019
IFCI Ltd.,Financial Services,IFCI,EQ,INE039A01010
IIFL Finance Ltd.,Financial Services,IIFL,EQ,INE530B01024
INOX India Ltd.,Capital Goods,INOXINDIA,EQ,INE616N01034
IRB Infrastructure Developers Ltd.,Construction,IRB,EQ,INE821I01022
IRCON International Ltd.,Construction,IRCON,EQ,INE962Y01021
ITC Ltd.,Fast Moving Consumer Goods,ITC,EQ,INE154A01025
ITI Ltd.,Telecommunication,ITI,EQ,INE248A01017
Indegene Ltd.,Healthcare,INDGN,EQ,INE065X01017
India Cements Ltd.,Construction Materials,INDIACEM,EQ,INE383A01012
Indiamart Intermesh Ltd.,Consumer Services,INDIAMART,EQ,INE933S01016
Indian Bank,Financial Services,INDIANB,EQ,INE562A01011
Indian Energy Exchange Ltd.,Financial Services,IEX,EQ,INE022Q01020
Indian Hotels Co. Ltd.,Consumer Services,INDHOTEL,EQ,INE053A01029
Indian Oil Corporation Ltd.,Oil Gas & Consumable Fuels,IOC,EQ,INE242A01010
Indian Overseas Bank,Financial Services,IOB,EQ,INE565A01014
Indian Railway Catering And Tourism Corporation Ltd.,Consumer Services,IRCTC,EQ,INE335Y01020
Indian Railway Finance Corporation Ltd.,Financial Services,IRFC,EQ,INE053F01010
Indian Renewable Energy Development Agency Ltd.,Financial Services,IREDA,EQ,INE202E01016
Indraprastha Gas Ltd.,Oil Gas & Consumable Fuels,IGL,EQ,INE203G01027
Indus Towers Ltd.,Telecommunication,INDUSTOWER,EQ,INE121J01017
IndusInd Bank Ltd.,Financial Services,INDUSINDBK,EQ,INE095A01012
Info Edge (India) Ltd.,Consumer Services,NAUKRI,EQ,INE663F01032
Infosys Ltd.,Information Technology,INFY,EQ,INE009A01021
Inox Wind Ltd.,Capital Goods,INOXWIND,EQ,INE066P01011
Intellect Design Arena Ltd.,Information Technology,INTELLECT,EQ,INE306R01017
InterGlobe Aviation Ltd.,Services,INDIGO,EQ,INE646L01027
International Gemmological Institute (India) Ltd.,Services,IGIL,EQ,INE0Q9301021
Inventurus Knowledge Solutions Ltd.,Information Technology,IKS,EQ,INE115Q01022
Ipca Laboratories Ltd.,Healthcare,IPCALAB,EQ,INE571A01038
J.B. Chemicals & Pharmaceuticals Ltd.,Healthcare,JBCHEPHARM,EQ,INE572A01036
J.K. Cement Ltd.,Construction Materials,JKCEMENT,EQ,INE823G01014
JBM Auto Ltd.,Automobile and Auto Components,JBMA,EQ,INE927D01051
JK Tyre & Industries Ltd.,Automobile and Auto Components,JKTYRE,EQ,INE573A01042
JM Financial Ltd.,Financial Services,JMFINANCIL,EQ,INE780C01023
JSW Energy Ltd.,Power,JSWENERGY,EQ,INE121E01018
JSW Holdings Ltd.,Financial Services,JSWHL,BE,INE824G01012
JSW Infrastructure Ltd.,Services,JSWINFRA,EQ,INE880J01026
JSW Steel Ltd.,Metals & Mining,JSWSTEEL,EQ,INE019A01038
Jaiprakash Power Ventures Ltd.,Power,JPPOWER,EQ,INE351F01018
Jammu & Kashmir Bank Ltd.,Financial Services,J&KBANK,EQ,INE168A01041
Jindal Saw Ltd.,Capital Goods,JINDALSAW,EQ,INE324A01032
Jindal Stainless Ltd.,Metals & Mining,JSL,EQ,INE220G01021
Jindal Steel & Power Ltd.,Metals & Mining,JINDALSTEL,EQ,INE749A01030
Jio Financial Services Ltd.,Financial Services,JIOFIN,EQ,INE758E01017
Jubilant Foodworks Ltd.,Consumer Services,JUBLFOOD,EQ,INE797F01020
Jubilant Ingrevia Ltd.,Chemicals,JUBLINGREA,EQ,INE0BY001018
Jubilant Pharmova Ltd.,Healthcare,JUBLPHARMA,EQ,INE700A01033
Jupiter Wagons Ltd.,Capital Goods,JWL,EQ,INE209L01016
Justdial Ltd.,Consumer Services,JUSTDIAL,EQ,INE599M01018
Jyothy Labs Ltd.,Fast Moving Consumer Goods,JYOTHYLAB,EQ,INE668F01031
Jyoti CNC Automation Ltd.,Capital Goods,JYOTICNC,EQ,INE980O01024
K.P.R. Mill Ltd.,Textiles,KPRMILL,EQ,INE930H01031
KEI Industries Ltd.,Capital Goods,KEI,EQ,INE878B01027
KNR Constructions Ltd.,Construction,KNRCON,EQ,INE634I01029
KPIT Technologies Ltd.,Information Technology,KPITTECH,EQ,INE04I401011
Kajaria Ceramics Ltd.,Consumer Durables,KAJARIACER,EQ,INE217B01036
Kalpataru Projects International Ltd.,Construction,KPIL,EQ,INE220B01022
Kalyan Jewellers India Ltd.,Consumer Durables,KALYANKJIL,EQ,INE303R01014
Kansai Nerolac Paints Ltd.,Consumer Durables,KANSAINER,EQ,INE531A01024
Karur Vysya Bank Ltd.,Financial Services,KARURVYSYA,EQ,INE036D01028
Kaynes Technology India Ltd.,Capital Goods,KAYNES,EQ,INE918Z01012
Kec International Ltd.,Construction,KEC,EQ,INE389H01022
Kfin Technologies Ltd.,Financial Services,KFINTECH,EQ,INE138Y01010
Kirloskar Brothers Ltd.,Capital Goods,KIRLOSBROS,EQ,INE732A01036
Kirloskar Oil Eng Ltd.,Capital Goods,KIRLOSENG,EQ,INE146L01010
Kotak Mahindra Bank Ltd.,Financial Services,KOTAKBANK,EQ,INE237A01028
Krishna Institute of Medical Sciences Ltd.,Healthcare,KIMS,EQ,INE967H01025
L&T Finance Ltd.,Financial Services,LTF,EQ,INE498L01015
L&T Technology Services Ltd.,Information Technology,LTTS,EQ,INE010V01017
LIC Housing Finance Ltd.,Financial Services,LICHSGFIN,EQ,INE115A01026
LT Foods Ltd.,Fast Moving Consumer Goods,LTFOODS,EQ,INE818H01020
LTIMindtree Ltd.,Information Technology,LTIM,EQ,INE214T01019
Larsen & Toubro Ltd.,Construction,LT,EQ,INE018A01030
Latent View Analytics Ltd.,Information Technology,LATENTVIEW,EQ,INE0I7C01011
Laurus Labs Ltd.,Healthcare,LAURUSLABS,EQ,INE947Q01028
Lemon Tree Hotels Ltd.,Consumer Services,LEMONTREE,EQ,INE970X01018
Life Insurance Corporation of India,Financial Services,LICI,EQ,INE0J1Y01017
Linde India Ltd.,Chemicals,LINDEINDIA,EQ,INE473A01011
Lloyds Metals And Energy Ltd.,Metals & Mining,LLOYDSME,EQ,INE281B01032
Lodha Developers Ltd.,Realty,LODHA,EQ,INE670K01029
Lupin Ltd.,Healthcare,LUPIN,EQ,INE326A01037
MMTC Ltd.,Services,MMTC,EQ,INE123F01029
MRF Ltd.,Automobile and Auto Components,MRF,EQ,INE883A01011
Mahanagar Gas Ltd.,Oil Gas & Consumable Fuels,MGL,EQ,INE002S01010
Maharashtra Seamless Ltd.,Capital Goods,MAHSEAMLES,EQ,INE271B01025
Mahindra & Mahindra Financial Services Ltd.,Financial Services,M&MFIN,EQ,INE774D01024
Mahindra & Mahindra Ltd.,Automobile and Auto Components,M&M,EQ,INE101A01026
Manappuram Finance Ltd.,Financial Services,MANAPPURAM,EQ,INE522D01027
Mangalore Refinery & Petrochemicals Ltd.,Oil Gas & Consumable Fuels,MRPL,EQ,INE103A01014
Mankind Pharma Ltd.,Healthcare,MANKIND,EQ,INE634S01028
Marico Ltd.,Fast Moving Consumer Goods,MARICO,EQ,INE196A01026
Maruti Suzuki India Ltd.,Automobile and Auto Components,MARUTI,EQ,INE585B01010
Mastek Ltd.,Information Technology,MASTEK,EQ,INE759A01021
Max Financial Services Ltd.,Financial Services,MFSL,EQ,INE180A01020
Max Healthcare Institute Ltd.,Healthcare,MAXHEALTH,EQ,INE027H01010
Mazagoan Dock Shipbuilders Ltd.,Capital Goods,MAZDOCK,EQ,INE249Z01020
Metropolis Healthcare Ltd.,Healthcare,METROPOLIS,EQ,INE112L01020
Minda Corporation Ltd.,Automobile and Auto Components,MINDACORP,EQ,INE842C01021
Motherson Sumi Wiring India Ltd.,Automobile and Auto Components,MSUMI,EQ,INE0FS801015
Motilal Oswal Financial Services Ltd.,Financial Services,MOTILALOFS,EQ,INE338I01027
MphasiS Ltd.,Information Technology,MPHASIS,EQ,INE356A01018
Multi Commodity Exchange of India Ltd.,Financial Services,MCX,EQ,INE745G01035
Muthoot Finance Ltd.,Financial Services,MUTHOOTFIN,EQ,INE414G01012
NATCO Pharma Ltd.,Healthcare,NATCOPHARM,EQ,INE987B01026
NBCC (India) Ltd.,Construction,NBCC,EQ,INE095N01031
NCC Ltd.,Construction,NCC,EQ,INE868B01028
NHPC Ltd.,Power,NHPC,EQ,INE848E01016
NLC India Ltd.,Power,NLCINDIA,EQ,INE589A01014
NMDC Ltd.,Metals & Mining,NMDC,EQ,INE584A01023
NMDC Steel Ltd.,Metals & Mining,NSLNISP,EQ,INE0NNS01018
NTPC Green Energy Ltd.,Power,NTPCGREEN,EQ,INE0ONG01011
NTPC Ltd.,Power,NTPC,EQ,INE733E01010
Narayana Hrudayalaya Ltd.,Healthcare,NH,EQ,INE410P01011
National Aluminium Co. Ltd.,Metals & Mining,NATIONALUM,EQ,INE139A01034
Nava Ltd.,Power,NAVA,EQ,INE725A01030
Navin Fluorine International Ltd.,Chemicals,NAVINFLUOR,EQ,INE048G01026
Nestle India Ltd.,Fast Moving Consumer Goods,NESTLEIND,EQ,INE239A01024
Netweb Technologies India Ltd.,Information Technology,NETWEB,EQ,INE0NT901020
Network18 Media & Investments Ltd.,Media Entertainment & Publication,NETWORK18,EQ,INE870H01013
Neuland Laboratories Ltd.,Healthcare,NEULANDLAB,EQ,INE794A01010
Newgen Software Technologies Ltd.,Information Technology,NEWGEN,EQ,INE619B01017
Nippon Life India Asset Management Ltd.,Financial Services,NAM-INDIA,EQ,INE298J01013
Niva Bupa Health Insurance Company Ltd.,Financial Services,NIVABUPA,EQ,INE995S01015
Nuvama Wealth Management Ltd.,Financial Services,NUVAMA,EQ,INE531F01015
Oberoi Realty Ltd.,Realty,OBEROIRLTY,EQ,INE093I01010
Oil & Natural Gas Corporation Ltd.,Oil Gas & Consumable Fuels,ONGC,EQ,INE213A01029
Oil India Ltd.,Oil Gas & Consumable Fuels,OIL,EQ,INE274J01014
Ola Electric Mobility Ltd.,Automobile and Auto Components,OLAELEC,EQ,INE0LXG01040
Olectra Greentech Ltd.,Automobile and Auto Components,OLECTRA,EQ,INE260D01016
One 97 Communications Ltd.,Financial Services,PAYTM,EQ,INE982J01020
Oracle Financial Services Software Ltd.,Information Technology,OFSS,EQ,INE881D01027
PB Fintech Ltd.,Financial Services,POLICYBZR,EQ,INE417T01026
PCBL Chemical Ltd.,Chemicals,PCBL,EQ,INE602A01031
PG Electroplast Ltd.,Consumer Durables,PGEL,EQ,INE457L01029
PI Industries Ltd.,Chemicals,PIIND,EQ,INE603J01030
PNB Housing Finance Ltd.,Financial Services,PNBHOUSING,EQ,INE572E01012
PNC Infratech Ltd.,Construction,PNCINFRA,EQ,INE195J01029
PTC Industries Ltd.,Capital Goods,PTCIL,EQ,INE596F01018
PVR INOX Ltd.,Media Entertainment & Publication,PVRINOX,EQ,INE191H01014
Page Industries Ltd.,Textiles,PAGEIND,EQ,INE761H01022
Patanjali Foods Ltd.,Fast Moving Consumer Goods,PATANJALI,EQ,INE619A01035
Persistent Systems Ltd.,Information Technology,PERSISTENT,EQ,INE262H01021
Petronet LNG Ltd.,Oil Gas & Consumable Fuels,PETRONET,EQ,INE347G01014
Pfizer Ltd.,Healthcare,PFIZER,EQ,INE182A01018
Phoenix Mills Ltd.,Realty,PHOENIXLTD,EQ,INE211B01039
Pidilite Industries Ltd.,Chemicals,PIDILITIND,EQ,INE318A01026
Piramal Enterprises Ltd.,Financial Services,PEL,EQ,INE140A01024
Piramal Pharma Ltd.,Healthcare,PPLPHARMA,EQ,INE0DK501011
Poly Medicure Ltd.,Healthcare,POLYMED,EQ,INE205C01021
Polycab India Ltd.,Capital Goods,POLYCAB,EQ,INE455K01017
Poonawalla Fincorp Ltd.,Financial Services,POONAWALLA,EQ,INE511C01022
Power Finance Corporation Ltd.,Financial Services,PFC,EQ,INE134E01011
Power Grid Corporation of India Ltd.,Power,POWERGRID,EQ,INE752E01010
Praj Industries Ltd.,Capital Goods,PRAJIND,EQ,INE074A01025
Premier Energies Ltd.,Capital Goods,PREMIERENE,EQ,INE0BS701011
Prestige Estates Projects Ltd.,Realty,PRESTIGE,EQ,INE811K01011
Punjab National Bank,Financial Services,PNB,EQ,INE160A01022
R R Kabel Ltd.,Capital Goods,RRKABEL,EQ,INE777K01022
RBL Bank Ltd.,Financial Services,RBLBANK,EQ,INE976G01028
REC Ltd.,Financial Services,RECLTD,EQ,INE020B01018
RHI MAGNESITA INDIA LTD.,Capital Goods,RHIM,EQ,INE743M01012
RITES Ltd.,Construction,RITES,EQ,INE320J01015
Radico Khaitan Ltd,Fast Moving Consumer Goods,RADICO,EQ,INE944F01028
Rail Vikas Nigam Ltd.,Construction,RVNL,EQ,INE415G01027
Railtel Corporation Of India Ltd.,Telecommunication,RAILTEL,EQ,INE0DD101019
Rainbow Childrens Medicare Ltd.,Healthcare,RAINBOW,EQ,INE961O01016
Ramkrishna Forgings Ltd.,Automobile and Auto Components,RKFORGE,EQ,INE399G01023
Rashtriya Chemicals & Fertilizers Ltd.,Chemicals,RCF,EQ,INE027A01015
RattanIndia Enterprises Ltd.,Consumer Services,RTNINDIA,EQ,INE834M01019
Raymond Lifestyle Ltd.,Textiles,RAYMONDLSL,EQ,INE02ID01020
Raymond Ltd.,Realty,RAYMOND,EQ,INE301A01014
Redington Ltd.,Services,REDINGTON,EQ,INE891D01026
Reliance Industries Ltd.,Oil Gas & Consumable Fuels,RELIANCE,EQ,INE002A01018
Reliance Power Ltd.,Power,RPOWER,BE,INE614G01033
Route Mobile Ltd.,Telecommunication,ROUTE,EQ,INE450U01017
SBFC Finance Ltd.,Financial Services,SBFC,EQ,INE423Y01016
SBI Cards and Payment Services Ltd.,Financial Services,SBICARD,EQ,INE018E01016
SBI Life Insurance Company Ltd.,Financial Services,SBILIFE,EQ,INE123W01016
SJVN Ltd.,Power,SJVN,EQ,INE002L01015
SKF India Ltd.,Capital Goods,SKFINDIA,EQ,INE640A01023
SRF Ltd.,Chemicals,SRF,EQ,INE647A01010
Sagility India Ltd.,Information Technology,SAGILITY,EQ,INE0W2G01015
Sai Life Sciences Ltd.,Healthcare,SAILIFE,EQ,INE570L01029
Sammaan Capital Ltd.,Financial Services,SAMMAANCAP,EQ,INE148I01020
Samvardhana Motherson International Ltd.,Automobile and Auto Components,MOTHERSON,EQ,INE775A01035
Sapphire Foods India Ltd.,Consumer Services,SAPPHIRE,EQ,INE806T01020
Sarda Energy and Minerals Ltd.,Metals & Mining,SARDAEN,EQ,INE385C01021
Saregama India Ltd,Media Entertainment & Publication,SAREGAMA,EQ,INE979A01025
Schaeffler India Ltd.,Automobile and Auto Components,SCHAEFFLER,EQ,INE513A01022
Schneider Electric Infrastructure Ltd.,Capital Goods,SCHNEIDER,BE,INE839M01018
Shipping Corporation of India Ltd.,Services,SCI,EQ,INE109A01011
Shree Cement Ltd.,Construction Materials,SHREECEM,EQ,INE070A01015
Shree Renuka Sugars Ltd.,Fast Moving Consumer Goods,RENUKA,EQ,INE087H01022
Shriram Finance Ltd.,Financial Services,SHRIRAMFIN,EQ,INE721A01047
Shyam Metalics and Energy Ltd.,Capital Goods,SHYAMMETL,EQ,INE810G01011
Siemens Ltd.,Capital Goods,SIEMENS,EQ,INE003A01024
Signatureglobal (India) Ltd.,Realty,SIGNATURE,EQ,INE903U01023
Sobha Ltd.,Realty,SOBHA,EQ,INE671H01015
Solar Industries India Ltd.,Chemicals,SOLARINDS,EQ,INE343H01029
Sona BLW Precision Forgings Ltd.,Automobile and Auto Components,SONACOMS,EQ,INE073K01018
Sonata Software Ltd.,Information Technology,SONATSOFTW,EQ,INE269A01021
Star Health and Allied Insurance Company Ltd.,Financial Services,STARHEALTH,EQ,INE575P01011
State Bank of India,Financial Services,SBIN,EQ,INE062A01020
Steel Authority of India Ltd.,Metals & Mining,SAIL,EQ,INE114A01011
Sterling and Wilson Renewable Energy Ltd.,Construction,SWSOLAR,EQ,INE00M201021
Sumitomo Chemical India Ltd.,Chemicals,SUMICHEM,EQ,INE258G01013
Sun Pharmaceutical Industries Ltd.,Healthcare,SUNPHARMA,EQ,INE044A01036
Sun TV Network Ltd.,Media Entertainment & Publication,SUNTV,EQ,INE424H01027
Sundaram Finance Ltd.,Financial Services,SUNDARMFIN,EQ,INE660A01013
Sundram Fasteners Ltd.,Automobile and Auto Components,SUNDRMFAST,EQ,INE387A01021
Supreme Industries Ltd.,Capital Goods,SUPREMEIND,EQ,INE195A01028
Suzlon Energy Ltd.,Capital Goods,SUZLON,EQ,INE040H01021
Swan Energy Ltd.,Chemicals,SWANENERGY,EQ,INE665A01038
Swiggy Ltd.,Consumer Services,SWIGGY,EQ,INE00H001014
Syngene International Ltd.,Healthcare,SYNGENE,EQ,INE398R01022
Syrma SGS Technology Ltd.,Capital Goods,SYRMA,EQ,INE0DYJ01015
TBO Tek Ltd.,Consumer Services,TBOTEK,EQ,INE673O01025
TVS Motor Company Ltd.,Automobile and Auto Components,TVSMOTOR,EQ,INE494B01023
Tanla Platforms Ltd.,Information Technology,TANLA,EQ,INE483C01032
Tata Chemicals Ltd.,Chemicals,TATACHEM,EQ,INE092A01019
Tata Communications Ltd.,Telecommunication,TATACOMM,EQ,INE151A01013
Tata Consultancy Services Ltd.,Information Technology,TCS,EQ,INE467B01029
Tata Consumer Products Ltd.,Fast Moving Consumer Goods,TATACONSUM,EQ,INE192A01025
Tata Elxsi Ltd.,Information Technology,TATAELXSI,EQ,INE670A01012
Tata Investment Corporation Ltd.,Financial Services,TATAINVEST,EQ,INE672A01018
Tata Motors Ltd.,Automobile and Auto Components,TATAMOTORS,EQ,INE155A01022
Tata Power Co. Ltd.,Power,TATAPOWER,EQ,INE245A01021
Tata Steel Ltd.,Metals & Mining,TATASTEEL,EQ,INE081A01020
Tata Technologies Ltd.,Information Technology,TATATECH,EQ,INE142M01025
Tata Teleservices (Maharashtra) Ltd.,Telecommunication,TTML,BE,INE517B01013
Tech Mahindra Ltd.,Information Technology,TECHM,EQ,INE669C01036
Techno Electric & Engineering Company Ltd.,Construction,TECHNOE,EQ,INE285K01026
Tejas Networks Ltd.,Telecommunication,TEJASNET,EQ,INE010J01012
The New India Assurance Company Ltd.,Financial Services,NIACL,EQ,INE470Y01017
The Ramco Cements Ltd.,Construction Materials,RAMCOCEM,EQ,INE331A01037
Thermax Ltd.,Capital Goods,THERMAX,EQ,INE152A01029
Timken India Ltd.,Capital Goods,TIMKEN,EQ,INE325A01013
Titagarh Rail Systems Ltd.,Capital Goods,TITAGARH,EQ,INE615H01020
Titan Company Ltd.,Consumer Durables,TITAN,EQ,INE280A01028
Torrent Pharmaceuticals Ltd.,Healthcare,TORNTPHARM,EQ,INE685A01028
Torrent Power Ltd.,Power,TORNTPOWER,EQ,INE813H01021
Transformers And Rectifiers (India) Ltd.,Capital Goods,TARIL,EQ,INE763I01026
Trent Ltd.,Consumer Services,TRENT,EQ,INE849A01020
Trident Ltd.,Textiles,TRIDENT,EQ,INE064C01022
Triveni Engineering & Industries Ltd.,Fast Moving Consumer Goods,TRIVENI,EQ,INE256C01024
Triveni Turbine Ltd.,Capital Goods,TRITURBINE,EQ,INE152M01016
Tube Investments of India Ltd.,Automobile and Auto Components,TIINDIA,EQ,INE974X01010
UCO Bank,Financial Services,UCOBANK,EQ,INE691A01018
UNO Minda Ltd.,Automobile and Auto Components,UNOMINDA,EQ,INE405E01023
UPL Ltd.,Chemicals,UPL,EQ,INE628A01036
UTI Asset Management Company Ltd.,Financial Services,UTIAMC,EQ,INE094J01016
UltraTech Cement Ltd.,Construction Materials,ULTRACEMCO,EQ,INE481G01011
Union Bank of India,Financial Services,UNIONBANK,EQ,INE692A01016
United Breweries Ltd.,Fast Moving Consumer Goods,UBL,EQ,INE686F01025
United Spirits Ltd.,Fast Moving Consumer Goods,UNITDSPR,EQ,INE854D01024
Usha Martin Ltd.,Capital Goods,USHAMART,EQ,INE228A01035
V-Guard Industries Ltd.,Consumer Durables,VGUARD,EQ,INE951I01027
Valor Estate Ltd.,Consumer Services,DBREALTY,BE,INE879I01012
Vardhman Textiles Ltd.,Textiles,VTL,EQ,INE825A01020
Varun Beverages Ltd.,Fast Moving Consumer Goods,VBL,EQ,INE200M01039
Vedant Fashions Ltd.,Consumer Services,MANYAVAR,EQ,INE825V01034
Vedanta Ltd.,Metals & Mining,VEDL,EQ,INE205A01025
Vijaya Diagnostic Centre Ltd.,Healthcare,VIJAYA,EQ,INE043W01024
Vishal Mega Mart Ltd.,Consumer Services,VMM,EQ,INE01EA01019
Vodafone Idea Ltd.,Telecommunication,IDEA,EQ,INE669E01016
Voltas Ltd.,Consumer Durables,VOLTAS,EQ,INE226A01021
Waaree Energies Ltd.,Capital Goods,WAAREEENER,EQ,INE377N01017
Welspun Corp Ltd.,Capital Goods,WELCORP,EQ,INE191B01025
Welspun Living Ltd.,Textiles,WELSPUNLIV,EQ,INE192B01031
Westlife Foodworld Ltd.,Consumer Services,WESTLIFE,EQ,INE274F01020
Whirlpool of India Ltd.,Consumer Durables,WHIRLPOOL,EQ,INE716A01013
Wipro Ltd.,Information Technology,WIPRO,EQ,INE075A01022
Wockhardt Ltd.,Healthcare,WOCKPHARMA,EQ,INE049B01025
Yes Bank Ltd.,Financial Services,YESBANK,EQ,INE528G01035
ZF Commercial Vehicle Control Systems India Ltd.,Automobile and Auto Components,ZFCVINDIA,EQ,INE342J01019
Zee Entertainment Enterprises Ltd.,Media Entertainment & Publication,ZEEL,EQ,INE256A01028
Zen Technologies Ltd.,Capital Goods,ZENTEC,EQ,INE251B01027
Zensar Technolgies Ltd.,Information Technology,ZENSARTECH,EQ,INE520A01027
Zydus Lifesciences Ltd.,Healthcare,ZYDUSLIFE,EQ,INE010B01027
eClerx Services Ltd.,Services,ECLERX,EQ,INE738I01010
"""
    with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as f:
        f.write(csv_content)

# --- [NEW] Load stock data ---
try:
    stock_df = pd.read_csv(CSV_FILE_PATH)
    stock_df.dropna(subset=['Symbol'], inplace=True)
except FileNotFoundError:
    print(f"Error: The file '{CSV_FILE_PATH}' was not found. Please ensure it is in the same directory.")
    exit()

# --- [NEW] Initialize WebDriver with options to run headless ---
chrome_options = Options()
# To hide the browser window, uncomment the following line
# chrome_options.add_argument("--headless") 
chrome_options.add_argument("--log-level=3") # Suppress console logs
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.tradingview.com/symbols/BTCUSD/?exchange=CRYPTO")
driver.maximize_window()
time.sleep(3)

# Data for live plotting
profits = []
share_prices = []
timestamps = []
percentage_changes = []
moving_averages = []
initial_price = None # Used to calculate profit for stocks

# --- [THEME CHANGE] - BLOOMBERG TERMINAL / DARK MODE THEME ---
plot_bgcolor = '#121212'
axes_color = '#181818'
line_color_profit = '#00A2FF'
text_color_primary = '#E0E0E0'
text_color_secondary = '#888888'
grid_color = '#333333'
accent_color_green = '#44D400'
accent_color_red = '#FF3B30'
accent_color_neutral = '#AAAAAA'
fill_color_positive = '#00803c' # Darker green for fill
fill_color_negative = '#a02820' # Darker red for fill
sma_color = '#FFC400'

# Apply the new theme using rcParams
plt.rcParams['axes.facecolor'] = axes_color
plt.rcParams['figure.facecolor'] = plot_bgcolor
plt.rcParams['axes.edgecolor'] = grid_color
plt.rcParams['axes.labelcolor'] = text_color_secondary
plt.rcParams['xtick.color'] = text_color_secondary
plt.rcParams['ytick.color'] = text_color_secondary
plt.rcParams['grid.color'] = grid_color
plt.rcParams['text.color'] = text_color_primary
plt.rcParams['font.family'] = ['Consolas', 'Menlo', 'Courier New', 'monospace']
plt.rcParams['font.weight'] = 'normal'
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'normal'

# Initialize matplotlib figure and axis
fig, ax = plt.subplots(figsize=(14, 8), facecolor=plot_bgcolor)

# --- [MODIFIED] BLOOMBERG-STYLE BRANDING WITH BOX ---
brand_fontsize = 24
brand_fontname = 'sans-serif'
brand_weight = 'heavy'
text_zorder = 10
patch_zorder = 9

brand_box = FancyBboxPatch((0.01, 0.925), width=0.215, height=0.065,
                           boxstyle="round,pad=0.01,rounding_size=0.01",
                           facecolor=axes_color, edgecolor=grid_color,
                           transform=fig.transFigure, clip_on=False, zorder=patch_zorder)
fig.patches.append(brand_box)

fig.text(0.018, 0.98, 'AnsCom', transform=fig.transFigure, fontsize=brand_fontsize,
         weight=brand_weight, color=text_color_primary, ha='left', va='top',
         fontname=brand_fontname, zorder=text_zorder)

fig.text(0.122, 0.98, 'Terminal', transform=fig.transFigure, fontsize=brand_fontsize,
         weight=brand_weight, color=sma_color, ha='left', va='top',
         fontname=brand_fontname, zorder=text_zorder)

# Chart Elements
line, = ax.plot([], [], label="Profit (₹)", color=line_color_profit, linewidth=2.0, linestyle='-')
ax.set_title(f"AT:(INTRADAY) {current_ticker} LIVE TRACKING and Profit Analysis for {SHARES} coin(s)", fontsize=18, color=text_color_primary, weight='bold', pad=45, fontname='Consolas')
ax.set_xlabel("Time", fontsize=14, color=text_color_secondary, labelpad=10)
ax.set_ylabel("Profit (₹)", fontsize=14, color=text_color_secondary, labelpad=10)

legend = ax.legend(fontsize=12, loc='upper left', facecolor=axes_color, edgecolor=grid_color, labelcolor=text_color_primary, framealpha=1.0)
for text in legend.get_texts(): text.set_fontweight('bold')

ax.grid(True, axis='y', linestyle='--', color=grid_color, alpha=0.7, linewidth=0.8)
ax.grid(True, axis='x', linestyle=':', color=grid_color, alpha=0.5, linewidth=0.5)
ax.tick_params(axis='both', which='major', direction='out', length=6, width=1, colors=text_color_secondary, pad=8)
for spine in ax.spines.values(): spine.set_color(grid_color)
ax.axhline(0, color=sma_color, linestyle='--', linewidth=1.2, alpha=0.8)

# Info Panel Text Boxes
bbox_props = dict(boxstyle='round,pad=0.4', facecolor=axes_color, edgecolor=grid_color, alpha=1.0)
text_x_position, text_y_position = 1.01, 0.99
live_profit_text = ax.text(text_x_position, text_y_position, '', transform=ax.transAxes, fontsize=13, verticalalignment='top', horizontalalignment='left', color=accent_color_green, weight='bold', bbox=bbox_props)
live_price_text = ax.text(text_x_position, text_y_position - 0.08, '', transform=ax.transAxes, fontsize=13, verticalalignment='top', horizontalalignment='left', color=text_color_primary, weight='bold', bbox=bbox_props)
live_change_text = ax.text(text_x_position, text_y_position - 0.16, '', transform=ax.transAxes, fontsize=11, verticalalignment='top', horizontalalignment='left', color=text_color_secondary, weight='bold', bbox=bbox_props)
live_pct_change_text = ax.text(text_x_position, text_y_position - 0.24, '', transform=ax.transAxes, fontsize=11, verticalalignment='top', horizontalalignment='left', color=line_color_profit, weight='bold', bbox=bbox_props)
live_sma_text = ax.text(text_x_position, text_y_position - 0.32, '', transform=ax.transAxes, fontsize=11, verticalalignment='top', horizontalalignment='left', color=sma_color, weight='bold', bbox=bbox_props)
price_change_by_day_text = ax.text(text_x_position, text_y_position - 0.40, '', transform=ax.transAxes, fontsize=11, verticalalignment='top', horizontalalignment='left', color=text_color_primary, weight='bold', bbox=bbox_props)
total_amount_text = ax.text(text_x_position, text_y_position - 0.48, '', transform=ax.transAxes, fontsize=13, verticalalignment='top', horizontalalignment='left', color=text_color_primary, weight='bold', bbox=bbox_props)
market_status_text = ax.text(text_x_position, 0.20, '', transform=ax.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left', weight='bold', bbox=bbox_props)
live_indicator_text = ax.text(text_x_position, 0.13, '● Live', transform=ax.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left', color=accent_color_red, weight='bold', bbox=bbox_props)
live_time_text = ax.text(text_x_position, 0.06, '', transform=ax.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left', color=text_color_primary, weight='bold', bbox=bbox_props)

prev_price = None
watermark_text = ax.text(0.99, 0.01, 'AnswerCom Terminal', transform=ax.transAxes, fontsize=11, weight='bold', verticalalignment='bottom', horizontalalignment='right', color=text_color_secondary, alpha=0.7)
fill_positive, fill_negative = None, None

# --- [NEW] Global vars for command widgets
command_box_widget = None
suggestion_ax = None
suggestion_buttons_widget = None

# --- [NEW] Command processing and data reset logic ---
def reset_plot_data():
    """Clears all historical data for a new stock."""
    global profits, share_prices, timestamps, percentage_changes, moving_averages, prev_price, initial_price
    profits.clear()
    share_prices.clear()
    timestamps.clear()
    percentage_changes.clear()
    moving_averages.clear()
    prev_price = None
    initial_price = None
    if fill_positive:
        try: fill_positive.remove()
        except: pass
    if fill_negative:
        try: fill_negative.remove()
        except: pass
    line.set_data([], [])
    ax.set_ylim(0, 1) # Reset y-limits
    ax.set_xlim(0, 1) # Reset x-limits
    
    # Also reset the info panel text
    live_profit_text.set_text('')
    live_price_text.set_text('')
    live_change_text.set_text('')
    live_pct_change_text.set_text('')
    live_sma_text.set_text('')
    price_change_by_day_text.set_text('')
    total_amount_text.set_text('')
    
    fig.canvas.draw_idle()

def process_command(command_text):
    """Parses command, navigates browser, and resets the plot for a new stock."""
    global SHARES, current_ticker
    
    # Regex to find Ticker and Shares from the command
    match = re.search(r"MARKET\s+INDIA\s+NSE\s+([A-Z0-9-&]+)\s+STOCKS:(\d+)", command_text.upper())
    
    if match:
        ticker, shares_str = match.groups()
        new_shares = int(shares_str)

        print(f"Processing command: Ticker={ticker}, Shares={new_shares}")
        
        SHARES = new_shares
        current_ticker = ticker
        
        # Reset all data
        reset_plot_data()

        # Update title and labels
        unit = "share(s)" if current_ticker != "BTC_USD" else "coin(s)"
        unit_symbol = "₹" if current_ticker != "BTC_USD" else "$"
        ax.set_title(f"AT:(INTRADAY) {current_ticker} LIVE TRACKING and Profit Analysis for {SHARES} {unit}", fontsize=18, color=text_color_primary, weight='bold', pad=45, fontname='Consolas')
        ax.set_ylabel(f"Profit ({unit_symbol})", fontsize=14, color=text_color_secondary, labelpad=10)
        legend.get_texts()[0].set_text(f"Profit ({unit_symbol})")


        # Navigate to the new TradingView URL
        url = f"https://www.tradingview.com/symbols/NSE-{ticker}/"
        print(f"Navigating to: {url}")
        driver.get(url)
        # We don't need to sleep here, the update loop's WebDriverWait will handle it
        
        # Clear command box and hide suggestions
        command_box_widget.set_val("")
        if suggestion_ax: suggestion_ax.set_visible(False)
        fig.canvas.draw_idle()
    else:
        print(f"Invalid command format: {command_text}")

# --- Callbacks for command widgets ---
def on_command_submit(text):
    process_command(text)

def on_suggestion_clicked(label):
    global command_box_widget
    ticker = label.split(' - ')[0]
    new_command = f"MARKET INDIA NSE {ticker} STOCKS:50"
    command_box_widget.set_val(new_command)
    suggestion_ax.set_visible(False)
    fig.canvas.draw_idle()

def on_command_text_changed(text):
    global suggestion_ax, suggestion_buttons_widget
    
    search_prefix = "MARKET INDIA NSE "
    if text.upper().startswith(search_prefix):
        search_term = text[len(search_prefix):].upper()
        if search_term:
            matches = stock_df[stock_df['Symbol'].str.startswith(search_term)][:7]
            if not matches.empty:
                labels = [f"{row['Symbol']} - {row['Company Name']}" for _, row in matches.iterrows()]
                if suggestion_buttons_widget:
                    suggestion_buttons_widget.disconnect_events()
                suggestion_ax.clear()
                suggestion_ax.set_facecolor(axes_color)
                suggestion_buttons_widget = RadioButtons(
                    suggestion_ax, labels, activecolor=sma_color,
                    label_props={'color': [text_color_primary], 'fontsize': [10]},
                    radio_props={'edgecolor': [grid_color]*len(labels), 'facecolor': [axes_color]*len(labels), 's': [40]*len(labels)}
                )
                suggestion_buttons_widget.on_clicked(on_suggestion_clicked)
                suggestion_ax.set_visible(True)
            else:
                suggestion_ax.set_visible(False)
        else:
            suggestion_ax.set_visible(False)
    else:
        if suggestion_ax: suggestion_ax.set_visible(False)
    fig.canvas.draw_idle()

# --- Setup Command and Suggestion Widgets ---
command_ax = fig.add_axes([0.25, 0.93, 0.5, 0.045])
command_box_widget = TextBox(
    command_ax, '', initial='MARKET INDIA NSE ',
    color=axes_color, hovercolor=grid_color, label_pad=0.01
)
command_box_widget.label.set_color(text_color_secondary)
for spine in command_box_widget.ax.spines.values():
    spine.set_edgecolor(grid_color)
command_box_widget.on_submit(on_command_submit)
command_box_widget.on_text_change(on_command_text_changed)

suggestion_ax = fig.add_axes([0.25, 0.67, 0.5, 0.25], visible=False)
suggestion_ax.set_facecolor(axes_color)
for spine in suggestion_ax.spines.values(): spine.set_visible(False)
suggestion_ax.tick_params(bottom=False, labelbottom=False, left=False, labelleft=False)

# --- Drawing and Analysis Tools ---
class DrawingManager:
    # ... (No changes needed in this class, keeping it as is)
    def __init__(self, ax, fig, data_providers):
        self.ax = ax; self.fig = fig; self.get_share_prices, self.get_timestamps = data_providers
        self.active_tool = 'None'; self.start_point = None; self.temp_artist = None
        self.drawn_artists = []; self.is_drawing = False
    def set_tool(self, label):
        self.active_tool = label.replace(' ', '_'); self.start_point = None
        if self.temp_artist: self.temp_artist.remove(); self.temp_artist = None
        self.fig.canvas.draw_idle()
    def on_press(self, event):
        if event.inaxes != self.ax or self.active_tool == 'None' or command_box_widget.capturekeystrokes: return
        self.is_drawing = True; self.start_point = (event.xdata, event.ydata)
        if self.active_tool in ['Line', 'Pencil']:
            self.temp_artist = Line2D([self.start_point[0]], [self.start_point[1]], color=sma_color, linestyle='--', linewidth=1.5); self.ax.add_line(self.temp_artist)
        elif self.active_tool == 'Measure_%':
            self.temp_artist = Line2D([self.start_point[0]], [self.start_point[1]], color=accent_color_green, marker='o', markersize=5); self.ax.add_line(self.temp_artist)
        self.fig.canvas.draw_idle()
    def on_motion(self, event):
        if not self.is_drawing or not self.start_point or event.inaxes != self.ax: return
        if self.active_tool == 'Pencil':
            x, y = self.temp_artist.get_data(); self.temp_artist.set_data(np.append(x, event.xdata), np.append(y, event.ydata))
        elif self.active_tool in ['Line', 'Measure_%']:
            self.temp_artist.set_data([self.start_point[0], event.xdata], [self.start_point[1], event.ydata])
        self.fig.canvas.draw_idle()
    def on_release(self, event):
        if not self.is_drawing or not self.start_point: return
        self.is_drawing = False; end_point = (event.xdata, event.ydata)
        if self.active_tool in ['Pencil', 'Line']:
            final_line = self.temp_artist; final_line.set_linestyle('-'); self.drawn_artists.append(final_line)
        elif self.active_tool == 'Measure_%' and self.temp_artist:
            self.temp_artist.remove(); self.calculate_and_draw_measurement(self.start_point[0], end_point[0])
        self.temp_artist = None; self.start_point = None; self.fig.canvas.draw_idle()
    def calculate_and_draw_measurement(self, x_start, x_end):
        prices = self.get_share_prices(); times = self.get_timestamps(); unit_symbol = "₹" if current_ticker != "BTC_USD" else "$"
        if not prices or len(prices) < 2: return
        idx_start, idx_end = np.clip(int(round(x_start)), 0, len(prices) - 1), np.clip(int(round(x_end)), 0, len(prices) - 1)
        if idx_start == idx_end: return
        if idx_start > idx_end: idx_start, idx_end = idx_end, idx_start
        price_start, price_end = prices[idx_start], prices[idx_end]
        time_start, time_end = datetime.strptime(times[idx_start], "%H:%M:%S"), datetime.strptime(times[idx_end], "%H:%M:%S")
        if time_end < time_start: time_end += timedelta(days=1)
        time_delta, price_delta = time_end - time_start, price_end - price_start
        pct_change = (price_delta / price_start) * 100 if price_start != 0 else 0
        color = accent_color_green if price_delta >= 0 else accent_color_red
        profit_start = (price_start - prices[0]) * SHARES if initial_price is not None else (price_start - prices[0]) * SHARES
        profit_end = (price_end - prices[0]) * SHARES if initial_price is not None else (price_end - prices[0]) * SHARES
        line = Line2D([idx_start, idx_end], [profit_start, profit_end], color=color, linestyle=':', marker='o', markersize=4, linewidth=2)
        text_content = (f"Δ Price: {unit_symbol}{price_delta:,.2f}\nΔ Return: {pct_change:.2f}%\nΔ Time: {str(time_delta)}")
        text_y_pos, text_x_pos = (profit_start + profit_end) / 2, (idx_start + idx_end) / 2
        annotation = self.ax.text(text_x_pos, text_y_pos, text_content, color=text_color_primary, ha='center', va='center', fontsize=10, weight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor=plot_bgcolor, edgecolor=color, alpha=0.9))
        self.ax.add_line(line); self.drawn_artists.extend([line, annotation])
    def clear_drawings(self, event):
        for artist in self.drawn_artists: artist.remove()
        self.drawn_artists.clear(); self.fig.canvas.draw_idle()


def is_market_open(): return True

def update(frame):
    global prev_price, fill_positive, fill_negative, initial_price
    try:
        # --- [FIX 2] Use WebDriverWait for reliable element finding ---
        wait = WebDriverWait(driver, 10) # Wait up to 10 seconds

        price_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-field="last"]')))
        change_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[data-field="change"]')))
        pct_change_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[data-field="change-percent"]')))
        
        live_price_str = price_elem.text
        day_change_str = change_elem.text
        pct_change_str = pct_change_elem.text.strip('()')
        
        live_price = float(live_price_str.replace(",", ""))
        day_price_change = float(day_change_str.replace("+", "").replace("−", "-").replace(",", ""))
        percentage_change = float(pct_change_str.replace("%", "").replace("+", "").replace("−", "-"))

        # Profit Calculation
        if current_ticker == "BTC_USD":
            profit = SHARES * day_price_change
        else:
            if initial_price is None:
                initial_price = live_price
            profit = (live_price - initial_price) * SHARES
        
        total_amount = SHARES * live_price
        profits.append(profit); share_prices.append(live_price)
        current_dt = datetime.now()
        timestamps.append(current_dt.strftime("%H:%M:%S"))
        percentage_changes.append(percentage_change)

        if len(share_prices) >= 5: moving_averages.append(np.mean(share_prices[-5:]))
        elif share_prices: moving_averages.append(np.mean(share_prices))
        else: moving_averages.append(np.nan)

        x_data = np.arange(len(profits))
        line.set_data(x_data, profits)

        min_profit, max_profit = (min(profits) if profits else 0), (max(profits) if profits else 0)
        padding = (max_profit - min_profit) * 0.2 + 1
        ax.set_ylim(min_profit - padding, max_profit + padding)
        ax.set_xlim(0, max(len(profits) - 1, 1))

        max_ticks = 15; step = max(1, len(timestamps) // max_ticks)
        ax.set_xticks(x_data[::step]); ax.set_xticklabels(timestamps[::step], rotation=45, ha='right', fontsize=10)

        if fill_positive: fill_positive.remove()
        if fill_negative: fill_negative.remove()
        if len(profits) > 1:
            profits_array = np.array(profits)
            fill_positive = ax.fill_between(x_data, profits_array, 0, where=profits_array >= 0, facecolor=fill_color_positive, alpha=0.3, interpolate=True)
            fill_negative = ax.fill_between(x_data, profits_array, 0, where=profits_array < 0, facecolor=fill_color_negative, alpha=0.3, interpolate=True)
        
        unit_symbol = "₹" if current_ticker != "BTC_USD" else "$"
        live_profit_text.set_text(f"Profit: {unit_symbol}{profit:,.2f}")
        live_price_text.set_text(f"Price: {unit_symbol}{live_price:,.2f}")
        live_change_text.set_text(f"Day Change: {day_change_str}")
        live_pct_change_text.set_text(f"Change %: {pct_change_str}")
        if not np.isnan(moving_averages[-1]): live_sma_text.set_text(f"SMA (5): {unit_symbol}{moving_averages[-1]:,.2f}")
        else: live_sma_text.set_text("SMA (5): N/A")
        price_change_by_day_text.set_text(f"Day Price Change: {day_price_change:,.2f}")
        total_amount_text.set_text(f"Total Value: {unit_symbol}{total_amount:,.2f}")
        market_status_text.set_text("Market Status: Open"); market_status_text.set_color(accent_color_green)
        live_indicator_text.set_color(accent_color_green); live_time_text.set_text(f"Time: {current_dt.strftime('%H:%M:%S')}")

        if prev_price is not None:
            if live_price > prev_price: price_color = accent_color_green
            elif live_price < prev_price: price_color = accent_color_red
            else: price_color = accent_color_neutral
        else: price_color = accent_color_neutral
        
        live_price_text.set_color(price_color)
        live_profit_text.set_color(accent_color_green if profit >= 0 else accent_color_red)
        prev_price = live_price

    except Exception as e:
        live_indicator_text.set_color(accent_color_red)
        # --- [FIX 3] Uncomment the print statement for debugging ---
        print(f"Error during update: {e}")

    return (line, fill_positive, fill_negative, live_profit_text, live_price_text,
            live_change_text, live_pct_change_text, live_sma_text, price_change_by_day_text,
            total_amount_text, market_status_text, live_indicator_text, live_time_text)

# Setup Drawing Manager and UI Widgets
data_providers = (lambda: share_prices, lambda: timestamps)
drawing_manager = DrawingManager(ax, fig, data_providers)
fig.canvas.mpl_connect('button_press_event', drawing_manager.on_press)
fig.canvas.mpl_connect('motion_notify_event', drawing_manager.on_motion)
fig.canvas.mpl_connect('button_release_event', drawing_manager.on_release)

tool_ax = fig.add_axes([0.015, 0.01, 0.2, 0.15], frameon=False)
tool_buttons = RadioButtons(
    tool_ax, ('None', 'Pencil', 'Line', 'Measure %'),
    activecolor=sma_color,
    label_props={'color': [text_color_primary], 'fontsize': [10]},
    radio_props={'edgecolor': [grid_color]*4, 's': [40]*4, 'facecolor': [axes_color]*4}
)
tool_buttons.on_clicked(drawing_manager.set_tool)

clear_ax = fig.add_axes([0.18, 0.02, 0.07, 0.04])
clear_button = Button(clear_ax, 'Clear All', color=axes_color, hovercolor=grid_color)
clear_button.label.set_color(text_color_primary); clear_button.label.set_fontweight('bold')
clear_button.on_clicked(drawing_manager.clear_drawings)

# Start live graph animation
ani = FuncAnimation(fig, update, interval=1000, blit=False)

try:
    plt.tight_layout(rect=[0, 0.05, 0.85, 0.90], pad=2.5)
    plt.show()
except (KeyboardInterrupt, SystemExit):
    print("Program stopped by the user.")
finally:
    driver.quit()
    print("WebDriver closed.")