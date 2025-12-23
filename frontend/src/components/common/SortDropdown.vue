<template>
  <div class="root" ref="rootEl">
    <button
      type="button"
      class="trigger"
      :aria-expanded="open"
      aria-haspopup="listbox"
      @click="toggle"
    >
      <span class="label">{{ label }}</span>
      <span class="value">{{ selectedLabel }}</span>
      <span class="chev" :class="{ open }">▾</span>
    </button>

    <div v-if="open" class="menu" role="listbox">
      <button
        v-for="opt in options"
        :key="opt.value"
        type="button"
        class="option"
        role="option"
        :aria-selected="opt.value === modelValue"
        :class="{ active: opt.value === modelValue }"
        @click="select(opt.value)"
      >
        {{ opt.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from "vue";

const props = defineProps({
  modelValue: { type: String, required: true },
  options: { type: Array, required: true },
  label: { type: String, default: "정렬" },
});

const emit = defineEmits(["update:modelValue"]);

const open = ref(false);
const rootEl = ref(null);

const selectedLabel = computed(() => {
  return props.options.find((o) => o.value === props.modelValue)?.label ?? "";
});

const toggle = () => {
  open.value = !open.value;
};

const select = (v) => {
  emit("update:modelValue", v);
  open.value = false;
};

const onClickOutside = (e) => {
  if (!rootEl.value) return;
  if (!rootEl.value.contains(e.target)) open.value = false;
};

const onKeydown = (e) => {
  if (e.key === "Escape") open.value = false;
};

onMounted(() => {
  window.addEventListener("mousedown", onClickOutside);
  window.addEventListener("keydown", onKeydown);
});

onBeforeUnmount(() => {
  window.removeEventListener("mousedown", onClickOutside);
  window.removeEventListener("keydown", onKeydown);
});
</script>

<style scoped>
.root {
  position: relative;
  display: inline-block;
}

.trigger {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  border: 1px solid #e5e5e5;
  background: #fff;
  border-radius: 999px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 13px;
  line-height: 1;
}

.trigger:hover {
  background: #fafafa;
}

.label {
  opacity: 0.7;
}

.value {
  font-weight: 700;
  letter-spacing: -0.2px;
}

.chev {
  opacity: 0.7;
  transform: translateY(-1px);
  transition: transform 120ms ease;
}

.chev.open {
  transform: translateY(-1px) rotate(180deg);
}

.menu {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  min-width: 180px;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 14px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
  padding: 6px;
  z-index: 30;
}

.option {
  width: 100%;
  text-align: left;
  border: 0;
  background: transparent;
  padding: 10px 10px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 13px;
}

.option:hover {
  background: #f6f6f6;
}

.option.active {
  background: #f2f2f2;
  font-weight: 800;
}
</style>
