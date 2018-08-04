
            SELECT
                RTRIM(SB1010.B1_COD)+' - '+RTRIM(SB1010.B1_DESC)
            FROM PROTHEUS.dbo.SB1010 SB1010
            WHERE
                SB1010.D_E_L_E_T_<>'*' AND
                SB1010.B1_COD = '02500132'

