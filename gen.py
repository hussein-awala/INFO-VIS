#! /usr/bin/env python3

# imports ###################################################################

from collections import defaultdict
from pprint import pprint


# categories ################################################################

#.write("%s\n" % '\t'.join([]))

#LANGS = ["en", "fr"]
LANGS = ["en"]

PARENTS   = defaultdict(set)
CHILDRENS = defaultdict(set)
CATEGORIES = set()

lang, parents, childrens = None, [], []

offc = open('off/categories.txt')
for line in offc:
	line = line.strip()
	if line.startswith("#"):
		continue
	if line.startswith("synonyms:"):
		continue # for now
	if line.startswith("stopwords:"):
		continue # for now
	if line.startswith("wikidata:"):
		continue # for now
	if line.startswith("wikidata_category:"):
		continue # for now
	if line.startswith("wikipediacategory:"):
		continue # for now
	if line.startswith("instanceof:"):
		continue # for now
	if line.startswith("country:"):
		continue # for now
	if line.startswith("Country:"):
		continue # for now
	if line.startswith("pnns_group_1:"):
		continue # for now
	if line.startswith("pnns_group_2:"):
		continue # for now
	if line.startswith("region:"):
		continue # for now
	if line.startswith("grapevariety:"):
		continue # for now
	
	if line == "":
		# that's the end of a block
		for parent in parents:
			for children in childrens:
				PARENTS[children].add(parent)
				CHILDRENS[parent].add(children)
			
		lang, parents, childrens = None, [], []

	elif line.startswith('<'):
		ps = line[1:]
		lang, *_, ps = ps.split(":") # to support errors like <en:en:Cocoa and chocolate powders
		if lang not in LANGS:
			continue
		p, *_ = (p.strip().lower().replace(' ', '-') for p in ps.split(','))
		parents += [p]

	else:
		try:
			lang, cs = line.split(":")
		except:
			# ignoring two malformed lines #3617 and #30055
			continue
		if lang not in LANGS:
			continue
		c, *_ = (c.strip().lower().replace(' ', '-') for c in cs.split(','))
		childrens += [c]
		CATEGORIES.add(c)

ROOTS = set(CHILDRENS) - set(PARENTS)


# category tables

with open('tsv/categories.tsv', 'w') as categories:
	categories.write("%s\n" % '\t'.join(["category"]))
	for category in CATEGORIES:
		categories.write("%s\n" % category)

categories = list(CATEGORIES-ROOTS)
parents = list(ROOTS)
	
with open('tsv/categories_taxonomy.tsv', 'w') as taxonomy:
	taxonomy.write("%s\n" % ('\t'.join(["parent", "children"])))
	while parents:
		parent = parents.pop()
		for children in CHILDRENS[parent]:
			taxonomy.write("%s\n" % ('\t'.join([parent, children])))
			if children in categories: # else, should have already be handled
				parents.append(children)
				categories.remove(children)

ORPHEANS = set(categories)


# products ##################################################################

counts = defaultdict(int)

offp = open('off/en.openfoodfacts.org.products.csv')
for line in offp:
	COLUMNS = line.strip().split('\t')
	break

assert COLUMNS == ['code', 'url', 'creator', 'created_t', 'created_datetime', 'last_modified_t', 'last_modified_datetime', 'product_name', 'generic_name', 'quantity', 'packaging', 'packaging_tags', 'brands', 'brands_tags', 'categories', 'categories_tags', 'categories_en', 'origins', 'origins_tags', 'manufacturing_places', 'manufacturing_places_tags', 'labels', 'labels_tags', 'labels_en', 'emb_codes', 'emb_codes_tags', 'first_packaging_code_geo', 'cities', 'cities_tags', 'purchase_places', 'stores', 'countries', 'countries_tags', 'countries_en', 'ingredients_text', 'allergens', 'allergens_en', 'traces', 'traces_tags', 'traces_en', 'serving_size', 'serving_quantity', 'no_nutriments', 'additives_n', 'additives', 'additives_tags', 'additives_en', 'ingredients_from_palm_oil_n', 'ingredients_from_palm_oil', 'ingredients_from_palm_oil_tags', 'ingredients_that_may_be_from_palm_oil_n', 'ingredients_that_may_be_from_palm_oil', 'ingredients_that_may_be_from_palm_oil_tags', 'nutrition_grade_fr', 'nova_group', 'pnns_groups_1', 'pnns_groups_2', 'states', 'states_tags', 'states_en', 'main_category', 'main_category_en', 'image_url', 'image_small_url', 'image_ingredients_url', 'image_ingredients_small_url', 'image_nutrition_url', 'image_nutrition_small_url', 'energy_100g', 'energy-from-fat_100g', 'fat_100g', 'saturated-fat_100g', '-butyric-acid_100g', '-caproic-acid_100g', '-caprylic-acid_100g', '-capric-acid_100g', '-lauric-acid_100g', '-myristic-acid_100g', '-palmitic-acid_100g', '-stearic-acid_100g', '-arachidic-acid_100g', '-behenic-acid_100g', '-lignoceric-acid_100g', '-cerotic-acid_100g', '-montanic-acid_100g', '-melissic-acid_100g', 'monounsaturated-fat_100g', 'polyunsaturated-fat_100g', 'omega-3-fat_100g', '-alpha-linolenic-acid_100g', '-eicosapentaenoic-acid_100g', '-docosahexaenoic-acid_100g', 'omega-6-fat_100g', '-linoleic-acid_100g', '-arachidonic-acid_100g', '-gamma-linolenic-acid_100g', '-dihomo-gamma-linolenic-acid_100g', 'omega-9-fat_100g', '-oleic-acid_100g', '-elaidic-acid_100g', '-gondoic-acid_100g', '-mead-acid_100g', '-erucic-acid_100g', '-nervonic-acid_100g', 'trans-fat_100g', 'cholesterol_100g', 'carbohydrates_100g', 'sugars_100g', '-sucrose_100g', '-glucose_100g', '-fructose_100g', '-lactose_100g', '-maltose_100g', '-maltodextrins_100g', 'starch_100g', 'polyols_100g', 'fiber_100g', 'proteins_100g', 'casein_100g', 'serum-proteins_100g', 'nucleotides_100g', 'salt_100g', 'sodium_100g', 'alcohol_100g', 'vitamin-a_100g', 'beta-carotene_100g', 'vitamin-d_100g', 'vitamin-e_100g', 'vitamin-k_100g', 'vitamin-c_100g', 'vitamin-b1_100g', 'vitamin-b2_100g', 'vitamin-pp_100g', 'vitamin-b6_100g', 'vitamin-b9_100g', 'folates_100g', 'vitamin-b12_100g', 'biotin_100g', 'pantothenic-acid_100g', 'silica_100g', 'bicarbonate_100g', 'potassium_100g', 'chloride_100g', 'calcium_100g', 'phosphorus_100g', 'iron_100g', 'magnesium_100g', 'zinc_100g', 'copper_100g', 'manganese_100g', 'fluoride_100g', 'selenium_100g', 'chromium_100g', 'molybdenum_100g', 'iodine_100g', 'caffeine_100g', 'taurine_100g', 'ph_100g', 'fruits-vegetables-nuts_100g', 'fruits-vegetables-nuts-estimate_100g', 'collagen-meat-protein-ratio_100g', 'cocoa_100g', 'chlorophyl_100g', 'carbon-footprint_100g', 'nutrition-score-fr_100g', 'nutrition-score-uk_100g', 'glycemic-index_100g', 'water-hardness_100g', 'choline_100g', 'phylloquinone_100g', 'beta-glucan_100g', 'inositol_100g', 'carnitine_100g']
N = len(COLUMNS)
CODE, PRODUCT, CAT, NADDS, ADDS, IMAGE, GRADE, NOVA, COUNTRIES, LABELS = (COLUMNS.index(col) for col in ["code", "product_name", "categories_tags", 'additives_n', 'additives_tags', 'image_url', 'nutrition_grade_fr', 'nova_group', 'countries_tags', 'labels_tags'])
INGREDIENTS = [column for column in COLUMNS if column.endswith('_100g') and not column.startswith('-')]
INGREDIENTS_COLS = [COLUMNS.index(i) for i in INGREDIENTS]

codes = set()
additives = set()
origins = set()
labels = defaultdict(int)
grades = defaultdict(int)
novas = defaultdict(int)

p_l      = open('tsv/products_labels.tsv', 'w')
p_l.write("%s\n" % ('\t'.join(["code", "label"])))

p_o      = open('tsv/products_countries.tsv', 'w')
p_o.write("%s\n" % ('\t'.join(["code", "country"])))

p_c_m    = open('tsv/products_categories_min.tsv', 'w')
p_c_m.write("%s\n" % ('\t'.join(["code", "category"])))

p_c_f    = open('tsv/products_categories_full.tsv', 'w')
p_c_f.write("%s\n" % ('\t'.join(["code", "category"])))

p_a      = open('tsv/products_additives.tsv', 'w')
p_a.write("%s\n" % ('\t'.join(["code", "additive"])))

products = open('tsv/products.tsv', 'w')
products.write("%s\n" % '\t'.join(["code", "name", "image", "n_additives", "nutriscore", "nova", *INGREDIENTS]))

for line in offp:
	words = line.split('\t')
	
	if len(words) != N: # skip 34(x2)+1 malformed lines
		continue
		
	code = words[CODE]
	if code in codes: # skip 109 duplicated lines
		continue
	else:
		codes.add(code)	
	# 179870 remaining products

	name, image = words[PRODUCT], words[IMAGE]
	try:
		assert (name, image) != ('', '')
	except AssertionError:
		continue
	
	# categories
	cats = words[CAT]
	if not cats: # skip 517159 uncategorized products
		continue
	
	cats = cats.split(',')
	cats = [cat for cat in cats if cat and (':' in cat)]
	cats = {cat for lang, cat in (cat.split(':') for cat in cats) if lang in LANGS}
	cats &= CATEGORIES
	if len(cats) == 0: # ignore 11666 more products (with no cat in english)
		continue
	# 168180 remaining products
		
	for cat in cats:
		p_c_f.write("%s\n" % '\t'.join([code, cat]))

	not_leaves = set()
	for p in cats:
		childrens = CHILDRENS[p] 
		if not childrens:
			continue
		for c in cats:
			if c in childrens:
				not_leaves.add(p)
	leaves = cats - not_leaves
	for cat in leaves:
		counts[cat] += 1
	
	for cat in leaves:
		p_c_m.write("%s\n" % '\t'.join([code, cat]))

	
	# additives
	try:
		n_additives = int(words[NADDS])
	except ValueError:
		n_additives = 0
	
	adds = [a for a in words[ADDS].split(',') if a]
	adds = {a for _, a in (add.split(':') for add in adds)}
	for additive in adds:
		p_a.write("%s\n" % '\t'.join([code, additive]))
	additives |= adds
	
	countries = [c for c in words[COUNTRIES].split(',') if c and (':' in c)]
	countries = {c for lang, c in (country.split(':') for country in countries) if lang == "en"}
	for country in countries:
		p_o.write("%s\n" % '\t'.join([code, country]))
	origins |= countries

	ls = [c for c in words[LABELS].split(',') if c and (':' in c)]
	ls = {c for lang, c in (l.split(':') for l in ls) if lang == "en"}
	for label in ls:
		p_l.write("%s\n" % '\t'.join([code, label]))
		labels[label] += 1

	grade = words[GRADE]
	grades[grade] += 1
	nova = words[NOVA]
	novas[nova] += 1
	products.write("%s\n" % '\t'.join([code, name, image, str(n_additives), grade, nova, *(words[i].strip() for i in INGREDIENTS_COLS)]))

#for category in ORPHEANS:
#	print(category, counts[category])
p_c_m.close()
p_c_f.close()
p_a.close()
p_o.close()
products.close()

for k in sorted(labels, key=lambda k: labels[k]):
	print(k, labels[k])

raise SystemExit


# output ####################################################################

# trees
def display(root, level=0, indent="  "):
	print(level*indent, root, counts[root])
	for children in CHILDRENS[root]:
		display(children, level+1, indent)

#display("desserts")
#display("breakfasts")
#display("vegetables")
#display("meals")
#display("chips and fries")

def tree(root, path='', sep='/'):
	path = sep.join([path, root])
	count = counts[root]
	if count > 0:
		print(path, counts[root])
	if root not in CHILDRENS:
		return
	for children in CHILDRENS[root]:
		tree(children, path, sep)

#tree("breakfasts")

