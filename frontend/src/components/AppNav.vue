<template>
    <header class="bg-primary sticky top-0 z-10 p-0">
      <nav class="flex justify-between flex-row my-0 h-full p-0 mx-6 text-center">
        <!--Logo-->
        <RouterLink to="/" class="text-2xl text-center font-bold position-relative hover:cursor-pointer text-center" v-slot="{ navigate }" custom>
          <div @click="navigate" class="text-center py-4 ">FakeFinder</div>
        </RouterLink>
  
        <!--Desktop Menu-->
        <ul class="hidden md:flex text-xl font-semibold h-max h-full p-0">
          <li
            v-for="item in items"
            :key="item.name"
            class=" py-4 px-6 flex-1  hover:shadow-md hover:bg-sky-500 h-max h-full p-0"
          >
            <RouterLink :to="item.path"  v-slot="{ navigate }" custom>
              <div @click="navigate" class="hover:cursor-pointer transition duration-300 h-full h-max">{{ item.name }}</div>
            </RouterLink>
          </li>
        </ul>
  
        <!--Mobile Menu Button-->
        <button
          class="md:hidden text-gray-600 dark:text-gray-200 focus:outline-none"
          @click="menuOpen = !menuOpen"
        >
          <svg
            v-if="!menuOpen"
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
          <svg
            v-else
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </nav>
      <div v-show="menuOpen">
        <!--Mobile Menu-->
        <ul class="md:hidden width-full text-center text-xl font-semibold mt-4">
          <li
            v-for="item in items"
            :key="item.name"
            class="px-4 py-2 transition duration-300 hover:shadow-md hover:bg-sky-500 h-max text-center"
            v-on:click.stop
          >
            <RouterLink :to="item.path" custom v-slot="{ navigate }" @click="menuOpen = false">
              <div role="link" @click="navigate" class="hover:cursor-pointer">{{ item.name }}</div>
            </RouterLink>
          </li>
        </ul>
      </div>
    </header>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const items = ref([
      { name: 'Home', path: '/' },
      { name: 'About', path: '/about' }
  ]);
  
  const menuOpen = ref(false);
  
  </script>