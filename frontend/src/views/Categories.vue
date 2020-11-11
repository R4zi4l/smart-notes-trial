<template>
  <section id="view-categories">
    <v-list-frame id="view-categories-list">
      <div class="header">
        <div class="title">
          <h5>Categories</h5>
          <v-icon-button
            icon="icon-settings"
            :class="{ active: settingsMenu }"
            @click="$emit('show-settings-menu', !settingsMenu)"
          ></v-icon-button>
        </div>

        <v-search v-model="search"></v-search>
      </div>

      <v-categories-list
        :search="search"
        :selected="category"
        class="content"
        @select="selectCategoryHandler($event)"
      ></v-categories-list>
    </v-list-frame>

    <v-category-editor
      :search="search"
      id="view-categories-content"
      :item="category"
      @action="actionHandler"
    ></v-category-editor>
  </section>
</template>

<script>
import IconButton from "./../components/IconButton.vue";
import Search from "./../components/Search.vue";
import CategoriesList from "./../components/content/CategoriesList.vue";
import CategoryEditor from "./../components/content/CategoryEditor.vue";
import { decodeModelItem } from "./../store/model.js";
import ListFrame from "./../components/ListFrame.vue";

export default {
  name: "Categories",

  components: {
    "v-icon-button": IconButton,
    "v-search": Search,
    "v-categories-list": CategoriesList,
    "v-category-editor": CategoryEditor,
    "v-list-frame": ListFrame
  },

  props: {
    settingsMenu: Boolean
  },

  data() {
    return {
      search: "",
      category: this.makeCategory()
    };
  },

  methods: {
    makeCategory() {
      return decodeModelItem("category", this.$store.getters.newId());
    },

    actionHandler(action) {
      const deleteCategoryHandler = () => {
        this.$store.dispatch("deleteModelItem", {
          model: "category",
          id: this.category.id
        });

        this.category = this.makeCategory();
      };

      if (action === "add") {
        this.category = this.makeCategory();
      } else if (action === "delete") {
        this.$emit("show-dialog", {
          title: "Warning",
          text:
            'You want to delete "' +
            (this.category.title || "untitled") +
            '" category. All dependent categories will also be removed. Are you sure?',
          buttons: [
            { title: "Delete", handler: deleteCategoryHandler },
            { title: "Close", handler: undefined }
          ]
        });
      }
    },

    selectCategoryHandler(category) {
      this.category = category;
    }
  },

  mounted() {
    this.$store.subscribe((mutation, state) => {
      if (
        mutation.type === "setModelItem" &&
        mutation.payload.model === "category" &&
        mutation.payload.id === this.category.id
      ) {
        this.category = state.category[this.category.id];
      }

      if (
        mutation.type === "deleteModelItem" &&
        mutation.payload.model === "category" &&
        mutation.payload.id === this.category.id
      ) {
        this.category = this.makeCategory();
      }
    });
  }
};
</script>

<style lang="sass" scoped>
$list-section-min-width: 376px

//-----------------------------------------------------------------------------
// Main frame
#view-categories
  width: 100%
  display: flex
  flex-flow: row nowrap
  align-items: stretch
  justify-content: stretch

#view-categories-list
  flex: 1 0 $list-section-min-width
  display: flex
  flex-flow: column
  align-items: stretch
  justify-content: stretch
  border-right: $step solid $color-primary

#view-categories-content
  flex: 1 1 70%
</style>
