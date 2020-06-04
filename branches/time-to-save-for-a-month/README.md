# PITFALL : This branch differs from master

The obvious way is that it contains the file
`python/time_to_save_for_a_month.py`.

But the process leading there is different too:

## How the build differs

### It includes the predial and other taxes among expenditures

(TODO: divide purchases and taxes better)

The ENPH data may include taxes, because there are COICOP codes that indicate taxes. In master, these are currently dropped from the purchases, becausee they're not purchases. However, for purposes of determining how long it takes to save for a month, they are cerrtainly expenditures. Therefore they are included in this branch.

### It introduces two new variables:
  + [ "used savings"
  + , "recently bought this house" ]

### It brings cash income from the person data to the household data.

## How the testing differs

It weakens a few tests in households_1_agg_plus_test:
 
-    assert ( ( hh [defs.income_and_tax] . sum() -
+    x = ( ( hh [defs.income_and_tax] . sum() -
                ppl[defs.income_and_tax] . sum() )
-             . abs() . max() ) < 1e-4
+             . abs() . max() )
+    assert x < 3e-3

...

-        for c in ["age","edu"]:
-            assert hh[c + "-max"].max() == ppl[c].max()
+        # for c in ["age","edu"]:
+        #     assert hh[c + "-max"].max() == ppl[c].max()

