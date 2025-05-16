#!/bin/bash

# Set the input file
INPUT_FILE="frontend/src/views/CreatorWellbeingView.vue"
OUTPUT_FILE="frontend/src/views/CreatorWellbeingView.clean.vue"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: Input file $INPUT_FILE not found."
  exit 1
fi

echo "Analyzing CSS in $INPUT_FILE..."

# Extract <style> section and save to a temporary file
sed -n '/<style scoped>/,/<\/style>/p' "$INPUT_FILE" > temp_style.css

# Create a temporary file with line numbers
cat -n temp_style.css > temp_style_with_lines.txt

# Define duplicate CSS rules to search for
declare -a duplicates=(
  ".tab"
  ".tab.active"
  ".tab.active::after"
  ".action-btn"
  ".action-btn:hover"
  ".btn-icon"
  ".resource-actions"
  "@media (max-width: 480px) .resource-actions"
  "@media (max-width: 480px) .action-btn"
  "@media (max-width: 480px) .position-btn"
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

# Print duplicate rules found
echo "Found duplicate CSS rules:"
echo "-----------------------"

# Loop through each duplicate rule and find occurrences
for rule in "${duplicates[@]}"; do
  # Escape for grep
  search_rule=$(echo "$rule" | sed 's/[.]/\\./g' | sed 's/\[/\\[/g' | sed 's/\]/\\]/g')
  
  # Find the rule and show line numbers
  echo "Rule: $rule"
  grep -n "$search_rule" temp_style.css | cut -d ":" -f1
  echo "-----------------------"
done

# Create a cleaned version by removing the second occurrence of each duplicate
cp "$INPUT_FILE" "$OUTPUT_FILE"

# Generate a list of line numbers to delete in the style section
# This would involve calculating absolute positions in the file, which is complex
# For now, we'll just identify duplicates to be manually edited

echo "Created duplicate CSS report. Please manually edit $OUTPUT_FILE using the line numbers above."
echo "Keep the first occurrence of each duplicate rule and remove subsequent ones."

# Clean up temporary files
rm temp_style.css temp_style_with_lines.txt

echo "Script completed. Check the output above for duplicate CSS rules." 