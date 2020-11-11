<template>
  <div class="bookmark">
    <div>
      <slot></slot>
    </div>

    <div>
      <svg viewBox="0 0 375 182" preserveAspectRatio="xMidYMin slice">
        <path
          d="M190.5 182L375 71.0185V36.6742L190.5 147.326L0 36.6742V71.0185L190.5 182Z"
        />
        <path d="M190.5 112.652L375 2V0L-3.05176e-05 0L0 2L190.5 112.652Z" />
      </svg>
    </div>
  </div>
</template>

<script>
export default {
  name: "Bookmark"
};
</script>

<style lang="sass" scoped>
// There are several fixes for compatibility with IE:
// 1. Svg tag must have preserveAspectRatio="xMidYMin slice" attribute
// 2. Svg tag must have a container
// 3. Svg tag must have 1% height, 100% width, visible overflow,
//    margin-bottom set to some % value

.bookmark
  width: 100%
  display: flex
  flex-flow: column

  &>div:nth-of-type(1)
    flex: 1 0 auto
    overflow: hidden
    padding: $step*2
    background-color: $color-primary
    color: $color-white
    text-align: center

  &>div:nth-of-type(2)
    width: 100%
    flex: 0 0 auto
    margin-top: -1px
    svg
      height: 1%
      width: 100%
      overflow: visible
      margin-bottom: 5%
      fill: $color-primary
</style>
