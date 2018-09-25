SELECT 
	SB2010.B2_FILIAL AS 'FILIAL', 
	SB2010.B2_LOCAL AS 'ARMAZÉM',
	RTRIM(SB2010.B2_COD) AS 'COD PRODUTO', 
	RTRIM(SB1010.B1_DESC) AS 'DESCRIÇÃO', 
	SB2010.B2_QATU AS 'QTD SYS',
	SB1010.B1_UPRC AS 'VALOR UND'
FROM PROTHEUS.dbo.SB2010 SB2010
	LEFT JOIN PROTHEUS.dbo.SB1010 SB1010 ON SB2010.B2_COD=SB1010.B1_COD AND SB1010.D_E_L_E_T_ <> '*'
WHERE 
	(SB2010.D_E_L_E_T_<>'*') AND
	(SB2010.B2_FILIAL={filial}) AND
	(SB2010.B2_LOCAL={armazem})