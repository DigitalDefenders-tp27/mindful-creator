<template>
  <!-- This is a style-only component -->
</template>

<style>
/* Navigation Link Styles for Dropdown Menu */
.dropdown-nav-item {
  opacity: 1;
  position: relative;
  padding: 0.5rem 1.25rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  margin: 0;
  display: block;
  width: 100%;
  text-align: right;
  line-height: 1.2;
  color: #555;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.2s;
  text-decoration: none;
  letter-spacing: 0.5px;
}

.dropdown-nav-item:hover {
  color: #e75a97;
}

.dropdown-nav-item.active {
  color: #e75a97;
  font-weight: 600;
}

.dropdown-nav-item span {
  font-size: 0.9rem;
  margin: 0;
  padding: 0;
}

/* Two-word Navigation Link Styles */
.dropdown-nav-item.two-words {
  display: flex;
  flex-direction: row;
  gap: 4px;
  justify-content: flex-end;
  padding: 0.5rem 1.25rem;
  line-height: 1.1;
}

.dropdown-nav-item.two-words span {
  font-size: 0.9rem;
  display: inline;
  margin: 0;
  padding: 0;
}

.dropdown-nav-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.dropdown-nav-item + .dropdown-nav-item {
  margin-top: 2px;
}

/* Small Screen Responsive Adjustments */
@media (max-width: 640px) {
  .dropdown-nav-item {
    font-size: 0.9rem;
  }
  
  .dropdown-nav-item.two-words span {
    font-size: 0.9rem;
  }
}
</style> 