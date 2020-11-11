<template>
  <div class="v-list-frame">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "ListFrame"
};
</script>

<style lang="sass" scoped>
//-----------------------------------------------------------------------------
// List appearance
.v-list-frame
  display: flex
  flex-flow: column
  align-items: stretch
  justify-content: stretch

  &>*
    display: flex
    flex-flow: column
    align-items: stretch
    justify-content: stretch

  &>.header
    flex: 0 0 auto
    margin-left: $step*2
    border-bottom: 1px solid $color-primary
    padding: $step $step $step 0

    &>* + *
      margin-top: $step*0.5

    &>.title
      display: flex
      flex-flow: row nowrap
      align-items: center

      &>.icon-button:nth-of-type(1)
        margin-left: auto

      &>.icon-button + .icon-button
        margin-left: $step*0.5

  &>.content
    flex: 1 1 auto
    overflow-x: hidden
    overflow-y: auto
</style>
