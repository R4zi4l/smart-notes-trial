<template>
  <section id="view-application">
    <router-view />
  </section>
</template>

<script>
export default {
  name: "Application"
};
</script>

<style lang="sass">
@import "@/styles/_normalize.sass"
@import "@/styles/_design_system.sass"
@import "@/styles/_iconic.sass"

#view-application
  display: flex
</style>
