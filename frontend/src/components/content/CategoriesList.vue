<template>
  <div class="content-categories-list">
    <template v-if="search">
      <v-drag-and-drop
        v-for="item in searchedItems"
        :key="item.id"
        :detail="{ type: 'category', id: item.id }"
        @drop.native="
          dropHandler($event.detail.type, item.id, $event.detail.id)
        "
      >
        <div
          class="item"
          :class="{ active: selected.id === item.id }"
          @click="$emit('select', item.category)"
        >
          <div>
            <sub>{{ item.path }}</sub>
            <h5 v-if="item.category.title">{{ item.category.title }}</h5>
          </div>
        </div>
      </v-drag-and-drop>
    </template>

    <template v-else>
      <v-drag-and-drop
        v-for="item in unaffectedItems"
        :key="item.id"
        :detail="{ type: 'category', id: item.id }"
        @drop.native="
          dropHandler($event.detail.type, item.id, $event.detail.id)
        "
      >
        <div
          class="item"
          :class="{
            hidden: isCollapsed(item.category.parent),
            active: selected.id === item.id
          }"
          @click="$emit('select', item.category)"
        >
          <span
            class="item-padding"
            v-for="level in item.level"
            :key="'level' + level"
          ></span>

          <button @click.stop="collapseHandler(item.id)">
            <span
              v-if="!children[item.id]"
              class="icon-arrow-right disabled"
            ></span>
            <span
              v-else-if="!collapsed[item.id]"
              class="icon-arrow-drop-down"
            ></span>
            <span v-else class="icon-arrow-right"></span>
          </button>

          <div>
            <h5 v-if="item.category.title">{{ item.category.title }}</h5>
          </div>
        </div>
      </v-drag-and-drop>
    </template>
  </div>
</template>

<script>
import Vue from "vue";
import DragAndDrop from "./../DragAndDrop.vue";

export default {
  name: "CategoriesList",

  components: {
    "v-drag-and-drop": DragAndDrop
  },

  props: {
    selected: {
      type: Object,
      default: () => ({})
    },
    search: String
  },

  data() {
    return {
      collapsed: {}
    };
  },

  computed: {
    children() {
      const $category = this.$store.state.category;

      var result = {};

      for (const id in $category) {
        const parent = $category[id].parent;

        if (!result[parent]) {
          result[parent] = [];
        }
        result[parent].push(id);
      }

      return result;
    },

    unaffectedItems() {
      const $category = this.$store.state.category;

      var children = this.children,
        result = [];

      const arrange = (parent, level, path) => {
        if (parent) {
          path += $category[parent].title + " / ";
        } else {
          path = "/ ";
        }

        if (children[parent]) {
          for (const id of children[parent]) {
            result.push({
              id,
              level,
              path,
              category: $category[id]
            });

            if (children[id]) {
              arrange(id, level + 1, path);
            }
          }
        }
      };
      arrange(undefined, 0, "");

      return result;
    },

    searchedItems() {
      const search = this.search,
        $category = this.$store.state.category;

      var result = [];

      for (const id in $category) {
        const category = $category[id];

        const strings = [category.title, category.text];

        if (this.match(search, strings)) {
          var parent = $category[category.parent],
            path = [];

          while (parent) {
            path.push(parent.title);
            parent = $category[parent.parent];
          }

          path = "/ " + path.reverse().join(" / ");

          result.push({
            id,
            path,
            category
          });
        }
      }

      return result;
    }
  },

  methods: {
    match(pattern, strings) {
      pattern = pattern.toLowerCase();

      for (const string of strings) {
        if (string.toLowerCase().indexOf(pattern) !== -1) {
          return true;
        }
      }
      return false;
    },

    isCollapsed(id) {
      const $category = this.$store.state.category;

      while (id) {
        if (this.collapsed[id] === true) {
          return true;
        }
        id = $category[id].parent;
      }
      return false;
    },

    collapseHandler(id) {
      Vue.set(this.collapsed, id, !this.collapsed[id]);
    },

    dropHandler(type, parent, child) {
      if (type === "category") {
        const $category = this.$store.state.category;

        var check = parent;

        while (check) {
          if (check === child) {
            break;
          }
          check = $category[check].parent;
        }

        if (!check) {
          if (parent === $category[child].parent) {
            parent = $category[parent].parent;
          }

          this.$store.dispatch("setModelItem", {
            model: "category",
            id: child,
            item: {
              parent: parent
            }
          });
        }
      }
    }
  }
};
</script>

<style lang="sass" scoped>
.content-categories-list
  display: flex
  flex-flow: column
  justify-content: start
  align-items: stretch

  &>.v-drag-and-drop
    flex: 0 0 auto
    overflow: hidden
    padding-left: $step*2

    .item
      display: flex
      flex-flow: row nowrap
      justify-content: stretch
      align-items: center
      background-color: $color-white

      &>*
        flex: 0 0 auto
        padding: $step*0.5 0

      &>.item-padding
        padding-left: $step*3

      &>button
        font-size: $step*3
        color: $color-dark

        &>.disabled
          color: alpha($color-dark, '88')

      &>div
        flex: 1 1 auto
        padding-right: $step

        &>h5
          color: $color-dark

  .v-drag-and-drop .item.active, .v-drag-and-drop .item:hover
    background-color: $color-gray

  .v-drag-and-drop .item.hidden
    display: none
</style>
