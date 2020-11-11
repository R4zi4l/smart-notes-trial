<template>
  <button class="icon-button" @click="$emit('click', $event)">
    <span :class="icon"></span>
  </button>
</template>

<script>
export default {
  name: "IconButton",

  props: {
    icon: String
  }
};
</script>

<style lang="sass" scoped>
.icon-button
  color: $color-primary
  width: $step*4
  height: $step*4
  border-radius: $step
  padding: $step*0.5
  font-size: $step*4 - $step
  line-height: $step*4 - $step

  &.active
    background-color: $color-primary
    color: $color-white

  &:hover
    background-color: $color-dark
    color: $color-white
</style>
