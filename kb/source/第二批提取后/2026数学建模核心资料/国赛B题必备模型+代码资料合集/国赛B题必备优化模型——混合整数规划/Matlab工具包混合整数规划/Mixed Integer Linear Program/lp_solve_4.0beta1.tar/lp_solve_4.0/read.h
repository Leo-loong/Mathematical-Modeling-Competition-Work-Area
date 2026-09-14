/* prototypes of functions used in the parser */

int init_read(void);
int add_constraint_name(char *name, int row);
void store_re_op(void);
void null_tmp_store(void);
int store_bounds(void);
void add_int_var(char *name);
void rhs_store(REAL value);
int var_store(char *var, int row, REAL value);
