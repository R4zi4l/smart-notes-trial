<template>
  <div class="v-text-editor">
    <textarea
      v-if="multiline"
      :value="value"
      @input="$emit('input', $event.target.value)"
    ></textarea>
    <input v-else :value="value" @input="$emit('input', $event.target.value)" />
    <span :class="{ hidden: value }">{{ placeholder }}</span>
    <div v-html="processValue(value, search)"></div>
  </div>
</template>

<script>
import browser from "./../utils/browser.js";

export const processValue = (text, search) => {
  if (search) {
    search = browser.escapeRegExp(search);
    search = new RegExp(search, "ig");

    const chunks = text.split(search);

    if (chunks.length > 1) {
      const matches = [...text.matchAll(search)];

      if (browser.isIE) {
        text = browser.escapeHtml(chunks[0]).replace(/ /g, " <wbr>");

        for (let i = 0; i < matches.length; ++i) {
          text +=
            "<span class='highlighter'>" +
            browser.escapeHtml(matches[i][0]).replace(/ /g, " <wbr>") +
            "</span>" +
            browser.escapeHtml(chunks[i + 1]).replace(/ /g, " <wbr>");
        }
      } else {
        text = browser.escapeHtml(chunks[0]);

        for (let i = 0; i < matches.length; ++i) {
          text +=
            "<span class='highlighter'>" +
            browser.escapeHtml(matches[i][0]) +
            "</span>" +
            browser.escapeHtml(chunks[i + 1]);
        }
      }
    } else {
      text = browser.escapeHtml(chunks[0]);
    }
  } else {
    text = browser.escapeHtml(text);

    if (browser.isIE) {
      text = text.replace(/ /g, " <wbr>");
    }
  }

  text = text.replace(/\n$/g, "\n\n");
  return text;
};

export default {
  name: "TextEditor",

  props: {
    multiline: {
      type: Boolean,
      default: true
    },

    placeholder: {
      type: String,
      default: ""
    },

    search: {
      type: String,
      default: ""
    },

    value: {
      type: String,
      default: ""
    }
  },

  methods: {
    processValue(text, search) {
      return processValue(text, search);
    }
  }
};
</script>

<style lang="sass">
.v-text-editor>.span.highlighter
  background-color: $color-secondary
  background-color: alpha($color-secondary, '88')
</style>

<style lang="sass" scoped>
.v-text-editor
  position: relative
  overflow: hidden
  -webkit-text-size-adjust: none

  width: 100%
  min-height: 100%

  &>*
    width: 100%
    overflow: hidden
    font: inherit
    letter-spacing: inherit
    white-space: pre-wrap
    word-wrap: break-word
    vertical-align: top

    &.hidden
      visibility: hidden

  &>textarea, &>input, &>span
    position: absolute
    top: 0
    left: 0
    height: 100%
    z-index: 2
    display: block
    resize: none
    background-color: transparent
    color: inherit

  &>span
    z-index: 1
    color: darken($color-gray, 30)

  &>div
    pointer-events: none
    color: transparent
</style>
