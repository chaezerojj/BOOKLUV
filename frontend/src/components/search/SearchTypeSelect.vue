<template>
  <div class="search-type-select">
    <select @change="handleSelectChange">
      <option value="book">책</option>
      <option value="club">모임</option>
    </select>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue';

const emit = defineEmits();

// 드롭다운에서 선택된 값 변경 시 부모 컴포넌트로 이벤트 발생
const handleSelectChange = (event) => {
  emit('update-search-type', event.target.value);
};
</script>

<style scoped>
.search-type-select {
  margin: 10px;
}

select {
  padding: 5px;
  font-size: 16px;
}
</style>
