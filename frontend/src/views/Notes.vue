<template>
  <section id="view-notes">
    <div id="view-notes-list">
      <v-list-frame id="view-notes-list-items">
        <div class="header">
          <div class="title">
            <h5>Notes</h5>
            <v-icon-button
              icon="icon-filter"
              :class="{ active: filtersMenu }"
              @click="filtersMenu = !filtersMenu"
            ></v-icon-button>
            <v-icon-button
              icon="icon-settings"
              :class="{ active: settingsMenu }"
              @click="$emit('show-settings-menu', !settingsMenu)"
            ></v-icon-button>
          </div>

          <v-search v-model="search"></v-search>
        </div>

        <v-notes-list
          :search="search"
          :filters="filters"
          :selected="note"
          class="content"
          @select="selectNoteHandler($event)"
        ></v-notes-list>
      </v-list-frame>

      <v-list-frame
        id="view-notes-list-filters"
        :class="{ hidden: !filtersMenu }"
      >
        <div class="header">
          <div class="title">
            <h5>Filters</h5>
            <v-icon-button
              icon="icon-close"
              @click="filtersMenu = false"
            ></v-icon-button>
          </div>
        </div>

        <v-filters-list :filters="filters" class="content"></v-filters-list>
      </v-list-frame>
    </div>

    <v-note-editor
      :search="search"
      id="view-notes-content"
      :item="note"
      @action="actionHandler"
      @show-dialog="$emit('show-dialog', $event)"
    ></v-note-editor>
  </section>
</template>

<script>
import IconButton from "./../components/IconButton.vue";
import Search from "./../components/Search.vue";
import NotesList from "./../components/content/NotesList.vue";
import FiltersList from "./../components/content/FiltersList.vue";
import NoteEditor from "./../components/content/NoteEditor.vue";
import { decodeModelItem } from "./../store/model.js";
import ListFrame from "./../components/ListFrame.vue";

export default {
  name: "Notes",

  components: {
    "v-icon-button": IconButton,
    "v-search": Search,
    "v-notes-list": NotesList,
    "v-filters-list": FiltersList,
    "v-note-editor": NoteEditor,
    "v-list-frame": ListFrame
  },

  props: {
    settingsMenu: Boolean
  },

  data() {
    return {
      filtersMenu: false,
      search: "",
      filters: [],
      note: this.makeNote()
    };
  },

  methods: {
    makeNote() {
      return decodeModelItem("note", this.$store.getters.newId());
    },

    actionHandler(action) {
      const deleteNoteHandler = () => {
        this.$store.dispatch("deleteModelItem", {
          model: "note",
          id: this.note.id
        });

        this.note = this.makeNote();
      };

      if (action === "add") {
        this.note = this.makeNote();
      } else if (action === "delete") {
        this.$emit("show-dialog", {
          title: "Warning",
          text:
            'You want to delete "' +
            (this.note.title || "untitled") +
            '" note. Are you sure?',
          buttons: [
            { title: "Delete", handler: deleteNoteHandler },
            { title: "Close", handler: undefined }
          ]
        });
      }
    },

    selectNoteHandler(note) {
      this.note = note;
    }
  },

  mounted() {
    this.$store.subscribe((mutation, state) => {
      if (
        mutation.type === "setModelItem" &&
        mutation.payload.model === "note" &&
        mutation.payload.id === this.note.id
      ) {
        this.note = state.note[this.note.id];
      }

      if (
        mutation.type === "deleteModelItem" &&
        mutation.payload.model === "note" &&
        mutation.payload.id === this.note.id
      ) {
        this.note = this.makeNote();
      }
    });
  }
};
</script>

<style lang="sass" scoped>
$list-section-min-width: 376px

//-----------------------------------------------------------------------------
// Main frame
#view-notes
  width: 100%
  display: flex
  flex-flow: row nowrap
  align-items: stretch
  justify-content: stretch

#view-notes-list
  flex: 1 0 $list-section-min-width
  display: flex
  flex-flow: column
  align-items: stretch
  justify-content: stretch
  border-right: $step solid $color-primary

#view-notes-list-items, #view-notes-list-filters
  flex: 1 1 auto
  min-height: 50vh

#view-notes-list-filters
  border-top: $step solid $color-primary

#view-notes-content
  flex: 1 1 70%

//-----------------------------------------------------------------------------
// Filters customization
#view-notes-list-filters
  &.hidden
    display: none

  &.v-list-frame>.header
    padding: $step*0.5 $step*0.5 $step*0.5 0
</style>
