#!/bin/bash

# Set the input file
INPUT_FILE="frontend/src/views/CreatorWellbeingView.vue"
OUTPUT_FILE="frontend/src/views/CreatorWellbeingView.clean.vue"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: Input file $INPUT_FILE not found."
  exit 1
fi

echo "Analyzing and cleaning CSS in $INPUT_FILE..."

# Create a temporary directory
TEMP_DIR=$(mktemp -d)
STYLE_FILE="$TEMP_DIR/style.css"
CLEAN_STYLE_FILE="$TEMP_DIR/clean_style.css"
VUE_PREFIX="$TEMP_DIR/vue_prefix.txt"
VUE_SUFFIX="$TEMP_DIR/vue_suffix.txt"

# Extract parts of the Vue file
sed -n '1,/<style scoped>/p' "$INPUT_FILE" > "$VUE_PREFIX"
sed -n '/<style scoped>/,/<\/style>/p' "$INPUT_FILE" > "$STYLE_FILE"
sed -n '/<\/style>/,$p' "$INPUT_FILE" > "$VUE_SUFFIX"

# Define duplicate CSS rules to clean
declare -a duplicates=(
  ".tab"
  ".tab.active"
  ".tab.active::after"
  ".action-btn"
  ".action-btn:hover"
  ".btn-icon"
  ".resource-actions"
  ".dashboard-section .tab"
  ".dashboard-section .tab span"
  ".dashboard-section .tab.active"
  ".dashboard-section .tab.active::after"
  ".filter-header"
  ".filter-header h3"
  ".filter-toggle"
  ".filter-toggle:hover"
  ".toggle-icon"
  ".event-filters"
  ".event-filters.filters-collapsed"
)

# Create a copy of the style file for cleaning
cp "$STYLE_FILE" "$CLEAN_STYLE_FILE"

# Function to extract CSS rule by selector and get the full block
extract_rule_block() {
  local file=$1
  local selector=$2
  local line_num=$3
  
  # Get the line with the selector
  local selector_line=$(sed -n "${line_num}p" "$file")
  
  # Get the start line of the CSS block (find the preceding opening brace)
  local start_line=$line_num
  while [[ $start_line -gt 1 && ! $(sed -n "${start_line}p" "$file") =~ "{" ]]; do
    ((start_line--))
  done
  
  # Find the end line (find the next closing brace)
  local end_line=$line_num
  local max_line=$(wc -l < "$file")
  while [[ $end_line -lt $max_line && ! $(sed -n "${end_line}p" "$file") =~ "}" ]]; do
    ((end_line++))
  done
  
  # Include the closing brace
  if [[ $end_line -lt $max_line && $(sed -n "${end_line}p" "$file") =~ "}" ]]; then
    echo "$start_line,$end_line"
  else
    echo "$line_num,$line_num"  # Fallback if block not found
  fi
}

# Process each duplicate rule
for rule in "${duplicates[@]}"; do
  echo "Processing rule: $rule"
  
  # Escape for grep
  search_rule=$(echo "$rule" | sed 's/[.]/\\./g' | sed 's/\[/\\[/g' | sed 's/\]/\\]/g')
  
  # Find all occurrences of the rule
  occurrences=($(grep -n "$search_rule" "$CLEAN_STYLE_FILE" | cut -d ":" -f1))
  
  # Skip if less than 2 occurrences (not a duplicate)
  if [ ${#occurrences[@]} -lt 2 ]; then
    echo "  Not a duplicate, skipping."
    continue
  fi
  
  # Keep track of which lines to remove
  declare -a lines_to_remove=()
  
  # Get the first occurrence (to keep)
  first_occurrence=${occurrences[0]}
  first_block=$(extract_rule_block "$CLEAN_STYLE_FILE" "$rule" "$first_occurrence")
  first_start=$(echo "$first_block" | cut -d "," -f1)
  first_end=$(echo "$first_block" | cut -d "," -f2)
  
  echo "  Keeping first occurrence at lines $first_start-$first_end"
  
  # Process all other occurrences (to remove)
  for ((i=1; i<${#occurrences[@]}; i++)); do
    current=${occurrences[$i]}
    current_block=$(extract_rule_block "$CLEAN_STYLE_FILE" "$rule" "$current")
    current_start=$(echo "$current_block" | cut -d "," -f1)
    current_end=$(echo "$current_block" | cut -d "," -f2)
    
    # Add to lines to remove if not already included
    for ((line=current_start; line<=current_end; line++)); do
      if [[ ! " ${lines_to_remove[@]} " =~ " ${line} " ]]; then
        lines_to_remove+=($line)
      fi
    done
    
    echo "  Marking duplicate at lines $current_start-$current_end for removal"
  done
  
  # Sort lines to remove in descending order
  IFS=$'\n' sorted_lines=($(sort -nr <<<"${lines_to_remove[*]}"))
  unset IFS
  
  # Remove lines from the clean style file (in reverse order to maintain line numbers)
  for line in "${sorted_lines[@]}"; do
    sed -i.bak "${line}d" "$CLEAN_STYLE_FILE"
  done
done

# Reassemble the file
(cat "$VUE_PREFIX"; cat "$CLEAN_STYLE_FILE"; cat "$VUE_SUFFIX") > "$OUTPUT_FILE"

# Count the lines before and after
original_lines=$(wc -l < "$STYLE_FILE")
cleaned_lines=$(wc -l < "$CLEAN_STYLE_FILE")
lines_removed=$((original_lines - cleaned_lines))

echo "Cleaning complete!"
echo "Original style section: $original_lines lines"
echo "Cleaned style section: $cleaned_lines lines"
echo "Removed approximately: $lines_removed lines"
echo "Cleaned file saved as: $OUTPUT_FILE"

# Clean up temporary files
rm -rf "$TEMP_DIR" 