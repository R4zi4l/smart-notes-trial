<template>
  <section id="view-desktop">
    <div id="view-desktop-navigation">
      <div class="logo">
        <object
          type="image/svg+xml"
          :data="require('@/assets/Logo.white.svg')"
          tabindex="-1"
        >
          <img :src="require('@/assets/Logo.white.svg')" alt="Logo" />
        </object>
        <h4>SmartNotes</h4>
      </div>
      <button
        :class="{ active: $route.name === 'account' }"
        @click="$router.push('account').catch(() => {})"
      >
        <h5>{{ username }}</h5>
      </button>
      <button
        :class="{ active: $route.name === 'notes' }"
        @click="$router.push('notes').catch(() => {})"
      >
        <h5>Notes</h5>
      </button>
      <button
        :class="{ active: $route.name === 'categories' }"
        @click="$router.push('categories').catch(() => {})"
      >
        <h5>Categories</h5>
      </button>
      <button
        :class="{ active: $route.name === 'settings' }"
        @click="$router.push('settings').catch(() => {})"
      >
        <h5>Settings</h5>
      </button>
    </div>

    <router-view
      @show-settings-menu="showSettingsMenuHandler"
      :settingsMenu="settingsMenu"
      @show-dialog="showDialogHandler"
    ></router-view>

    <v-list-frame
      id="view-desktop-settings"
      class="view-desktop-list"
      :class="{ hidden: !settingsMenu }"
    >
      <div class="header">
        <div class="title">
          <h5>Settings</h5>
          <v-icon-button
            icon="icon-close"
            @click="settingsMenu = false"
          ></v-icon-button>
        </div>

        <v-search></v-search>
      </div>

      <div class="content"></div>
    </v-list-frame>

    <div id="view-desktop-dialogs" :class="{ hidden: !dialogs.length }">
      <v-dialog
        v-for="(dialog, index) in dialogs"
        :key="'dialog' + index"
        :title="dialog.title"
        :text="dialog.text"
        :buttons="dialog.buttons"
        @close="closeDialogHandler(dialog)"
      ></v-dialog>
    </div>
  </section>
</template>

<script>
import IconButton from "./../components/IconButton.vue";
import Search from "./../components/Search.vue";
import Dialog from "./../components/Dialog.vue";
import ListFrame from "./../components/ListFrame.vue";

export default {
  name: "Desktop",

  components: {
    "v-icon-button": IconButton,
    "v-search": Search,
    "v-dialog": Dialog,
    "v-list-frame": ListFrame
  },

  data() {
    return {
      settingsMenu: false,
      dialogs: []
    };
  },

  computed: {
    username() {
      return this.$store.state.user?.username || "Jhon Doe";
    }
  },

  methods: {
    showSettingsMenuHandler(visible) {
      this.settingsMenu = visible;
    },

    showDialogHandler(dialog) {
      this.dialogs.push(dialog);
    },

    closeDialogHandler(dialog) {
      const index = this.dialogs.indexOf(dialog);

      if (index !== -1) {
        this.dialogs.splice(index, 1);
      }
    }
  }
};
</script>

<style lang="sass" scoped>
//-----------------------------------------------------------------------------
// Main frame
#view-desktop
  min-width: $desktop-min-width
  width: 100%
  height: 100vh
  position: relative
  display: flex
  flex-flow: row
  align-items: stretch

#view-desktop-navigation
  flex: 0 0 auto
  overflow-x: hidden
  overflow-y: auto
  display: flex
  flex-flow: column
  padding: $step*2
  background-color: $color-primary
  color: $color-white

  &>*
    flex: 0 0 auto
    padding: $step*2 0

  &>* + *
    border-top: 1px solid $color-white

  &>.logo
    padding-top: 0
    white-space: nowrap

    &>*
      display: inline-block

    object
      vertical-align: bottom
      width: 3rem
      margin-right: $step

  &>*.active
    color: $color-primary
    background-color: $color-white

  &>button:hover
    color: $color-white
    background-color: $color-dark

//-----------------------------------------------------------------------------
// Settings
#view-desktop-settings
  position: absolute
  top: 0
  right: 0
  height: 100%
  width: 50vw
  z-index: 100
  border-left: $step solid $color-primary
  background-color: $color-white

#view-desktop-dialogs
  position: absolute
  top: 0
  right: 0
  height: 100%
  width: 100%
  z-index: 200
  overflow: auto
  display: flex
  flex-flow: column
  align-items: center
  justify-content: center
  background-color: alpha($color-primary, '66')

//-----------------------------------------------------------------------------
// Settings customization
#view-desktop-settings
  &.hidden
    display: none

//-----------------------------------------------------------------------------
// Dialogs customization
#view-desktop-dialogs
  &.hidden
    display: none
</style>
