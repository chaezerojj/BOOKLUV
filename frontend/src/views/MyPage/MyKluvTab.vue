<template>
  <div class="mykluv">
    <div class="head">
      <h2 class="title">나의 모임방</h2>
      <p class="sub">참여 중인 모임의 채팅방 목록이에요.</p>
    </div>

    <div v-if="loading" class="state">불러오는 중...</div>
    <div v-else-if="error" class="state error">목록을 불러오지 못했어요.</div>

    <div v-else>
      <div v-if="items.length === 0" class="empty">참여 중인 모임이 없습니다.</div>

      <ul v-else class="list">
        <li v-for="(room, idx) in items" :key="idx" class="row">
          <div class="left">
            <div class="room-name">{{ room.room_name }}</div>
            <div class="time">
              시작: {{ formatDateTime(room.started_at) }}<br />
              종료: {{ formatDateTime(room.finished_at) }}
            </div>
          </div>

          <div class="right">
            <span v-if="room.is_active" class="badge active">진행 중</span>
            <span v-else class="badge ended">종료</span>

            <!-- room_slug 있을 때만 링크 -->
            <RouterLink
              v-if="room.is_active && room.room_slug"
              class="enter"
              :to="{ name: 'kluvtalk-chat-room', params: { roomSlug: room.room_slug } }"
            >
              채팅방 입장
            </RouterLink>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { http } from "@/api/http" // ✅ 네 http.js가 export const http 라서 이게 맞음

const loading = ref(false)
const error = ref(null)
const items = ref([])

const fetchMyRooms = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await http.get("/api/v1/auth/myroom/api/")
    items.value = res.data?.results ?? []
  } catch (e) {
    error.value = e
    items.value = []
  } finally {
    loading.value = false
  }
}

onMounted(fetchMyRooms)

const pad2 = (n) => String(n).padStart(2, "0")

const formatDateTime = (iso) => {
  if (!iso) return "-"
  const d = new Date(iso)
  return `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())} ${pad2(d.getHours())}:${pad2(d.getMinutes())}`
}
</script>

<style scoped>
.head { margin-bottom: 12px; }
.title { margin: 0; font-size: 1.2rem; }
.sub { margin: 6px 0 0; color: #666; font-size: .9rem; }

.state { padding: 14px; color: #555; }
.state.error { color: #c0392b; }

.empty {
  padding: 12px;
  background: #fafafa;
  color: #888;
  border-radius: 10px;
}

.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 10px;
}

.row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 14px;
  border: 1px solid #eee;
  border-radius: 12px;
  background: #fff;
}

.room-name { font-weight: 800; margin-bottom: 6px; }
.time { color: #666; font-size: .9rem; line-height: 1.4; }

.right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  min-width: 120px;
}

.badge {
  font-size: .85rem;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid #e6e6e6;
  font-weight: 800;
}

.badge.active {
  background: #e8fff2;
  color: #1b7f3a;
  border-color: #bff0d1;
}

.badge.ended {
  background: #f3f3f3;
  color: #777;
}

.enter {
  padding: 8px 10px;
  background: #1a73e8;
  color: #fff;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 900;
}
</style>
