=================
OpenFoodFacts Viz
=================

A dataset scrapped from `Open Food Facts`_.


Files
-----

- **off**/                                   sources optained from `Open Food Facts`_
    - **data-fields.txt**                    documentation of the fields for the product database
    - **categories.txt**                     product taxonomy
    - **en.openfoodfacts.org.products.csv**  products (not versionned, available from `OFF database`_)
- **tsv**/                                   cleaned data sets ready for use with d3.js_
    - **categories.tsv**                     list of all non empty categories
    - **categories_taxonomy.tsv**            parent/children relation between categories
    - **products.tsv**                       all 167300 products
    - **products_additives.tsv**             product/additive relations
    - **products_categories_full.tsv**       product/category relations (all categories, including parents, listed for all products)
    - **products_categories_min.tsv**        product/category relations (only most specific categories)
    - **products_countries.tsv**             product/country relations
    - **products_labels.tsv**                product/label relations
- **viz**/
    - **cookies.html**   sample visualisation of elements from the cookies category generated using d3.js_
- **vendor**/ vendorized libraries
    - **d3**


The tsv folder also includes restrictions of the while products.tsv dataset to specific categories:

===================================== ==========
file                                  # products
===================================== ==========
products_only_cookies.tsv                    697
products_only_mueslis.tsv                   1056
products_only_breakfast-cereals.tsv         2711
products_only_breads.tsv                    3872
products_only_fruits-based-foods.tsv        8741
products.tsv                              179448
===================================== ==========

.. _Open Food Facts: https://world.openfoodfacts.org
.. _d3.js: http://d3js.org


Licences
--------

Files in the off/ directory come from the `Open Food Facts`_ project and are licenced under the `Open Database License`_.

Files in the tsv/ directory are extractions of the `OFF database`_, and as such are made available here under the `Open Database License`_.

.. _Open Database License: https://opendatacommons.org/licenses/odbl/1.0/
.. _OFF database: https://world.openfoodfacts.org/data
