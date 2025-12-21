<template>
  <!-- <select class="select" :value="modelValue" @change="onChange">
    <option class="option" value="book" selected>책</option> 
    <option class="option" value="kluvtalk">모임</option>
  </select> -->

  <div class="dropdown" ref="root">
    <button type="button" class="trigger" @click="toggle" :aria-expanded="open" aria-haspopup="listbox">
      <span class="label">{{ selectedLabel }}</span>
      <span class="chev" :class="{ open }">▾</span>
    </button>

    <!-- option -->
    <ul v-show="open" class="menu" role="listbox" :aria-activedescendant="activeId" @keydown.prevent.down="onArrowDown"
      @keydown.prevent.up="onArrowUp" @keydown.prevent.enter="onEnter" @keydown.prevent.esc="close" tabindex="-1"
      ref="menuEl">
      <li v-for="(opt, idx) in options" :key="opt.value" class="item" role="option" :id="`opt-${uid}-${opt.value}`"
        :aria-selected="opt.value === modelValue" :class="{
          active: idx === activeIndex,
          selected: opt.value === modelValue,
        }" @mouseenter="activeIndex = idx" @click="select(opt.value)">
        {{ opt.label }}
      </li>
    </ul>
  </div>
</template>


<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue';
  
const props = defineProps({
  modelValue: { type: String, default: 'book' },
})

const emit = defineEmits(['update:modelValue'])

const options = [
  { value: 'book', label: '책'},
  { value: 'kluvtalk', label: 'KluvTalk'},
]

const root = ref(null)
const menuEl = ref(null)
const open = ref(false)
const activeIndex = ref(0)

// uid (id 충돌 방지)
const uid = Math.random().toString(16).slice(2)

const selectedLabel = computed(() => {
  return options.find(o => o.value === props.modelValue)?.label ?? '선택'
})

const activeId = computed(() => {
  const opt = options[activeIndex.value]
  return opt ? `opt-${uid}-${opt.value}` : undefined
})

const setActiveToSelected = () => {
  const idx = options.findIndex(o => o.value === props.modelValue)
  activeIndex.value = idx >= 0 ? idx : 0
}

const focusMenu = async () => {
  await nextTick()
  menuEl.value?.focus?.()
}

const toggle = async () => {
  open.value = !open.value
  if (open.value) {
    setActiveToSelected()
    await focusMenu()
  }
}

const close = () => {
  open.value = false
}

const select = value => {
  emit('update:modelValue', value)
  close()
}

const onArrowDown = () => {
  activeIndex.value = (activeIndex.value + 1) % options.length
}

const onArrowUp = () => {
  activeIndex.value = (activeIndex.value - 1 + options.length) % options.length
}

const onEnter = () => {
  const opt = options[activeIndex.value]
  if (opt) select(opt.value)
}

// 바깥 클릭 닫기
const onClickOutside = (e) => {
  if (!root.value) return
  if (!root.value.contains(e.target)) close()
}

onMounted(() => {
  window.addEventListener('mousedown', onClickOutside)
})

onBeforeUnmount(() => {
  window.removeEventListener('mousedown', onClickOutside)
})

</script>

<style scoped>
.dropdown {
  position: relative;
  width: 90px;
  font-size: 13px;
}

/* 닫힌 상태 버튼 (select처럼 보이게) */
.trigger {
  width: 100%;
  height: 40px;
  padding: 0 10px;
  border: none;
  border-radius: 13px;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.trigger:focus {
  outline: none;
  box-shadow: 0 0 0 1px rgba(13, 110, 253, 0.15);
}

.label {
  font-size: 14px;
}

.chev {
  font-size: 17px;
  transition: transform 0.15s ease;
}

.chev.open {
  transform: rotate(180deg);
}

.menu {
  position: absolute;
  top: calc(100% + 10px);
  left: -5px;
  width: 85%;
  margin: 0;
  padding: 6px;
  list-style: none;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.1);
  z-index: 50;
}

.item {
  padding: 10px 10px;
  border-radius: 13px;
  cursor: pointer;
  user-select: none;
}

/* ✅ hover 색: 여기서 바꿔 */
.item:hover,
.item.active {
  background: #f1f5ff; /* 원하는 색으로 */
}

/* 선택된 값 표시 */
.item.selected {
  font-weight: 700;
}
</style>