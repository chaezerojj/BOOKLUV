<template>
  <div class="mykluv">
    <div class="head">
      <h2 class="title">나의 채팅방</h2>
      <p class="sub">시작 10분 전부터 입장 가능, 시작 후에는 채팅 가능해요.</p>
    </div>

    <div v-if="loading" class="state">불러오는 중...</div>
    <div v-else-if="error" class="state error">목록을 불러오지 못했어요.</div>

    <div v-else class="sections">
      <!-- 진행중 -->
      <section class="section">
        <div class="section-head">
          <h3>진행중</h3><span class="count">{{ grouped.active.length }}</span>
        </div>

        <div v-if="grouped.active.length === 0" class="empty">진행중인 채팅방이 없어요.</div>

        <div class="cards">
          <RouterLink v-for="item in grouped.active" :key="item.meeting_id" class="card" :to="toChat(item)">
            <div class="badge active">진행중</div>
            <div class="name">{{ item.title }}</div>
            <div class="time">{{ formatRange(item.started_at, item.finished_at) }}</div>
            <div class="cta">입장 →</div>
          </RouterLink>
        </div>
      </section>

      <!-- 진행전 -->
      <section class="section">
        <div class="section-head">
          <h3>진행전</h3><span class="count">{{ grouped.soon.length }}</span>
        </div>

        <div v-if="grouped.soon.length === 0" class="empty">곧 시작할 채팅방이 없어요.</div>

        <div class="cards">
          <RouterLink v-for="item in grouped.soon" :key="item.meeting_id" class="card" :to="toChat(item)">
            <div class="badge soon">진행전</div>
            <div class="name">{{ item.title }}</div>
            <div class="time">{{ formatRange(item.started_at, item.finished_at) }}</div>
            <div class="cta">대기실 →</div>
          </RouterLink>
        </div>
      </section>

      <!-- 진행예정 -->
      <section class="section">
        <div class="section-head">
          <h3>진행예정</h3><span class="count">{{ grouped.planned.length }}</span>
        </div>

        <div v-if="grouped.planned.length === 0" class="empty">예정된 모임이 없어요.</div>

        <div class="cards">
          <div v-for="item in grouped.planned" :key="item.meeting_id" class="card disabled" title="시작 10분 전부터 입장 가능해요.">
            <div class="badge planned">진행예정</div>
            <div class="name">{{ item.title }}</div>
            <div class="time">{{ formatRange(item.started_at, item.finished_at) }}</div>
            <div class="cta muted">방 준비중</div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"
import { http } from "@/api/http" // axios 인스턴스(세션이면 withCredentials 필수)

const router = useRouter()

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

const grouped = computed(() => {
  const planned = []
  const soon = []
  const active = []

  for (const it of items.value) {
    if (it.status === "진행중") active.push(it)
    else if (it.status === "진행전") soon.push(it)
    else planned.push(it) // 진행예정
  }

  return { planned, soon, active }
})


const toChat = (item) => {
  // 진행예정(아직 방 없음) or 방slug 없음 → 이동 불가
  if (!item.can_enter || !item.room_slug) {
    return { name: "mypage-mykluv" } // 실제로는 disabled 카드라 클릭 안 되게 처리하는 게 더 좋음
  }

  // ✅ 라우터 params는 roomSlug
  return {
    name: "kluvtalk-chat-room",
    params: { roomSlug: item.room_slug },
  }
}

const pad2 = (n) => String(n).padStart(2, "0")
const formatRange = (startISO, endISO) => {
  if (!startISO || !endISO) return "-"
  const s = new Date(startISO)
  const e = new Date(endISO)
  return `${pad2(s.getMonth()+1)}/${pad2(s.getDate())} ${pad2(s.getHours())}:${pad2(s.getMinutes())} ~ ${pad2(e.getHours())}:${pad2(e.getMinutes())}`
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

.sections {
  display: grid;
  gap: 16px;
}

.section {
  background: #fff;
  border-radius: 12px;
  padding: 14px;
}

.section-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 10px;
}

.count {
  color: #888;
  font-size: .9rem;
}

.empty {
  padding: 12px;
  background: #fafafa;
  color: #888;
  border-radius: 10px;
}

.cards {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* 카드 고정 크기 */
.card {
  position: relative;
  width: 220px;
  height: 130px;
  padding: 14px;
  border-radius: 14px;
  border: 1px solid #eee;
  background: #fafafa;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card:hover {
  background: #f3f3f3;
}

.card.disabled {
  opacity: .65;
  cursor: not-allowed;
}

.badge {
  position: absolute;
  top: 10px;
  left: 10px;
  font-size: .75rem;
  padding: 4px 8px;
  border-radius: 999px;
  background: #eaeaea;
}

.badge.active {
  background: #e6f7ff;
}

.badge.soon {
  background: #fff7e6;
}

.badge.planned {
  background: #f5f5f5;
}

.name {
  margin-top: 18px;
  font-weight: 700;
  line-height: 1.2;
  max-height: 2.4em;
  overflow: hidden;
}

.time {
  font-size: .85rem;
  color: #666;
}

.cta {
  font-weight: 700;
}

.cta.muted {
  color: #888;
}
</style>
