<template>
  <div class="mykluv">
    <div class="head">
      <h2 class="title">나의 채팅방</h2>
      <p class="sub">시작 10분 전부터 입장 가능, 시작 후에는 채팅 가능해요.</p>
    </div>

    <div v-if="loading" class="state">불러오는 중...</div>
    <div v-else-if="error" class="state error">목록을 불러오지 못했어요.</div>

    <div v-else class="sections">
      <section class="section">
        <div class="section-head">
          <h3>나의 채팅방</h3><span class="count">{{ items.length }}</span>
        </div>

        <div v-if="items.length === 0" class="empty">목록을 불러오지 못했어요.</div>

        <div class="list">
          <div v-for="item in items" :key="item.meeting_id" class="item">
            <div class="left">
              <div class="title">{{ item.title }}</div>
              <div class="time">{{ item.started_at ? formatRange(item.started_at, item.finished_at) : '시간 정보 없음' }}
              </div>
            </div>
            <div class="right">
              <RouterLink v-if="item.can_enter && item.room_slug" :to="toChat(item)" class="enter">채팅방 입장</RouterLink>
              <span v-else-if="item.status === '진행예정'" class="waiting">방 준비중</span>
              <span v-else class="waiting">입장 불가</span>
            </div>
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

/* list style for my rooms */
.list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  border-radius: 12px;
  background: #fff;
  border: 1px solid #eee;
}

.left .title {
  font-weight: 700;
}

.left .time {
  color: #666;
  font-size: .9rem;
}

.enter {
  padding: 8px 10px;
  background: #1a73e8;
  color: #fff;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 800;
}

.waiting {
  padding: 8px 10px;
  border-radius: 10px;
  background: #f3f3f3;
  color: #777;
  border: 1px solid #e6e6e6;
  font-weight: 900;
}
</style>
