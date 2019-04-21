import r
def update_qry_without_fk(i, update_value):
    cursor.execute('''UPDATE ''' + set_row_value.table_name + ''' SET ''' + set_row_value.table_fields +
                   ''' = ? where id=?''', (update_value, i))


def update_qry_with_fk(plan_id):
    cursor.execute('''UPDATE ''' + set_row_value.table_dependent_tbl_name + ''' SET '''
                   + set_row_value.table_dependent_tbl_fields +
                   ''' = ? where ''' + set_row_value.table_dependent_tbl_fields + '''=?''', (plan_id, 61))
    cursor.execute(
        '''UPDATE ''' + set_row_value.table_name + ''' SET ''' + set_row_value.table_fields +
        ''' = ? where ''' + set_row_value.table_dependent_tbl_fields + '''=?''', (plan_id, 61))