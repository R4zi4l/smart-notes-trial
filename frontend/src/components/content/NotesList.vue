<template>
  <div class="content-notes-list">
    <div
      v-for="(item, id) in items"
      :key="id"
      class="item"
      :class="{ active: selected.id === id }"
      @click="$emit('select', item)"
    >
      <div>
        <h5>{{ item.title }}</h5>
        <div v-if="categoriesLength(categories[id])" class="categories">
          <button v-for="category in categories[id]" :key="category.id + id">
            <h6>{{ category.title }}</h6>
          </button>
        </div>
        <p>{{ item.text }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import {
  getEntityFromCategoryEntityId,
  getCategoryFromCategoryEntityId
} from "./../../store/model.js";

export default {
  name: "NotesList",

  props: {
    selected: {
      type: Object,
      default: () => ({})
    },
    search: String,
    filters: Array
  },

  computed: {
    items() {
      const search = this.search,
        $note = this.$store.state.note;

      var notes = {},
        result = {};

      if (this.filters) {
        for (const id in $note) {
          const note = $note[id];

          if (this.filters.every(filter => filter.handler(id))) {
            notes[id] = note;
          }
        }
      } else {
        notes = $note;
      }

      if (search) {
        for (const id in notes) {
          const note = notes[id];

          const strings = [
            note.title,
            note.text,
            ...Array.from(
              Object.values(this.categories[id] || {}),
              category => category.title
            )
          ];

          if (this.match(search, strings)) {
            result[id] = note;
          }
        }
      } else {
        result = notes;
      }

      return result;
    },

    categories() {
      const $note = this.$store.state.note,
        $category = this.$store.state.category,
        $categoryentity = this.$store.state.categoryentity;

      var result = {};

      for (const id in $categoryentity) {
        const entity = getEntityFromCategoryEntityId(id),
          category = getCategoryFromCategoryEntityId(id);

        if (entity in $note) {
          if (!result[entity]) {
            result[entity] = {};
          }
          result[entity][category] = $category[category];
        }
      }
      return result;
    }
  },

  methods: {
    categoriesLength(categories) {
      return Object.getOwnPropertyNames(categories || {}).length;
    },

    match(pattern, strings) {
      pattern = pattern.toLowerCase();

      for (const string of strings) {
        if (string.toLowerCase().indexOf(pattern) !== -1) {
          return true;
        }
      }
      return false;
    }
  }
};
</script>

<style lang="sass" scoped>
.content-notes-list
  display: flex
  flex-flow: column
  justify-content: start
  align-items: stretch

  &>.item
    flex: 0 0 auto
    overflow: hidden
    padding-left: $step*2

    &>div
      display: flex
      flex-flow: column
      padding: $step*2 $step $step 0

      &>* + *
        margin-top: $step*0.5

      &>h5
        color: $color-dark

      &>.categories
        display: flex
        flex-flow: row wrap
        align-items: center
        justify-content: start

        &>button
          color: $color-tertiary

        &>button + button
          margin-left: $step

        &>button:hover
          text-decoration: underline

      &>p
        max-height: 2.4rem
        overflow: hidden

        // Keep this part as an example
        // &:after
        //   content: ""
        //   text-align: right
        //   position: absolute
        //   top: 1.2rem
        //   right: 0
        //   width: 70%
        //   height: 1.2rem
        //   background: linear-gradient(to right, alpha($color-white, "00"), alpha($color-white, "CC") 50%)

  &>.item + .item>div
    border-top: 1px solid alpha($color-primary, "88")

  &>.item.active, &>.item:hover
    background-color: $color-gray
</style>
