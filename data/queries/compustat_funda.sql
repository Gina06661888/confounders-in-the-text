SELECT
    comp_na_daily_all.funda.costat,
    comp_na_daily_all.funda.curcd,
    comp_na_daily_all.funda.datafmt,
    comp_na_daily_all.funda.indfmt,
    comp_na_daily_all.funda.consol,
    comp_na_daily_all.funda.gvkey,
    comp_na_daily_all.funda.datadate,
    comp_na_daily_all.funda.conm,
    comp_na_daily_all.funda.cik,
    comp_na_daily_all.funda.fyr,
    comp_na_daily_all.funda.apdedate,
    comp_na_daily_all.funda.curncd,
    comp_na_daily_all.funda.fyear,
    comp_na_daily_all.funda.at,
    comp_na_daily_all.funda.che,
    comp_na_daily_all.funda.dlc,
    comp_na_daily_all.funda.dltt,
    comp_na_daily_all.funda.lt,
    comp_na_daily_all.funda.seq,
    comp_na_daily_all.funda.ib,
    comp_na_daily_all.funda.ni,
    comp_na_daily_all.funda.oiadp,
    comp_na_daily_all.funda.pi,
    comp_na_daily_all.funda.sale,
    comp_na_daily_all.funda.txt,
    comp_na_daily_all.funda.xrd,
    comp_na_daily_all.funda.capx,
    comp_na_daily_all.funda.sich

FROM comp_na_daily_all.funda
LEFT JOIN (
    SELECT
        gvkey
    FROM comp_na_daily_all.company
) AS id_table 

ON comp_na_daily_all.funda.gvkey = id_table.gvkey

WHERE comp_na_daily_all.funda.datadate BETWEEN
    '2008-01-01'::date AND '2026-10-31'::date

AND ("comp_na_daily_all"."funda"."consol" = ANY (ARRAY['C']) AND "comp_na_daily_all"."funda"."indfmt" = ANY (ARRAY['INDL','FS']) AND "comp_na_daily_all"."funda"."datafmt" = ANY (ARRAY['STD']) AND "comp_na_daily_all"."funda"."curcd" = ANY (ARRAY['USD','CAD']) AND "comp_na_daily_all"."funda"."costat" = ANY (ARRAY['A','I']))
