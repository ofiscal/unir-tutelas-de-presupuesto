import pdb
import re
from os import path


def agencies_at_each_quantile_of_each_numeric_var (
    together : pd.DataFrame, # all agencies we can read
) -> pd.DataFrame:

  cop_cols : List[str] = (
    list (
      defs.column_name_regexes . keys() )
    [2:] )
  quantiles = [0,0.25,0.5,0.75,1]
  res = pd.DataFrame (
    [],
    columns = [ x
                for cn in cop_cols
                for x in [cn, cn + " file"] ],
    index = quantiles )

  for cn in (
      list ( defs.column_name_regexes . keys() )
      [2:] ): # The first two aren't floats.
    for q in quantiles: # a quantile
      qcop = together[cn] . quantile (q) # a COP value
      res.loc [ q, cn ] = qcop
      # pdb.set_trace()
      nearest_below_index = (
        # There might be no value for which together[cn]
        # is exactly equal to qcop,
        # so instead I find the maximum of values below it.
        together [ together[cn] <= qcop ]
        [cn] . idxmax () )
      res.loc [ q, cn + " file" ] = (
        together [ together.index == nearest_below_index ]
        ["agency"]
        . iloc[0] )

  res . transpose() . to_excel (
    "agencies_at_each_quantile_of_each_numerical_var.xlsx" )

  return res
