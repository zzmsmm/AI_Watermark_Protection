<template>
  <div class="dashboard-editor-container">
    <panel-group />
    <incentivecurve ref="incentiveDom"></incentivecurve>
  </div>
</template>

<script>
import PanelGroup from './components/PanelGroup'
import incentivecurve from './components/curve'

export default {
  name: 'DashboardAdmin',
  components: {
    PanelGroup, incentivecurve
  },
  data() {
    return {
    }
  },
  methods: {
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .github-corner {
    position: absolute;
    top: 0px;
    border: 0;
    right: 0;
  }

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
