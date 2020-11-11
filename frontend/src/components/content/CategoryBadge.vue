<template>
  <div class="v-category-badge" :class="{ active: !!active }" ref="root">
    <button @click="activateHandler" @blur="cancelHandler($event)">
      <h6 v-html="processText(category.title)"></h6>
    </button>
    <button @click="removeHandler" @blur="cancelHandler($event)">
      <span class="icon-close"></span>
    </button>
  </div>
</template>

<script>
import { processValue } from "./../TextEditor.vue";

export default {
  name: "CategoryBadge",

  props: {
    category: Object,
    search: String
  },

  data() {
    return {
      active: false
    };
  },

  methods: {
    processText(text) {
      return processValue(text, this.search);
    },

    activateHandler() {
      this.active = !this.active;
    },

    removeHandler() {
      this.$emit("remove", this.category.id);
    },

    cancelHandler(event) {
      if (!this.$refs.root.contains(event.relatedTarget)) {
        this.active = false;
      }
    }
  }
};
</script>

<style lang="sass" scoped>
.v-category-badge
  overflow: hidden
  display: flex
  flex-flow: row nowrap
  justify-content: stretch
  align-items: center
  border-radius: $step*2
  color: $color-tertiary

  &>button:nth-of-type(1)
    padding: 1px $step*0.5 0

    &:hover
      text-decoration: underline

  &>button:nth-of-type(2)
    display: none
    padding: 2px 0 0

    &:hover
      background-color: $color-tertiary
      color: $color-white

  &.active
    border: 1px solid $color-tertiary

    &>button:nth-of-type(1):hover
      text-decoration: none

    &>button:nth-of-type(2)
      display: block
</style>
