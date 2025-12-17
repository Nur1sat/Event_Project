<template>
  <div class="flex items-center space-x-3">
    <!-- Logo Icon - Using image file -->
    <div class="flex items-center justify-center w-8 h-8.5">
      <img src="/image.png" alt="JIHC Logo" class="w-full h-full" />
    </div>
    
    <!-- Text - Dynamic color based on page -->
    <div class="flex flex-col">
      <span :class="['text-base font-bold', isHome ? 'text-gray-900' : 'text-gray-900']">JIHC</span>
      <span :class="['text-xs', isHome ? 'text-gray-700' : 'text-gray-700']">clubs</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'JIHCLogo',
  props: {
    isHome: {
      type: Boolean,
      default: false
    }
  }
}
</script>

