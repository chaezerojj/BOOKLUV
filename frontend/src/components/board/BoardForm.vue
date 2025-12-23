<template>
    <form class="form" @submit.prevent="emitSubmit">
        <label>제목</label>
        <input v-model="localTitle" maxlength="20" required />

        <label>내용</label>
        <textarea v-model="localContent" rows="10" required />

        <div class="actions">
            <button type="submit" :disabled="loading">{{ submitText }}</button>
            <button type="button" @click="$emit('cancel')" :disabled="loading">취소</button>
        </div>

        <p v-if="errorText" class="error">{{ errorText }}</p>
    </form>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
    title: { type: String, default: "" },
    content: { type: String, default: "" },
    loading: { type: Boolean, default: false },
    submitText: { type: String, default: "저장" },
    errorText: { type: String, default: "" },
});

const emit = defineEmits(["submit", "cancel", "update:title", "update:content"]);

const localTitle = ref(props.title);
const localContent = ref(props.content);

watch(
    () => props.title,
    (v) => (localTitle.value = v ?? "")
);
watch(
    () => props.content,
    (v) => (localContent.value = v ?? "")
);

// v-model처럼 동작시키기
watch(localTitle, (v) => emit("update:title", v));
watch(localContent, (v) => emit("update:content", v));

const emitSubmit = () => {
    emit("submit", { title: localTitle.value.trim(), content: localContent.value.trim() });
};
</script>

<style scoped>
.form {
    display: grid;
    gap: 10px;
}

input,
textarea {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
    font-size: 14px;
}

.actions {
    display: flex;
    gap: 10px;
    margin-top: 8px;
}

button {
    border: 1px solid #ddd;
    background: white;
    border-radius: 10px;
    padding: 10px 14px;
    cursor: pointer;
}

button:disabled {
    opacity: .45;
    cursor: not-allowed;
}

.error {
    color: #d00;
}
</style>
