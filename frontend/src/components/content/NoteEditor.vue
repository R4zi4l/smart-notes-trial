<template>
  <div class="content-note-editor">
    <div class="header">
      <v-icon-button
        icon="icon-add"
        @click="$emit('action', 'add')"
      ></v-icon-button>
      <v-icon-button
        icon="icon-delete"
        @click="$emit('action', 'delete')"
      ></v-icon-button>
    </div>

    <div class="content">
      <v-text-editor
        class="title"
        :value="item.title"
        :search="search"
        placeholder="Note title"
        :multiline="false"
        @input="titleInput($event)"
      ></v-text-editor>

      <div class="category">
        <v-category-badge
          v-for="category in categories"
          :key="category.id"
          :category="category"
          :search="search"
          @remove="removeCategoryHandler"
        ></v-category-badge>
        <v-category-input
          @create="createCategoryHandler"
          @select="selectCategoryHandler"
        ></v-category-input>
      </div>

      <v-text-editor
        class="text"
        :value="item.text"
        :search="search"
        placeholder="Note text"
        @input="textInput($event)"
      ></v-text-editor>
    </div>
  </div>
</template>

<script>
import IconButton from "./../IconButton.vue";
import {
  getEntityFromCategoryEntityId,
  getCategoryFromCategoryEntityId,
  makeCategoryEntityId
} from "./../../store/model.js";
import TextEditor from "./../TextEditor.vue";
import CategoryInput from "./CategoryInput.vue";
import { decodeModelItem } from "./../../store/model.js";
import CategoryBadge from "./CategoryBadge.vue";

export default {
  name: "NoteEditor",

  components: {
    "v-icon-button": IconButton,
    "v-text-editor": TextEditor,
    "v-category-input": CategoryInput,
    "v-category-badge": CategoryBadge
  },

  props: {
    item: {
      type: Object,
      default: () => ({
        id: "",
        title: "",
        text: ""
      })
    },
    search: String
  },

  computed: {
    categories() {
      const category = this.$store.state.category,
        categoryentity = this.$store.state.categoryentity;

      var result = {};

      for (const id in categoryentity) {
        if (this.item.id === getEntityFromCategoryEntityId(id)) {
          result[getCategoryFromCategoryEntityId(id)] =
            category[getCategoryFromCategoryEntityId(id)];
        }
      }
      return result;
    }
  },

  methods: {
    titleInput(value) {
      this.item.title = value;

      this.$store.dispatch("setModelItem", {
        model: "note",
        id: this.item.id,
        item: {
          title: value
        }
      });
    },

    textInput(value) {
      this.item.text = value;

      this.$store.dispatch("setModelItem", {
        model: "note",
        id: this.item.id,
        item: {
          text: value
        }
      });
    },

    createCategoryHandler(title) {
      const createCategory = () => {
        const id = this.$store.getters.newId();

        if (!this.$store.state.note[this.item.id]) {
          this.$store.dispatch("setModelItem", {
            model: "note",
            id: this.item.id,
            item: {}
          });
        }

        this.$store.dispatch("setModelItem", {
          model: "category",
          id,
          item: decodeModelItem("category", id, {
            title
          })
        });

        this.$store.dispatch("setModelItem", {
          model: "categoryentity",
          id: makeCategoryEntityId(id, this.item.id),
          item: {
            category: id,
            entity: this.item.id
          }
        });
      };

      this.$emit("show-dialog", {
        title: "Warning",
        text: "Do you want to cretate new category '" + title + "'?",
        buttons: [
          { title: "Create", handler: createCategory },
          { title: "Cancel", handler: undefined }
        ]
      });
    },

    selectCategoryHandler(category) {
      if (!this.$store.state.note[this.item.id]) {
        this.$store.dispatch("setModelItem", {
          model: "note",
          id: this.item.id,
          item: {}
        });
      }

      this.$store.dispatch("setModelItem", {
        model: "categoryentity",
        id: makeCategoryEntityId(category, this.item.id),
        item: {
          category,
          entity: this.item.id
        }
      });
    },

    removeCategoryHandler(category) {
      this.$store.dispatch("deleteModelItem", {
        model: "categoryentity",
        id: makeCategoryEntityId(category, this.item.id)
      });
    }
  }
};
</script>

<style lang="sass" scoped>
.content-note-editor
  display: flex
  flex-flow: column
  align-items: stretch
  justify-content: stretch

  &>.header
    flex: 0 0 auto
    display: flex
    flex-flow: row wrap
    padding: 0 $step*0.5 $step*0.5 0
    border-bottom: 1px solid $color-primary

    &>*
      flex: 0 0 auto
      overflow: hidden
      margin: $step*0.5 0 0 $step*0.5

  &>.content
    flex: 1 1 auto
    overflow-x: hidden
    overflow-y: auto
    padding: $step

    &>* + *
      margin-top: $step*0.5

    &>.category
      display: flex
      flex-flow: row wrap
      align-items: center
      justify-content: start

      &>* + .v-category-badge
        margin-left: $step

      &>* + .v-category-input
        margin-left: $step

    &>.title
      font-weight: bold
      font-size: $step*3
      letter-spacing: 1px
      color: $color-dark
      min-height: $step*3*1.2

    &>.text
      font-size: $step*2
      color: $color-primary
      min-height: 70vh
</style>
