# Data sources

Three official, keyless APIs. All numbers in the report come from these three
- the LLM never invents or adjusts a figure (enforced by `prompts/reviewer.md`).

## 1. World Bank Indicators API
- Base: `https://api.worldbank.org/v2`
- Data: `GET /country/{iso3}/indicator/{code}?format=json&per_page=100`
- Metadata (for methodology check): `GET /indicator/{code}?format=json`
- Code: `sources/worldbank.py`

## 2. WHO Global Health Observatory (GHO) OData API
- Base: `https://ghoapi.azureedge.net/api`
- Data: `GET /{code}?$filter=SpatialDim eq '{iso3}' and Dim1 eq 'SEX_BTSX'&$orderby=TimeDim desc`
  (falls back to no `Dim1` filter if the indicator has no sex breakdown)
- Metadata: `GET /Indicator?$filter=IndicatorCode eq '{code}'`
- Code: `sources/who_gho.py`

## 3. UN SDG Global Database API
- Base: `https://unstats.un.org/sdgapi/v1/sdg`
- Data: `GET /Series/Data?seriesCode={code}&areaCode={geoAreaCode}&pageSize=500`
- **Important:** the commonly-referenced `Indicator/PageOfData` endpoint returns
  404 on the current API. The correct endpoint (confirmed against the API's own
  `swagger/v1/swagger.json`) is `Series/Data`, used above.
- Uzbekistan's `geoAreaCode` is `860` (see `GeoArea/List`).
- Series often have disaggregations (sex, urban/rural, age). `un_sdg.py` picks
  the combination closest to an overall total (values like `_T`, `ALLAREA`,
  `BOTHSEX`, `ALLAGE`); if no full "total" combo exists, it falls back to
  whichever combination has the most such markers, which is often the only
  breakdown a series has (e.g. maternal mortality is only reported as `FEMALE`).
- Code: `sources/un_sdg.py`

Country: all three sources are queried for **Uzbekistan** (`config.COUNTRY_ISO3
= "UZB"`, `config.COUNTRY_SDG_AREA_CODE = "860"`).

## Field -> indicator map

| Field | World Bank | WHO GHO | UN SDG |
|---|---|---|---|
| health | `SP.DYN.LE00.IN`, `SH.XPD.CHEX.GD.ZS` | `WHOSIS_000001` | `SH_STA_MORT` |
| education | `SE.ADT.LITR.ZS`, `SE.PRM.ENRR` | - | `SE_TOT_CPLR` |
| climate and energy | `EG.ELC.ACCS.ZS`, `EN.GHG.CO2.PC.CE.AR5`, `EG.FEC.RNEW.ZS` | - | `EG_ACS_ELEC` |
| water and food | `SH.H2O.BASW.ZS`, `SN.ITK.DEFC.ZS` | - | `SH_H2O_SAFE` |
| poverty and finance | `SI.POV.NAHC`, `FX.OWN.TOTL.ZS` | - | `SI_POV_DAY1` |
| internet access | `IT.NET.USER.ZS` | - | `IT_USE_ii99` |
| urban environment | `SP.URB.TOTL.IN.ZS`, `EN.POP.SLUM.UR.ZS` | - | `EN_LND_SLUM` |
| labor market | `SL.UEM.TOTL.ZS`, `SL.TLF.CACT.ZS` | - | `SL_EMP_PCAP` |

WHO GHO mainly covers `health` - it's a health-specific database, so most
other fields simply have no WHO candidate, which is fine: the scorer only
compares whichever candidates actually return data.

## Reliability scoring (`sources/scoring.py`)

Plain Python, no LLM. For every candidate that returns real, non-null data for
Uzbekistan, points are added for:

1. **Official organization** - fixed base points; all three sources are
   official international statistical agencies, so this mostly gates which
   sources are considered at all rather than differentiating between them.
2. **Recency** - `15 - (current_year - latest_data_year)`, floored at 0. More
   recent data scores higher.
3. **Country coverage** - number of non-null historical observations found for
   Uzbekistan (capped at 20 points). More years of maintained history scores
   higher.
4. **Published methodology** - +5 if the source publishes a name/definition
   for the indicator (checked via a live metadata call for World Bank/WHO, or
   via the indicator description already returned by the SDG indicator list).

The candidate with the highest total wins; `explain_winner()` renders a short
Russian-language paragraph justifying the choice, printed to the console and
included in the PDF.

## Adding a new field

1. Pick 1-3 candidate indicator codes per source that plausibly cover the
   topic. Verify each one actually returns non-null data for Uzbekistan
   (`curl` the endpoints above) before adding it - don't guess codes.
2. Add an entry to `FIELD_INDICATORS` in `sources/registry.py`, following the
   existing shape (`fetch`, `code`, `label`, optionally `description` for SDG
   entries).
3. Add the field to `config.FIELDS` (keep the list length even, so rotation
   pairs stay balanced) and give it a Russian label in
   `config.FIELD_LABELS_RU`.
4. Add a row to the table above and re-run `pytest tests/test_registry.py`.
