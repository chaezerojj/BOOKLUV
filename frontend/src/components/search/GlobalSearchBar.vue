<template>
  <div class="container">
    <div>검색창 (전역)</div>
    <search-type-select />
  </div>
</template>

<script setup>
import SearchTypeSelect from './SearchTypeSelect.vue';


</script>

<style scoped>
.container {
  display: flex;
}

.container div {
  border: 1px solid purple;
}

</style>