<template>
  <div class="bg-black min-h-screen flex flex-col ">
    <AppNav />
    <main class="flex-grow w-[80%] lg:w-[50%] mx-auto">
      <router-view />
    </main>
    <AppFooter />
  </div>

</template>

<script setup>
import AppFooter from './components/AppFooter.vue';
import AppNav from './components/AppNav.vue';

  //
</script>
