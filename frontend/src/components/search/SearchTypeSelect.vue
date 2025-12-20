<template>
  <select class="select" :value="modelValue" @change="onChange">
    <option value="book">책</option>
    <option value="kluvtalk">모임</option>
  </select>
</template>

<script setup>
const props = defineProps({
  modelValue: { type: String, default: 'book' },
})

const emit = defineEmits(['update:modelValue'])

const onChange = (e) => {
  emit('update:modelValue', e.target.value)
}
</script>

<style scoped>
.select {
  width: 100px;
  height: 40px;
  padding: 0 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
</style>
