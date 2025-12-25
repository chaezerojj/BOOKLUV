<template>
  <div class="page">
    <div class="head">
      <RouterLink class="back" :to="{ name: 'mypage-mykluv' }">← 목록</RouterLink>
      <div class="title">
        <h1 class="h1">{{ store.room?.name ?? "대기실" }}</h1>
        <p class="sub" v-if="store.meeting">
          {{ store.meeting.title }}
        </p>
      </div>
    </div>

    <div v-if="store.roomLoading" class="state">불러오는 중...</div>
    <div v-else-if="store.roomError" class="state error">채팅방 정보를 불러오지 못했어요.</div>

    <div v-else class="container">
      <!-- chat -->
      <section class="chat-area">
        <div ref="chatLog" class="chat-log">
          <template v-for="(m, idx) in store.messages" :key="idx">
            <div v-if="m.type === 'system'" class="system">
              {{ m.message }}
            </div>

            <div v-else class="message" :class="isSelf(m) ? 'self' : 'other'">
              <div class="message-content">
                <div class="message-header">
                  <strong>{{ m.username }}</strong>
                  <span>{{ time(m.timestamp) }}</span>
                </div>
                <div class="message-body">{{ m.message }}</div>
              </div>
            </div>
          </template>
        </div>

        <div class="input-area">
          <input
            v-model="text"
            class="input"
            type="text"
            placeholder="메시지 입력..."
            :disabled="!store.canChat"
            @keydown.enter="onSend"
          />
          <button class="send" type="button" :disabled="!store.canChat" @click="onSend">
            전송
          </button>
        </div>

        <div v-if="!store.canChat" class="hint">
          현재는 채팅 가능한 시간이 아니에요.
        </div>
      </section>

      <!-- participants -->
      <aside class="participants">
        <div class="p-head">
          <h4>👥 참여자</h4>
          <span class="count">({{ onlineCount }}/{{ store.participants.length }})</span>
        </div>

        <ul class="p-list">
          <li v-for="p in store.participants" :key="p.id" class="p-item">
            <span class="dot" :class="p.online ? 'online' : 'offline'"></span>
            <span class="p-name" :class="{ on: p.online }">
              <span v-if="p.isLeader" class="crown">👑</span>
              {{ p.nickname }}
            </span>
          </li>
        </ul>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useKluvChatStore } from "@/stores/kluvChat";

const route = useRoute();
const store = useKluvChatStore();

const roomSlug = computed(() => String(route.params.roomSlug ?? ""));
const text = ref("");
const chatLog = ref(null);

const time = (ts) => store.fmtTime(ts);

const isSelf = (m) => {
  const myId = store.currentUser?.id;
  if (myId == null) return false;
  return String(m.user_id) === String(myId);
};

const onlineCount = computed(() => store.participants.filter((p) => p.online).length);

const scrollBottom = async () => {
  await nextTick();
  if (!chatLog.value) return;
  chatLog.value.scrollTop = chatLog.value.scrollHeight;
};

const onSend = () => {
  if (!store.canChat) return;
  const msg = text.value.trim();
  if (!msg) return;
  store.sendMessage(msg);
  text.value = "";
};

watch(
  () => store.messages.length,
  async () => {
    await scrollBottom();
  }
);

onMounted(async () => {
  await store.fetchRoomDetail(roomSlug.value);
  await scrollBottom();
  store.connectRoomSocket(roomSlug.value);
});

onBeforeUnmount(() => {
  store.disconnectRoomSocket();
});
</script>

<style scoped>
.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 18px 16px 60px;
}
.head {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  margin-bottom: 12px;
}
.back {
  text-decoration: none;
  color: #1a73e8;
  font-weight: 900;
  padding: 8px 10px;
  border-radius: 12px;
}
.back:hover {
  background: rgba(26,115,232,0.08);
}
.title {
  flex: 1;
}
.h1 {
  margin: 0;
  font-size: 22px;
  font-weight: 900;
}
.sub {
  margin: 6px 0 0;
  color: #666;
  font-size: 13px;
}

.state {
  padding: 14px;
  background: #fafafa;
  border: 1px solid #eee;
  border-radius: 14px;
}
.state.error {
  background: #fff5f5;
  border-color: #ffd6d6;
  color: #b42318;
}

.container {
  display: flex;
  gap: 16px;
  height: 78vh;
}
@media (max-width: 980px) {
  .container { flex-direction: column; height: auto; }
}

.chat-area {
  flex: 3;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 16px;
  border: 1px solid #eee;
  box-shadow: 0 10px 22px rgba(0,0,0,0.06);
  overflow: hidden;
}

.chat-log {
  flex: 1;
  overflow-y: auto;
  padding: 18px;
  background: #f9f9fb;
  display: flex;
  flex-direction: column;
}

.message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 14px;
}
.message.self {
  justify-content: flex-end;
}
.message-content {
  padding: 10px 14px;
  border-radius: 14px;
  max-width: 65%;
  font-size: 14px;
}
.message.self .message-content {
  background: #fee500;
  color: #3c1e1e;
  border-top-right-radius: 6px;
  margin-right: 8px;
}
.message.other .message-content {
  background: #fff;
  border: 1px solid #e6e6e6;
  border-top-left-radius: 6px;
  margin-left: 8px;
}

.message-header {
  font-size: 11px;
  color: #888;
  margin-bottom: 4px;
  display: flex;
  gap: 8px;
}
.message-body {
  white-space: pre-wrap;
  word-break: break-word;
}

.system {
  align-self: center;
  color: #777;
  font-size: 12px;
  margin: 10px 0;
  background: #eee;
  border-radius: 999px;
  padding: 4px 12px;
}

.input-area {
  padding: 14px;
  background: #fff;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
}
.input {
  flex: 1;
  padding: 11px 12px;
  border: 1px solid #ddd;
  border-radius: 12px;
  outline: none;
}
.send {
  padding: 11px 16px;
  border-radius: 12px;
  border: none;
  background: #1a73e8;
  color: #fff;
  font-weight: 900;
  cursor: pointer;
}
.send:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}
.hint {
  padding: 10px 14px;
  font-size: 12px;
  color: #888;
  background: #fff;
  border-top: 1px dashed #eee;
}

/* participants */
.participants {
  flex: 1;
  background: #fff;
  border-radius: 16px;
  border: 1px solid #eee;
  box-shadow: 0 10px 22px rgba(0,0,0,0.06);
  padding: 16px;
}
.p-head {
  display: flex;
  align-items: center;
  gap: 8px;
}
.p-head h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 900;
}
.count {
  color: #888;
  font-size: 12px;
}

.p-list {
  list-style: none;
  padding: 0;
  margin: 14px 0 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.p-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
}
.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}
.dot.online {
  background: #4caf50;
  box-shadow: 0 0 6px #4caf50;
}
.dot.offline {
  background: #cfcfcf;
}
.p-name {
  color: #888;
}
.p-name.on {
  color: #2e7d32;
  font-weight: 900;
}
.crown {
  margin-right: 4px;
}
</style>
