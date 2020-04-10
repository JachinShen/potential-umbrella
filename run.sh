echo "Caching expresssions:"
python cache_expression.py
echo "Selecting cached expresssions:"
python select_cached.py
echo "Filter half permutations:"
python filter_selected.py