<template>
  <div class="dialog">
    <div>
      <h5>{{ title }}</h5>
    </div>

    <div>
      <div>
        <p>{{ text }}</p>
      </div>

      <div>
        <button
          v-for="(button, index) in buttons"
          :key="'button' + index"
          @click="clickHandler(button.handler)"
        >
          {{ button.title }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dialog",

  props: {
    title: {
      type: String,
      default: ""
    },

    text: {
      type: String,
      default: ""
    },

    buttons: {
      type: Array,
      default: () => []
    }
  },

  methods: {
    clickHandler(handler) {
      if (handler instanceof Function) {
        handler();
      }
      this.$emit("close");
    }
  }
};
</script>

<style lang="sass" scoped>
.dialog
  border-radius: $step
  border: $step solid $color-primary
  background-color: $color-primary
  color: $color-white

  &.hidden
    display: none

  &>div:nth-of-type(1)
    padding: 0 $step*0.5 $step*0.5

  &>div:nth-of-type(2)
    border-radius: $step
    background-color: $color-white
    color: $color-primary

    &>div:nth-of-type(1)
      min-height: 5rem
      overflow: hidden
      display: flex
      flex-flow: column
      align-items: center
      justify-content: center
      padding: $step $step*2

      &>*
        flex: 0 0 auto

    &>div:nth-of-type(2)
      display: flex
      flex-flow: row
      padding: 0 $step $step

      &>button
        flex: 0 1 6rem
        padding: $step $step*2
        margin-left: $step
        border-radius: $step
        border: 2px solid $color-primary

        &:hover
          border: 2px solid $color-dark
          background-color: $color-dark
          color: $color-white

      &>*:first-child
        margin-left: auto
</style>
