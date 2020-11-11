<template>
  <div class="v-drag-and-drop" ref="root">
    <div ref="content">
      <slot></slot>
    </div>
  </div>
</template>

<script>
// import Vue from "vue";
import { makeDragAndDropMouseController } from "./../utils/utils.js";

export default {
  name: "DragAndDrop",

  props: {
    detail: {
      type: undefined,
      default: undefined
    }
  },

  mouseController: undefined,

  methods: {
    beginDragHandler() {
      const root = this.$refs.root,
        content = this.$refs.content;

      root.style.height = content.getBoundingClientRect().height + "px";
      content.style.width = root.getBoundingClientRect().width + "px";
    },

    endDropHandler() {
      this.$refs.root.style.height = "";
      this.$refs.content.style.width = "";
    }
  },

  mounted() {
    this.mouseController = makeDragAndDropMouseController(
      this.$refs.content,
      this.detail,
      this.beginDragHandler,
      undefined,
      this.endDropHandler
    );

    this.mouseController.bind();
  },

  beforeDestroy() {
    this.mouseController.unbind();
  }
};
</script>

<style lang="sass" scoped></style>
