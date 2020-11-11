<template>
  <div class="search">
    <input
      type="text"
      placeholder="Search..."
      ref="search"
      :value="value"
      @input="$emit('input', $event.target.value)"
    />
    <button :class="{ hidden: value }" @click="$refs.search.focus()">
      <span class="icon-search"></span>
    </button>
    <button
      :class="{ hidden: !value }"
      @click="$emit('input', ''), $refs.search.focus()"
    >
      <span class="icon-close"></span>
    </button>
  </div>
</template>

<script>
export default {
  name: "Search",

  props: {
    value: String
  }
};
</script>

<style lang="sass" scoped>
.search
  display: flex
  flex-flow: row nowrap

  &>input
    width: 100%
    padding: 0 $step
    background-color: $color-gray
    border-top-left-radius: $step
    border-bottom-left-radius: $step
    color: $color-dark

    &::-ms-clear
      display: none

  &>button
    padding: $step*0.5 $step
    margin-left: -1px
    background-color: $color-gray
    border-top-right-radius: $step
    border-bottom-right-radius: $step
    font-size: $step*4 - $step
    line-height: $step*4 - $step

  &>button:hover
    background-color: $color-primary
    color: $color-white

  &>button.hidden
    display: none
</style>
