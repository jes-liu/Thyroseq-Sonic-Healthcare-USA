SELECT
C.number,
REPLACE(convert(NVARCHAR,C.date, 106),' ','-') as Collection_date,
P.lastName + ',' + P.firstName as person
,S.is_____
,S.desc
,SP.id
,CASE
    WHEN SP.id = 1 THEN 'I'
    WHEN SP.id = 2 THEN 'II'
    WHEN SP.id = 3 THEN 'III'
    WHEN SP.id = 4 THEN 'IV'
    WHEN SP.id = 5 THEN 'V'
    WHEN SP.id = 6 THEN 'VI'
END as category
,SP.diag
,a.acc
from cases as C
LEFT JOIN table1 as PL on C.id1=PL.id2
LEFT JOIN table2 as P on  P.id3=PL.id4
LEFT JOIN table3 S on S.id5 = C.id6
LEFT JOIN table4 SP on S.id7 = SP.id8
LEFT JOIN table5 as R on C.id9 = R.id1
LEFT JOIN table6 a on pl.id2 = a.id3
where C.accessionNumber like '%a%'
and C.dateReported between DateAdd(mm,DateDiff(mm,0,GetDate())-1,0) and DateAdd(mm,DateDiff(mm,0,GetDate()),0)
order by C.date;
