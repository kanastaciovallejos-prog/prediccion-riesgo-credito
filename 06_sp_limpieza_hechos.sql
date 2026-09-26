CREATE OR REPLACE PROCEDURE sp_limpieza_hechos()
LANGUAGE plpgsql
AS $$
BEGIN
    -- 1. Winsorización de Outliers en LIMIT_BAL (24 casos)
    -- Acotamos los valores extremos a 750,000 según el análisis de la data
    UPDATE silver_hechos
    SET limit_bal = 750000
    WHERE limit_bal > 750000;

    -- 2. Winsorización de Outliers en PAY_AMT1 (14 casos)
    -- Acotamos los pagos inusualmente altos al tope de 250,000
    UPDATE silver_hechos
    SET pay_amt1 = 250000
    WHERE pay_amt1 > 250000;

    -- 3. Limpieza de valores negativos erróneos en historial de pagos
    -- Los pagos (PAY_AMT) no pueden ser negativos. Si hay alguno, se pasa a 0.
    UPDATE silver_hechos SET pay_amt1 = 0 WHERE pay_amt1 < 0;
    UPDATE silver_hechos SET pay_amt2 = 0 WHERE pay_amt2 < 0;
    UPDATE silver_hechos SET pay_amt3 = 0 WHERE pay_amt3 < 0;
    UPDATE silver_hechos SET pay_amt4 = 0 WHERE pay_amt4 < 0;
    UPDATE silver_hechos SET pay_amt5 = 0 WHERE pay_amt5 < 0;
    UPDATE silver_hechos SET pay_amt6 = 0 WHERE pay_amt6 < 0;

    -- 4. Estandarización de los estados de pago (PAY_0 a PAY_6)
    -- Valores no documentados como -2 (sin consumo) se agrupan a 0 (pago regular)
    UPDATE silver_hechos SET pay_0 = 0 WHERE pay_0 = -2;
    UPDATE silver_hechos SET pay_2 = 0 WHERE pay_2 = -2;
    UPDATE silver_hechos SET pay_3 = 0 WHERE pay_3 = -2;
    UPDATE silver_hechos SET pay_4 = 0 WHERE pay_4 = -2;
    UPDATE silver_hechos SET pay_5 = 0 WHERE pay_5 = -2;
    UPDATE silver_hechos SET pay_6 = 0 WHERE pay_6 = -2;

END;
$$;