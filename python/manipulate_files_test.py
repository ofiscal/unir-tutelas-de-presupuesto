import numpy as np
from   numpy import nan
import pandas as pd
import re
#
import python.manipulate_files_defs as defs


def test_series_matches_regex ():
  assert (
    defs.series_matches_regex (
      pattern = ".*x.*",
      series = pd.Series ( [ "axa",
                             "y" ] ) )
    . equals (
      pd.Series ( [ True, False ] ) ) )

def test_strip_leading_rows ():
  if True: # Test the case of good data
    good_data = pd.DataFrame (
      { 0 : ["strip", "this", "garbage",
             "denominación de cargos","moo","bark",] } )
    assert ( defs.strip_leading_rows ( good_data )
             . equals ( good_data[3:] ) )

  if True: # Test the case of bad data --
           # i.e. that Exception-raising works.
    try:
      defs.strip_leading_rows (
        pd.DataFrame ( { 0 : ["no","match","here"] } ) )
    except ValueError as e:
      # PITFALL: Enums cannot be compared directly!
      # (They are all equal if they're all of the same type.)
      # Must call `value` first.
      assert e.args[0].pattern == defs.denominacion_pattern
    else:
      assert False # This would be test failure.

def test_strip_trailing_rows ():
  if True: # Test the case of good data
    good_data = pd.DataFrame (
      { 0 : [ "denominación de cargos",
              "accountant",
              "bandido",
              "pintor",
              "total meh",
              "total bleh",
              "strip",
              "this",
              "garbage", ] } )
    assert ( defs.strip_trailing_rows ( good_data )
             . equals ( good_data[:-3] ) )

  if True: # Test the case of bad data --
           # i.e. that Exception-raising works.
    try:
      defs.strip_trailing_rows (
        pd.DataFrame ( { 0 : ["no","match","here"] } ) )
    except ValueError as e:
      # PITFALL: Enums cannot be compared directly!
      # (They are all equal if they're all of the same type.)
      # Must call `value` first.
      assert e.args[0].pattern == defs.total_pattern
    else:
      assert False # This would be test failure.

def test_strip_empty_rows ():
  df = pd.DataFrame ( [ [ nan, nan ],
                        [ 3  , nan ],
                        [ 3  , 4 ] ] )
  assert ( defs.strip_empty_rows ( df )
           . equals ( df[1:] ) )

def test_assemble_header ():
  assert (
    defs.assemble_header (
      pd.DataFrame ( [
        [ # The first nan here becomes "".
          # All the others in the first three rows are filled with
          # the previous non-nan value.
          nan   , ""    , 3     , nan   , 5        ],
        [ 1     , 2     , 3     , 4     , 5        ],
        [ 1     , nan   , 3     , nan   , nan      ],
        [ # this row has no effect on the resulting names
          nan   , nan   , nan   , nan   , nan      ],
        [ # Tricky: even the nan after the 4 becomes ""
          # in this row, unlike the others.
          nan   , nan   , nan   , 4     , nan      ],
        [ "none", "of", "this", "should", "change" ], ] ) )
    . equals (
      pd.DataFrame (
        [ [ "none", "of", "this", "should", "change" ] ],
        index = [5],
        columns = [ "1:1",
                    "2:1",
                    "3:3:3",
                    "3:4:3:4",
                    "5:5:3" ] ) ) )

def test_false_rows_to_column ():
  assert (
    defs.false_rows_to_column (
      source_column_name = "source",
      patterns           = ["a","b"],
      new_column_name    = "sink",
      df = pd.DataFrame ( {
        "source" : ["1","2","a","4","b","6","7"],
        "more"   : [ 1 , 2 , 3 , 4 , 5 , 6 , 7 ],
      } ) )
    . reset_index ( drop = True )
    . equals (
      pd.DataFrame ( {
        "source" : [ "1","2","4","6","7" ],
        "more"   : [  1 , 2 , 4 , 6 , 7  ],
        "sink"   : [ nan,nan,"a","b","b" ],
      } ) ) )
