<template>
  <div>
    Hello, conference!
    Your code is {{ conferenceCode }}
  </div>
</template>

<script>
export default {
  computed: {
    conferenceCode () {
      return this.$route.params.code;
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
