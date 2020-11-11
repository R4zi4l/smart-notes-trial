<template>
  <div class="content-category-editor">
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
        placeholder="Category title"
        :multiline="false"
        @input="titleInput($event)"
      ></v-text-editor>

      <v-text-editor
        class="text"
        :value="item.text"
        :search="search"
        placeholder="Category text"
        @input="textInput($event)"
      ></v-text-editor>
    </div>
  </div>
</template>

<script>
import IconButton from "./../IconButton.vue";
import TextEditor from "./../TextEditor.vue";

export default {
  name: "CategoryEditor",

  components: {
    "v-icon-button": IconButton,
    "v-text-editor": TextEditor
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

  methods: {
    titleInput(value) {
      this.item.title = value;

      this.$store.dispatch("setModelItem", {
        model: "category",
        id: this.item.id,
        item: {
          title: value
        }
      });
    },

    textInput(value) {
      this.item.text = value;

      this.$store.dispatch("setModelItem", {
        model: "category",
        id: this.item.id,
        item: {
          text: value
        }
      });
    }
  }
};
</script>

<style lang="sass" scoped>
.content-category-editor
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

      &>button
        color: $color-tertiary

      &>button + button
        margin-left: $step

      &>button:hover
        text-decoration: underline

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
