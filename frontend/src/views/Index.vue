<template>
  <section id="index-page">
    <section id="index-page-main">
      <v-bookmark>
        <object
          id="index-page-logo"
          type="image/svg+xml"
          :data="require('@/assets/Logo.white.svg')"
          tabindex="-1"
        >
          <img :src="require('@/assets/Logo.white.svg')" alt="Logo" />
        </object>
        <h2>SmartNotes</h2>
        <p>
          Make your life easier with a couple of notes. SmartNotes will helps
          you to keep everyday routine in order.
        </p>
        <button
          :class="{ active: authorizationType === 'login' }"
          @click="(authorizationType = 'login'), $event.target.blur()"
        >
          Login
        </button>
        <button
          :class="{ active: authorizationType === 'register' }"
          @click="(authorizationType = 'register'), $event.target.blur()"
        >
          Register
        </button>
      </v-bookmark>
    </section>

    <section id="index-page-sidebar">
      <v-bookmark>
        <div id="index-page-spacer"></div>
      </v-bookmark>
      <v-authorization :type="authorizationType"></v-authorization>
    </section>

    <section id="index-page-footer">
      <p>Go to <a>mobile version.</a></p>
    </section>
  </section>
</template>

<script>
import Bookmark from "./../components/Bookmark.vue";
import Authorization from "./../components/Authorization.vue";

export default {
  name: "Index",

  components: {
    "v-bookmark": Bookmark,
    "v-authorization": Authorization
  },

  data() {
    return {
      authorizationType: "login"
    };
  }
};
</script>

<style lang="sass" scoped>
$section-min-width: 360px
$sidebar-max-width: 768px
$bookmark-width: $section-min-width - $step

//-----------------------------------------------------------------------------
// Main frame
#index-page
  flex: 1 1 $desktop-min-width
  position: relative
  width: 100%
  min-height: 100vh
  display: flex
  flex-flow: row nowrap
  background: top/cover url("~@/assets/Background.svg")

#index-page-main
  flex: 1 0 $section-min-width
  padding-bottom: 20vh

#index-page-sidebar
  flex: 0 0 30%
  min-width: $section-min-width
  max-width: $sidebar-max-width
  border-left: $step solid $color-primary
  background: bottom/80% auto url("~@/assets/Ink_background.svg") no-repeat, $color-white


//-----------------------------------------------------------------------------
// Bookmark
.bookmark
  width: $bookmark-width
  margin: 0 auto

//-----------------------------------------------------------------------------
// Sidebar
#index-page-sidebar
  #index-page-spacer
    height: 2rem

  .authorization
    width: 85%
    margin: 0 auto

//-----------------------------------------------------------------------------
// Main
#index-page-main
  .bookmark
    #index-page-logo
      margin: 2rem 0 0
      width: $bookmark-width * 0.5
      height: $bookmark-width * 0.5 / 1.6

    p
      margin: 2rem 0 4rem

    button
      display: block
      width: 70%
      height: $step*5
      margin: 1rem auto 0
      border-radius: $step
      border: 1px solid $color-white

      &.active
        background-color: $color-white
        color: $color-primary

      @media (hover: hover), (-ms-high-contrast:none)
        &:hover, &:focus
          background-color: $color-dark !important
          color: $color-white !important

//-----------------------------------------------------------------------------
// Footer
#index-page-footer
  position: absolute
  left: $step*2
  bottom: $step*2
  color: $color-dark
</style>
