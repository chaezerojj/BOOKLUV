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

      <div v-else class="sections">
        <div v-for="group in groups" :key="group.type" class="group">
          <h3 class="group-title">{{ group.title }}</h3>

          <div v-if="group.list.length === 0" class="group-empty">
            해당하는 모임이 없습니다.
          </div>

          <ul v-else class="list">
            <li v-for="(room, idx) in group.list" :key="idx" class="row">
              <div class="left">
                <div class="room-name">{{ room.room_name }}</div>
                <div class="time">
                  시작: {{ formatDateTime(room.started_at) }}<br />
                  종료: {{ formatDateTime(room.finished_at) }}
                </div>
              </div>

              <div class="right">
                <span v-if="group.type === 'active'" class="badge active">진행 중</span>
                <span v-else-if="group.type === 'upcoming'" class="badge upcoming">진행 예정</span>
                <span v-else class="badge ended">종료</span>

                <!-- room_slug 있을 때만 링크 (진행 중일 때만) -->
                <RouterLink v-if="room.is_active && room.room_slug" class="enter"
                  :to="{ name: 'kluvtalk-chat-room', params: { roomSlug: room.room_slug } }">
                  채팅방 입장
                </RouterLink>
              </div>
            </li>
          </ul>
          <button v-if="group.type === 'ended' && group.hasMore" class="more-btn" @click="loadMoreEnded">
            더보기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import { http } from "@/api/http"

const loading = ref(false)
const error = ref(null)
const items = ref([])
const endedLimit = ref(5)

const loadMoreEnded = () => {
  endedLimit.value += 5
}

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

const groups = computed(() => {
  const now = new Date()
  const active = []
  const upcoming = []
  const ended = []

  items.value.forEach(room => {
    if (room.is_active) {
      active.push(room)
    } else if (new Date(room.started_at) > now) {
      upcoming.push(room)
    } else {
      ended.push(room)
    }
  })

  // 정렬: 진행중/예정은 시작시간 빠른순, 종료는 종료시간 느린순(최신순)
  active.sort((a, b) => new Date(a.started_at) - new Date(b.started_at))
  upcoming.sort((a, b) => new Date(a.started_at) - new Date(b.started_at))
  ended.sort((a, b) => new Date(b.finished_at) - new Date(a.finished_at))

  const result = [
    { title: '🔥 진행 중인 모임', list: active, type: 'active' },
    { title: '⏳ 진행 예정 모임', list: upcoming, type: 'upcoming' }
  ]

  if (ended.length > 0) {
    result.push({
      title: '🏁 종료된 모임',
      list: ended.slice(0, endedLimit.value),
      type: 'ended',
      hasMore: ended.length > endedLimit.value
    })
  }
  return result
})

const pad2 = (n) => String(n).padStart(2, "0")

const formatDateTime = (iso) => {
  if (!iso) return "-"
  const d = new Date(iso)
  return `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())} ${pad2(d.getHours())}:${pad2(d.getMinutes())}`
}
</script>

<style scoped>
.head {
  margin-bottom: 12px;
}

.title {
  margin: 0;
  font-size: 1.2rem;
}

.sub {
  margin: 6px 0 0;
  color: #666;
  font-size: .9rem;
}

.state {
  padding: 14px;
  color: #555;
}

.state.error {
  color: #c0392b;
}

.empty {
  padding: 12px;
  background: #fafafa;
  color: #888;
  border-radius: 10px;
}

.sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.group-title {
  margin: 0 0 10px 4px;
  font-size: 1rem;
  font-weight: 800;
  color: #444;
}

.group-empty {
  padding: 20px;
  text-align: center;
  color: #999;
  font-size: 0.9rem;
  background: #fafafa;
  border-radius: 12px;
  border: 1px dashed #e0e0e0;
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

.room-name {
  font-weight: 800;
  margin-bottom: 6px;
}

.time {
  color: #666;
  font-size: .9rem;
  line-height: 1.4;
}

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

.badge.upcoming {
  background: #fff8e1;
  color: #f57f17;
  border-color: #ffe0b2;
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

.more-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 12px;
  margin-top: 16px;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  color: #666;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.more-btn:hover {
  background: #fafafa;
  border-color: #ccc;
  color: #333;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.more-btn:active {
  transform: translateY(0);
  box-shadow: none;
  background: #f5f5f5;
}
</style>
