<template>
  <div class="v-category-input" ref="root">
    <div>
      <div>
        <input
          :class="{ active: !!active }"
          type="text"
          ref="input"
          v-model="title"
          @blur="cancelHandler($event)"
        />
        <button @click="createHandler">
          <span class="icon-add" @blur="cancelHandler($event)"></span>
        </button>
      </div>
      <div :class="{ active: !!active && filtered.length }">
        <button
          v-for="category in filtered"
          :key="category.id"
          @click="selectHandler(category.id)"
          @blur="cancelHandler($event)"
        >
          {{ category.title }}
        </button>
        <p v-if="filtered.length && categories.length > 10">...</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CategoryInput",

  data() {
    return {
      active: false,
      title: ""
    };
  },

  computed: {
    categories() {
      const $category = this.$store.state.category;
      var result = [];

      for (const id in $category) {
        result.push($category[id]);
      }

      return result;
    },

    filtered() {
      var result = [];

      for (let category of this.categories) {
        if (
          category.title.toLowerCase().indexOf(this.title.toLowerCase()) !== -1
        ) {
          result.push(category);

          if (result.length > 10) {
            break;
          }
        }
      }

      return result;
    }
  },

  methods: {
    createHandler() {
      if (this.active) {
        if (this.title) {
          this.$emit("create", this.title);
        }
        this.active = false;
      } else {
        this.active = true;
        this.title = "";

        this.$nextTick(() => {
          this.$refs.input.focus();
        });
      }
    },

    selectHandler(id) {
      this.$emit("select", id);
      this.active = false;
    },

    cancelHandler(event) {
      if (!this.$refs.root.contains(event.relatedTarget)) {
        this.active = false;
      }
    }
  }
};
</script>

<style lang="sass" scoped>
.v-category-input
  position: relative
  color: $color-tertiary

  &>div
    overflow: hidden
    display: flex
    flex-flow: column
    justify-content: stretch
    align-items: stretch

    &>div
      border-radius: $step*2
      border: 1px solid $color-tertiary

    &>div:nth-of-type(1)
      overflow: hidden
      display: flex
      flex-flow: row
      justify-content: stretch
      align-items: center

      &>input
        display: none
        padding: 0 $step

        &.active
          display: block

      &>button
        font-size: $step*2
        line-height: $step*2
        padding: 1px 0 0 1px

        &:hover
          color: $color-white
          background-color: $color-tertiary

    &>div:nth-of-type(2)
      position: absolute
      top: 120%
      left: 0
      width: 100%
      z-index: 1000
      overflow: hidden
      display: none
      flex-flow: column
      justify-content: stretch
      align-items: stretch
      background-color: $color-white

      &.active
        display: flex

      &>button
        padding: $step*0.5 $step
        text-align: start

        &:hover
          background-color: $color-gray

      &>p
        padding: $step*0.5 $step
        font-weight: bold
        text-align: center
</style>
