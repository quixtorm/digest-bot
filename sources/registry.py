"""
Maps each of the 8 fields to candidate indicators in each of the 3 source APIs.
See docs/SOURCES.md for how to add a new field or indicator.

Each candidate is a dict with the keys needed to call that source's fetch_indicator().
Candidates are tried in order; scoring.py compares whichever ones actually return data.
"""
from sources import worldbank, who_gho, un_sdg

FIELD_INDICATORS = {
    "health": [
        {"fetch": worldbank.fetch_indicator, "code": "SP.DYN.LE00.IN", "label": "Ожидаемая продолжительность жизни при рождении (лет)"},
        {"fetch": worldbank.fetch_indicator, "code": "SH.XPD.CHEX.GD.ZS", "label": "Расходы на здравоохранение (% ВВП)"},
        {"fetch": who_gho.fetch_indicator, "code": "WHOSIS_000001", "label": "Ожидаемая продолжительность жизни при рождении (лет)"},
        {"fetch": un_sdg.fetch_indicator, "code": "SH_STA_MORT", "label": "Материнская смертность (на 100 000 живорождений)", "description": "Maternal mortality ratio"},
    ],
    "education": [
        {"fetch": worldbank.fetch_indicator, "code": "SE.ADT.LITR.ZS", "label": "Грамотность взрослого населения (%)"},
        {"fetch": worldbank.fetch_indicator, "code": "SE.PRM.ENRR", "label": "Охват начальным образованием (%, валовой)"},
        {"fetch": un_sdg.fetch_indicator, "code": "SE_TOT_CPLR", "label": "Доля завершивших уровень образования (%)", "description": "Completion rate"},
    ],
    "climate and energy": [
        {"fetch": worldbank.fetch_indicator, "code": "EG.ELC.ACCS.ZS", "label": "Доступ к электричеству (% населения)"},
        {"fetch": worldbank.fetch_indicator, "code": "EN.GHG.CO2.PC.CE.AR5", "label": "Выбросы CO2 на душу населения (т)"},
        {"fetch": worldbank.fetch_indicator, "code": "EG.FEC.RNEW.ZS", "label": "Доля возобновляемой энергии (%)"},
        {"fetch": un_sdg.fetch_indicator, "code": "EG_ACS_ELEC", "label": "Доступ к электричеству (% населения)", "description": "Proportion of population with access to electricity"},
    ],
    "water and food": [
        {"fetch": worldbank.fetch_indicator, "code": "SH.H2O.BASW.ZS", "label": "Доступ к базовому источнику питьевой воды (%)"},
        {"fetch": worldbank.fetch_indicator, "code": "SN.ITK.DEFC.ZS", "label": "Недоедание (% населения)"},
        {"fetch": un_sdg.fetch_indicator, "code": "SH_H2O_SAFE", "label": "Безопасное водоснабжение (%)", "description": "Safely managed drinking water services"},
    ],
    "poverty and finance": [
        {"fetch": worldbank.fetch_indicator, "code": "SI.POV.NAHC", "label": "Бедность по национальной черте (%)"},
        {"fetch": worldbank.fetch_indicator, "code": "FX.OWN.TOTL.ZS", "label": "Владение банковским/платёжным счётом (%)"},
        {"fetch": un_sdg.fetch_indicator, "code": "SI_POV_DAY1", "label": "Бедность по международной черте (%)", "description": "Population below international poverty line"},
    ],
    "internet access": [
        {"fetch": worldbank.fetch_indicator, "code": "IT.NET.USER.ZS", "label": "Пользователи интернета (% населения)"},
        {"fetch": un_sdg.fetch_indicator, "code": "IT_USE_ii99", "label": "Пользователи интернета (% населения)", "description": "Proportion of individuals using the Internet"},
    ],
    "urban environment": [
        {"fetch": worldbank.fetch_indicator, "code": "SP.URB.TOTL.IN.ZS", "label": "Городское население (% от общего)"},
        {"fetch": worldbank.fetch_indicator, "code": "EN.POP.SLUM.UR.ZS", "label": "Население трущоб (% городского населения)"},
        {"fetch": un_sdg.fetch_indicator, "code": "EN_LND_SLUM", "label": "Население трущоб (% городского населения)", "description": "Proportion of urban population living in slums"},
    ],
    "labor market": [
        {"fetch": worldbank.fetch_indicator, "code": "SL.UEM.TOTL.ZS", "label": "Уровень безработицы (%)"},
        {"fetch": worldbank.fetch_indicator, "code": "SL.TLF.CACT.ZS", "label": "Участие в рабочей силе (%)"},
        {"fetch": un_sdg.fetch_indicator, "code": "SL_EMP_PCAP", "label": "Работающие за чертой бедности (%)", "description": "Employed population below poverty line"},
    ],
}
