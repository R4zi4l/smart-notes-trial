<template>
  <div class="content-filters-list">
    <template v-for="group in groups">
      <div :key="'group-' + group.id" class="group" @click="toggleGorup(group)">
        <div>
          <h5>{{ group.title }}</h5>
          <span
            class="icon-arrow-drop-up"
            :class="{ hidden: !collapsed[group.id] }"
          ></span>
          <span
            class="icon-arrow-drop-down"
            :class="{ hidden: collapsed[group.id] }"
          ></span>
        </div>
      </div>

      <div
        v-for="item in group.items"
        :key="group.id + item.id"
        class="item"
        :class="{
          hidden: collapsed[group.id],
          active: isItemActive(group, item)
        }"
        @click="toggleItem(group, item)"
      >
        <div>
          <span>{{ item.title }}</span>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import Vue from "vue";
import { makeCategoryEntityId } from "./../../store/model.js";

export default {
  name: "FiltersList",

  props: {
    // Filters structure:
    // [
    //   {
    //     group: String,
    //     item: String
    //     title: String,
    //     handler: Function
    //   }
    // ]
    filters: {
      type: Array,
      default: () => []
    }
  },

  data() {
    return {
      collapsed: {}
    };
  },

  computed: {
    actives() {
      var result = [];

      for (let i = 0; i < this.filters.length; ++i) {
        const filter = this.filters[i];

        result.push({
          id: i + "-" + filter.item,
          title: filter.title,
          text: ""
        });
      }

      Vue.set(this.collapsed, "acvtive", false);
      return result;
    },

    categories() {
      const $category = this.$store.state.category;
      var result = [];

      const categoryFullTitle = category => {
        return category.parent
          ? categoryFullTitle($category[category.parent]) +
              " / " +
              category.title
          : category.title;
      };

      for (const id in $category) {
        const item = $category[id];

        result.push({
          id: id,
          title: categoryFullTitle(item),
          text: item.text
        });
      }

      Vue.set(this.collapsed, "category", false);
      return result;
    },

    groups() {
      var result = [];

      if (this.actives.length) {
        result.push({
          id: "active",
          title: "Active",
          items: this.actives
        });
      }

      if (this.categories.length) {
        result.push({
          id: "category",
          title: "Category",
          items: this.categories
        });
      }

      return result;
    }
  },

  methods: {
    isItemActive(group, item) {
      return (
        group.id === "active" ||
        this.filters.findIndex(filter => {
          return filter.group === group.id && filter.item === item.id;
        }) !== -1
      );
    },

    toggleGorup(group) {
      Vue.set(this.collapsed, group.id, !this.collapsed[group.id]);
    },

    toggleItem(group, item) {
      if (group.id === "active") {
        const index = this.filters.findIndex((element, i) => {
          return i + "-" + element.item === item.id;
        });

        if (index !== -1) {
          Vue.delete(this.filters, index);
        }
      } else if (group.id === "category") {
        const index = this.filters.findIndex(element => {
          return element.group === group.id && element.item === item.id;
        });

        if (index !== -1) {
          Vue.delete(this.filters, index);
        } else {
          Vue.set(this.filters, this.filters.length, {
            group: group.id,
            item: item.id,
            title: item.title,
            handler: id => {
              return !!this.$store.state.categoryentity[
                makeCategoryEntityId(item.id, id)
              ];
            }
          });
        }
      }
    }
  }
};
</script>

<style lang="sass" scoped>
.content-filters-list
  display: flex
  flex-flow: column
  justify-content: start
  align-items: stretch

  &>.group, &>.item
    flex: 0 0 auto
    overflow: hidden
    padding-left: $step*2

    &:hover
      background-color: $color-gray

  &>.group>div
    display: flex
    flex-flow: row nowrap
    align-items: center
    justify-content: start
    margin-top: $step*2
    color: $color-dark
    border-bottom: 1px solid alpha($color-dark, '88')

    &>span
      margin-left: auto
      font-size: $step*4 - $step
      line-height: $step*4 - $step

      &.hidden
        display: none

  &>.item>div
    margin: $step*0.5 0 0 $step*0.5

  &>.item.active>div
    font-weight: bold

  &>.item.hidden
    display: none
</style>
