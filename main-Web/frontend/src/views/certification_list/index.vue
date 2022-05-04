<template>
	<el-card style="height: 520px;">
		<el-table
		  :data="tableData.filter(data => !search
      || data.hash.toLowerCase().includes(search.toLowerCase())
      || data.watermark_type.toLowerCase().includes(search.toLowerCase())
      || data.model_type.toLowerCase().includes(search.toLowerCase()))"
		  height="520" style="width: 100%"
      :cell-style="cellStyle">
		  <el-table-column
		    label="Hash"
		    prop="hash"
			  width="300px" align="center">
        <template slot-scope="scope">
          <!--
        	 <el-button type="text" plain size="small" @click="todetail(scope.row.hash)">{{scope.row.hash}}</el-button>
          -->
          <el-tooltip content="点击查看详情" placement="top">
            <a href="javascript:;" @click="todetail(scope.row.hash)">{{scope.row.hash}}</a>
          </el-tooltip>
        </template>
		  </el-table-column>
		  <el-table-column
		    label="水印算法"
		    prop="algorithm_name" align="center">
		  </el-table-column>
      <el-table-column
        label="水印类型"
        prop="watermark_type" align="center">
      </el-table-column>
      <el-table-column
        label="模型类型"
        prop="model_type" align="center">
      </el-table-column>
		  <el-table-column
		    align="right">
		    <template slot="header" slot-scope="scope">
		      <el-input
		        v-model="search"
		        size="medium"
		        placeholder="输入关键字搜索"
			  prefix-icon="el-icon-search" />
		    </template>
		  </el-table-column>
		</el-table>
	</el-card>
</template>

<script>
import {unfinished_list} from '@/api/certification'
  export default {
    data() {
      return {
        tableData: [],
				search: '',
				timer: null //定时器名称
      }
    },
	created(){
	  this.getlist()
		this.timer = setInterval(() => {
			setTimeout(this.getlist(), 0)
		}, 1000 * 30)
	},
    methods: {
      getlist(){
        unfinished_list(this.$store.getters.token).then(response => {
          console.log(response)
          const { data } = response
          console.log()
          var count = 0
          for(var i in data){
            count ++
          }
          console.log(count)
          for(var i = 0;i<count;i++){
          this.$set(this.tableData,i,data[i])
          }

        })
      },
      cellStyle ({ row, column, rowIndex, columnIndex }) {
        if (columnIndex === 0) {
          return 'color: #409eff; font-weight: bold'
        } else {
          return 'color: #666666'
        }
      },
      todetail(id) {
      			this.$router.push({ path:'/certification/detail/'+id })
      },
      beforeDestroy() {
        clearInterval(this.timer);
        this.timer = null;
      }
    },
  }
</script>

<style lang="scss" scoped>

  .card-panel-col {
    margin-bottom: 32px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-message {
        background: #36a3f7;
      }

      .icon-money {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-message {
      color: #36a3f7;
    }

    .icon-money {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
}

@media (max-width:550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
