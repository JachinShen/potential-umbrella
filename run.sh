echo "Caching expresssions:"
python 1_cache_expression_q0.py
echo "Selecting cached expresssions:"
python 2_select_cached.py
echo "Filter half permutations:"
python 3_filter_selected.py
echo "Recombine permutations:"
python 4_split.py