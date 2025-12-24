<!-- src/views/KluvTalk/KluvTalkChatRoomView.vue -->
<template>
  <div class="wrap">
    <div class="top">
      <div class="left">
        <RouterLink class="back" :to="{ name: 'kluvtalk-chat-list' }">← 목록</RouterLink>
        <h1 class="title">{{ roomTitle }}</h1>
        <p class="sub">
          WS: <span :class="store.socketStatus">{{ store.socketStatus }}</span>
          <span v-if="store.lastErrorMessage" class="err"> · {{ store.lastErrorMessage }}</span>
        </p>
      </div>

      <div class="right">
        <div class="chip" :class="{ on: canChat }">
          {{ canChat ? "회의 진행중" : "회의 시간이 아닙니다" }}
        </div>
      </div>
    </div>

    <div v-if="store.roomLoading" class="state">로딩중...</div>
    <div v-else-if="store.roomError" class="state error">방 정보를 불러오지 못했어요.</div>

    <div v-else class="grid">
      <!-- chat -->
      <section class="chat">
        <div class="log" ref="logRef">
          <div
            v-for="(m, idx) in store.messages"
            :key="idx"
            class="msg"
            :class="{ system: m.type === 'system' }"
          >
            <template v-if="m.type === 'system'">
              <div class="sys">{{ m.message }}</div>
              <div class="time">{{ formatTime(m.timestamp) }}</div>
            </template>

            <template v-else>
              <div class="avatar">{{ (m.username?.[0] ?? "?").toUpperCase() }}</div>
              <div class="body">
                <div class="meta">
                  <strong>{{ m.username }}</strong>
                  <span>{{ formatTime(m.timestamp) }}</span>
                </div>
                <div class="text">{{ m.message }}</div>
              </div>
            </template>
          </div>
        </div>

        <div class="composer">
          <input
            v-model="text"
            class="input"
            :disabled="!canChat"
            placeholder="메시지를 입력하세요"
            @keydown.enter.prevent="onSend"
          />
          <button class="btn" :disabled="!canChat || !text.trim()" @click="onSend">
            전송
          </button>
        </div>
      </section>

      <!-- participants -->
      <aside class="side">
        <div class="side-head">
          <h3>참여자</h3>
          <span class="count">{{ onlineCount }} / {{ totalMembers }}</span>
        </div>

        <ul class="people">
          <li v-for="p in store.participants" :key="p.id" :class="{ online: p.online }">
            <span class="role" v-if="p.isLeader">👑</span>
            <span class="name">{{ p.username }}</span>
            <span class="dot" />
          </li>
        </ul>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { RouterLink, useRoute } from "vue-router";
import { useKluvChatStore } from "@/stores/kluvChat";

const route = useRoute();
const store = useKluvChatStore();

const roomSlug = computed(() => route.params.roomSlug);
const text = ref("");

const logRef = ref(null);

const canChat = computed(() => !!store.room?.can_chat);
const roomTitle = computed(() => store.room?.name ?? `채팅방 (${roomSlug.value})`);

const totalMembers = computed(() => {
  // 백엔드 템플릿에서는 joined_members/total_members를 표시 :contentReference[oaicite:8]{index=8}
  return store.room?.total_members ?? store.participants.length ?? 0;
});

const onlineCount = computed(() => store.participants.filter((p) => p.online).length);

const formatTime = (ts) => {
  if (!ts) return "";
  // ts가 ISO든 "YYYY-mm-dd HH:MM:SS"든 최대한 안전하게 파싱
  const d = new Date(ts);
  if (!Number.isNaN(d.getTime())) {
    return d.toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit" });
  }
  return String(ts).slice(11, 16); // fallback
};

const scrollToBottom = async () => {
  await nextTick();
  const el = logRef.value;
  if (!el) return;
  el.scrollTop = el.scrollHeight;
};

const onSend = () => {
  if (!canChat.value) return;
  const v = text.value.trim();
  if (!v) return;
  store.sendMessage(v);
  text.value = "";
};

onMounted(async () => {
  await store.fetchRoomDetail(roomSlug.value);
  store.connectRoomSocket(roomSlug.value);
  await scrollToBottom();
});

onBeforeUnmount(() => {
  store.disconnectRoomSocket();
});

watch(
  () => store.messages.length,
  async () => {
    await scrollToBottom();
  }
);
</script>

<style scoped>
.wrap {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 16px;
}

.top {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.back {
  display: inline-block;
  color: #1a73e8;
  text-decoration: none;
  font-weight: 800;
  margin-bottom: 8px;
}
.back:hover { text-decoration: underline; }

.title { margin: 0; font-size: 26px; }
.sub { margin: 6px 0 0; color: #666; font-size: 13px; }
.sub .open { color: #0a7a2f; font-weight: 800; }
.sub .connecting { color: #8a6d00; font-weight: 800; }
.sub .closed, .sub .error { color: #b00020; font-weight: 800; }
.err { color: #b00020; }

.chip {
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid #eee;
  color: #666;
  font-size: 13px;
  font-weight: 800;
}
.chip.on {
  color: #0a7a2f;
  border-color: #bfe8c9;
  background: #f3fff6;
}

.state { color: #666; padding: 18px 0; }
.state.error { color: #b00020; }

.grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 14px;
}
@media (max-width: 860px) {
  .grid { grid-template-columns: 1fr; }
}

.chat {
  border: 1px solid #eee;
  border-radius: 16px;
  background: #fff;
  display: flex;
  flex-direction: column;
  min-height: 520px;
}

.log {
  padding: 14px;
  overflow-y: auto;
  flex: 1;
}

.msg {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
  align-items: flex-start;
}
.msg.system {
  gap: 8px;
  color: #777;
  font-style: italic;
}
.sys { flex: 1; }
.time { font-size: 12px; color: #999; white-space: nowrap; }

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 999px;
  background: #4caf50; /* 템플릿 느낌 유지 */
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  flex-shrink: 0;
}

.body {
  background: #f6f6f6;
  border-radius: 12px;
  padding: 10px 12px;
  max-width: 70%;
}
.meta {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  font-size: 12px;
  color: #666;
  margin-bottom: 6px;
}
.text { white-space: pre-wrap; }

.composer {
  display: flex;
  gap: 10px;
  padding: 12px;
  border-top: 1px solid #eee;
}
.input {
  flex: 1;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 12px;
  outline: none;
}
.btn {
  border: 0;
  border-radius: 12px;
  padding: 12px 14px;
  cursor: pointer;
  font-weight: 900;
}
.btn:disabled { opacity: 0.5; cursor: not-allowed; }

.side {
  border: 1px solid #eee;
  border-radius: 16px;
  background: #fff;
  padding: 14px;
  height: fit-content;
}

.side-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 10px;
}
.side-head h3 { margin: 0; }
.count { color: #777; font-size: 13px; }

.people {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 8px;
}
.people li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 10px;
  border: 1px solid #f1f1f1;
  border-radius: 12px;
  color: #888;
}
.people li.online { color: #0a7a2f; font-weight: 800; }

.role { margin-right: 6px; }
.name { flex: 1; }

.dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: #ccc;
}
.people li.online .dot { background: #0a7a2f; }
</style>
