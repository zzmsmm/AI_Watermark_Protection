<template>
  <el-card shadow="always" body-style="padding:20px"
           style="height: 190px;width: 230px;margin: 15px;display: inline-block"
           v-loading="this.state==='mining...'" element-loading-text="mining..."
           element-loading-spinner="el-icon-loading">
    <div style="display: flex;justify-content:space-around;align-items: center;font-weight: 600">
      <i class="el-icon-folder"></i>
      <span>验证电路 {{id+1}}</span>
		<el-switch
		  v-model="value"
		  active-color="#13ce66"
		  inactive-color="#c8c8c8"
		  @change="changestate()">
		</el-switch>
      <span style="color: orange"></span>
    </div>
    <div style="margin-top: 20px;display: flex;justify-content: space-between;align-items: center">
      <span>状态</span>
      {{state}}
    </div>
    <div style="margin-top: 10px;display: flex;justify-content: space-between;align-items: center">
      <span>提供方</span>
      {{supplier}}
    </div>
    <div style="margin-top: 10px;display: flex;justify-content: space-between;align-items: center">
      <span style="width: 50px;">详情</span>
      {{detail}}
    </div>
  </el-card>
</template>

<script>
  export default {
    name: "Circuit",
    props: {
      id: 0,
      state: '',
      supplier: '',
      detail: '',
	  value: false
    },
    data() {
      return {
        colors: {2: '#32CD32', 4: '#32CD32', 5: '#32CD32'},
        samples: 20,
        supplier: this.supplier,
        detail: this.detail,
      }
    },
    methods: {
		changestate(){
			this.$emit("change", this.value, this.id)
			if (this.state === '待选用' && this.value === true) {
				this.state = '已选用'
			}
			else {
				this.state = '待选用'
			}
		}
	},
  computed: {
  },
    watch: {
	  value: function (val){
		  if (val === true) {
			  this.state = '已选用'
		  }
		  else {
			  this.state = '待选用'
		  }
	  }
    }
  }
</script>

<style scoped>
</style>
