select  C.number,
        C.history,
        C.comments,
        C.createdOn,
        REPLACE(convert(NVARCHAR,S.date, 106),' ','-') as collection_date,
        DATENAME(MONTH,S.date) as spec_collection_date,
        S.desc,
        SUBSTRING(S.desc, PATINDEX('%[(]%',s.desc)+1,4) as LOCATION_DATE,
        CASE
            WHEN SUBSTRING(S.desc, PATINDEX('%[)]%',S.desc)-5, 5) = '' THEN NULL
            ELSE SUBSTRING(S.desc, PATINDEX('%[)]%',S.desc)-5, 5)
            END as LOCATION,
        SP.id,
        CASE
            WHEN SP.id = 1 THEN 'I'
            WHEN SP.id = 2 THEN 'II'
            WHEN SP.id = 3 THEN 'III'
            WHEN SP.id = 4 THEN 'IV'
            WHEN SP.id = 5 THEN 'V'
            WHEN SP.id = 6 THEN 'VI'
            END as category,
        SP.diag,
        SP.ca,
        SP.cb
from spec S
JOIN case as C on S.id1 = C.id2
JOIN test SP on S.id3 = SP.id4
WHERE S.date BETWEEN DateAdd(mm,DateDiff(mm,0,GetDate())-6,0) AND DateAdd(mm,DateDiff(mm,0,GetDate())-3,0)
AND S.desc like '%desc_1%'
AND C.history like '%hist_1%'
AND SP.category in (6, -- VI
                    1, -- I
                    2 -- II
                    )
ORDER BY S.dateCollected DESC