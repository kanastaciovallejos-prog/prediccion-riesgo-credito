CREATE OR REPLACE PROCEDURE sp_limpieza_maestros()
LANGUAGE plpgsql
AS $$
BEGIN
    -- 1. Limpieza de códigos inválidos y nulos en SEX (25 casos)
    -- Valores válidos: 1 (Hombre), 2 (Mujer). Lo demás va a 3 (Otros)
    UPDATE silver_maestros
    SET sex = 3
    WHERE sex NOT IN (1, 2) OR sex IS NULL;

    -- 2. Limpieza de códigos inválidos y nulos en EDUCATION (60 casos)
    -- Valores válidos: 1, 2, 3. Lo demás va a 4 (Otros)
    UPDATE silver_maestros
    SET education = 4
    WHERE education NOT IN (1, 2, 3, 4) OR education IS NULL;

    -- 3. Limpieza de códigos inválidos y nulos en MARRIAGE (40 casos)
    -- Valores válidos: 1, 2. Lo demás va a 3 (Otros)
    UPDATE silver_maestros
    SET marriage = 3
    WHERE marriage NOT IN (1, 2, 3) OR marriage IS NULL;

    -- 4. Winsorización de Outliers en AGE (22 casos)
    -- Acotar edades atípicas a un tope de 75 años para no sesgar el modelo
    UPDATE silver_maestros
    SET age = 75
    WHERE age > 75;

END;
$$;