WITH CONCEPT_CDS_FOR_Q AS (
    -- 8
    SELECT CONCEPT_CD
    FROM CONCEPT_DIMENSION
    WHERE STARTSWITH(CONCEPT_CD, 'ICD10:N04')

    -- 1, 2, 3, 6, 7
    UNION
    SELECT CONCEPT_CD
    FROM CONCEPT_DIMENSION
    WHERE CONCEPT_CD IN ('CPT4:84156', 'CPT4:82570')

    -- 10, 11, 12, 13, 14, 15
    UNION
    SELECT CONCEPT_CD
    FROM CONCEPT_DIMENSION
    WHERE CONCEPT_CD IN ('ICD9:582.1', 'ICD9 583.1', 'ICD10 N02.0', 'ICD10 N05.2', 'ICD10:N05.2', 'ICD10:N03.3')

    -- 9
    UNION
    SELECT CONCEPT_CD
    FROM CONCEPT_DIMENSION
    WHERE STARTSWITH(CONCEPT_CD, 'ICD9:581')

    -- Labs from Simran's notes
    UNION
    SELECT CONCEPT_CD
    FROM CONCEPT_DIMENSION
    WHERE CONCEPT_CD IN ('LAB:3775197', 'LAB:3775497', 'LAB:3774493', 'LAB:3775584')
),
MATCHING_PATIENTS AS (
    SELECT distinct(REPLACE(PAT_DIM.PATIENT_NUM, '.00000', '')) AS PATIENT_NUMS
    FROM 
        PROTOCOL_PATIENT_DIMENSION_SV AS PAT_DIM
    WHERE
        BIRTH_DATE > '1990-01-01'
        AND BIRTH_DATE < CURRENT_DATE()
        AND NOT STARTSWITH(PAT_DIM.PATIENT_NUM, '-')
        AND PROTOCOL = 'P00000159'
        
),
MATCHING_PATIENTS_WITH_CODES AS (
    SELECT DISTINCT(PROTOCOL_OBSERVATION_FACT_SV.PATIENT_NUM) AS PATIENT_NUM
    FROM
        PROTOCOL_OBSERVATION_FACT_SV
        INNER JOIN CONCEPT_CDS_FOR_Q ON CONCEPT_CDS_FOR_Q.CONCEPT_CD = REPLACE(PROTOCOL_OBSERVATION_FACT_SV.CONCEPT_CD, 'LAB:-', 'LAB:')
        INNER JOIN MATCHING_PATIENTS ON MATCHING_PATIENTS.PATIENT_NUMS = PROTOCOL_OBSERVATION_FACT_SV.PATIENT_NUM
    LIMIT 1
    OFFSET %s
)

SELECT
    PROTOCOL_OBSERVATION_FACT_SV.PATIENT_NUM AS PATIENT_NUM,
    CONCEPT_DIMENSION.CONCEPT_PATH AS CONCEPT_PATH,
    PROTOCOL_OBSERVATION_FACT_SV.CONCEPT_CD AS CONCEPT_CD,
    PROTOCOL_OBSERVATION_FACT_SV.NVAL_NUM AS NVAL_NUM,
    PROTOCOL_OBSERVATION_FACT_SV.TVAL_CHAR AS TVAL_CHAR,
    PROTOCOL_OBSERVATION_FACT_SV.START_DATE AS TIMESTAMP
FROM PROTOCOL_OBSERVATION_FACT_SV
    INNER JOIN CONCEPT_DIMENSION ON PROTOCOL_OBSERVATION_FACT_SV.CONCEPT_CD = CONCEPT_DIMENSION.CONCEPT_CD
    INNER JOIN MATCHING_PATIENTS_WITH_CODES ON MATCHING_PATIENTS_WITH_CODES.PATIENT_NUM = PROTOCOL_OBSERVATION_FACT_SV.PATIENT_NUM
WHERE
    PROTOCOL_OBSERVATION_FACT_SV.START_DATE > '1920-01-01'
