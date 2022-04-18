<template>
	<el-container style="height: 100vh;padding:1% 3% 0 3%">
		<el-aside width="600px">
			<el-container>
			  <el-header>
				  <h2><svg-icon icon-class="user" style="color: #2a68a7; margin-right: 10px;"/>{{title}}</h2><hr />
			  </el-header>
			  <el-container>
			    <el-aside width="300px">
					<div style="margin-top: 50px; margin-left: 20px;">
						<img :src="user_img" width="250px"/>
					</div>
				</el-aside>
			    <el-main>
					<div style="margin-top: 10px;">
						<span><svg-icon icon-class="documentation" style="color: #2a68a7; margin-right: 10px; margin-top: 20px;"/>{{name_title}}</span>
						<p><b>{{name}}</b></p> 
						<span><svg-icon icon-class="documentation" style="color: #2a68a7; margin-right: 10px; margin-top: 30px;"/>{{age_title}}</span>
						<p><b>{{age}}</b></p>
						<span><svg-icon icon-class="documentation" style="color: #2a68a7; margin-right: 10px; margin-top: 30px;"/>联系方式</span>
						<p><b>{{phone}}</b></p>			
					</div>	
				</el-main>
			  </el-container>
			</el-container>
		</el-aside>
	</el-container>
</template>

<script>
import{permission} from "@/api/user.js"
  export default {
	name: "blockinfo",
    data() {
      return {
				title: '',
				name_title: '',
				age_title: '',
				name: '',
				age: '',
				phone: '',
				user_img: '',
      }
    },
	mounted() {
		this.getInfo()
	},
    methods: {
		getInfo() {
			permission().then(response => {
				if(response.msg == '1') {
					this.title = '个人信息';
					this.name_title = '姓名';
					this.age_title = '年龄';
					this.name = 'Bob';
					this.age = '22';
					this.phone = '12345678910';
					this.user_img = require('@/assets/kuli.jpg')
				}
				else if(response.msg == '2') {
					this.title = '单位信息';
					this.name_title = '负责人姓名';
					this.age_title = '单位名称';
					this.name = 'hh';
					this.age = 'A';
					this.phone = '29876543211';
					this.user_img = require('@/assets/qiye.jpeg')
				}
			})
		}
    },
  }
</script>

<style lang="scss" scoped>
  .errPage-container {
    padding: 30px;
  }

  .card-panel-col {
    margin-bottom: 30px;
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