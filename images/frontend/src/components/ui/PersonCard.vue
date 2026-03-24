<template>
  <div class="person-card" @click="handleClick">
    <div class="person-avatar">
      <div class="avatar-placeholder">{{ initials }}</div>
    </div>
    <div class="person-info">
      <h3 class="person-name">{{ name }}</h3>
      <div class="person-roles">
        <span
          v-for="role in displayRoles"
          :key="role"
          :class="['role-tag', getRoleClass(role)]"
        >
          {{ getRoleDisplayName(role) }}
        </span>
        <span v-if="roles.length > maxRoles" class="role-more">
          +{{ roles.length - maxRoles }}
        </span>
      </div>
      <div class="person-filmworks">
        <span class="filmworks-count">
          {{ filmworksText }}
        </span>
      </div>
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface Props {
  id: string;
  name: string;
  roles?: string[];
  filmworkCount?: number;
  maxRoles?: number;
  clickable?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  roles: () => [],
  filmworkCount: 0,
  maxRoles: 3,
  clickable: true,
});

const emit = defineEmits<{
  click: [id: string];
}>();

const initials = computed(() => {
  return props.name
    .split(" ")
    .map((part) => part.charAt(0))
    .join("")
    .toUpperCase()
    .slice(0, 2);
});

const displayRoles = computed(() => {
  return props.roles.slice(0, props.maxRoles);
});

const filmworksText = computed(() => {
  const count = props.filmworkCount || 0;
  const word = getFilmworkWord(count);
  return `Участвовал(а) в ${count} фильмах${word}`;
});

const getFilmworkWord = (count: number): string => {
  if (count % 100 >= 11 && count % 100 <= 19) {
    return "ах";
  }
  switch (count % 10) {
    case 1:
      return "е";
    case 2:
    case 3:
    case 4:
      return "ах";
    default:
      return "ах";
  }
};

const getRoleClass = (role: string) => {
  const roleLower = role.toLowerCase();
  if (roleLower.includes("actor") || roleLower.includes("актер")) {
    return "role-actor";
  } else if (roleLower.includes("director") || roleLower.includes("режиссер")) {
    return "role-director";
  } else if (roleLower.includes("writer") || roleLower.includes("сценарист")) {
    return "role-writer";
  } else if (roleLower.includes("producer") || roleLower.includes("продюсер")) {
    return "role-producer";
  }
  return "role-other";
};

const getRoleDisplayName = (role: string) => {
  const roleLower = role.toLowerCase();
  if (roleLower.includes("actor") || roleLower.includes("актер")) {
    return "Актер";
  } else if (roleLower.includes("director") || roleLower.includes("режиссер")) {
    return "Режиссер";
  } else if (roleLower.includes("writer") || roleLower.includes("сценарист")) {
    return "Сценарист";
  } else if (roleLower.includes("producer") || roleLower.includes("продюсер")) {
    return "Продюсер";
  }
  return role;
};

const handleClick = () => {
  if (props.clickable) {
    emit("click", props.id);
  }
};
</script>

<style scoped>
.person-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.person-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgb(0 0 0 / 10%);
}

.person-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.avatar-placeholder {
  font-size: 28px;
  color: #999;
  font-weight: bold;
}

.person-info {
  text-align: center;
}

.person-name {
  margin: 0 0 10px;
  font-size: 1.1em;
  font-weight: 600;
  color: #333;
}

.person-roles {
  display: flex;
  justify-content: center;
  gap: 5px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.role-tag {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75em;
  font-weight: 500;
}

.role-actor {
  background: #e8f5e9;
  color: #2e7d32;
}

.role-director {
  background: #e3f2fd;
  color: #1565c0;
}

.role-writer {
  background: #fff3e0;
  color: #ef6c00;
}

.role-producer {
  background: #f3e5f5;
  color: #7b1fa2;
}

.role-other {
  background: #eceff1;
  color: #546e7a;
}

.role-more {
  color: #666;
  font-size: 0.75em;
  display: flex;
  align-items: center;
}

.person-filmworks {
  color: #666;
  font-size: 0.85em;
}

@media (width <= 768px) {
  .person-avatar {
    width: 60px;
    height: 60px;
  }

  .avatar-placeholder {
    font-size: 22px;
  }

  .person-name {
    font-size: 1em;
  }
}
</style>
