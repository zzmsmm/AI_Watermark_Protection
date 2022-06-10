<template>
    <el-container style="padding: 20px 250px">
      <el-header height="110px">
		<div style="text-align: center;margin-top: 10px">
		  <el-progress :percentage="currentpercentage" :status="currentstatus"></el-progress>
		</div>
		<div style="text-align: center;margin-top: 20px">
		  <div style="text-align: center;margin-top: 12px">
		  <el-button :type="type"
					@click="showDialog()"
		             v-text="generate"
		             size="medium"
					:disabled="is_finish">
		  </el-button>
		  </div>
		</div>
      </el-header>
		<el-dialog title="上传" :visible.sync="dialogOfUpload" width="50%" style="text-align: center;">
			<el-upload class="upload-demo" action="#" drag multiple :headers="headers" :auto-upload="false"
			 :file-list="fileList" :on-change="handleChange">
				<i class="el-icon-upload"></i>
				<div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
				<div class="el-upload__tip" slot="tip"></div>
			</el-upload>
			<div slot="footer" class="dialog-footer">
				<el-button @click="dialogOfUpload = false">取 消</el-button>
				<el-button type="primary" @click="confirmUpload()">上 传</el-button>
			</div>
		</el-dialog>
		<div style="text-align: center;margin-top: 0px" v-if="state">
		  <span><svg-icon icon-class="search" style="color: #66b1ff; margin-right: 10px;"/>识别结果: <b>{{number}}</b></span>
		</div>
    </el-container>
</template>

<script>
import {upload, permission} from '@/api/user'
  export default {
    name: "centralizationfl",
	inject:['reload'],
    components: {
    },
    data() {
      return {
		dialogOfUpload: false,
		flag: false,
		fileList: [],
        activestep: 0,
        traintime: 100,
		generate: '点击上传',
        currentpercentage: 0,
        currentstatus: null,
		is_finish: false,
		state: false,
		number:"",
		type: "primary"
      }
    },
    created() {
      this.initCircuit()
    },
    watch: {
    },
    methods: {
			showDialog() {
			this.dialogOfUpload = true
			},
      setprocess(step) {
        console.log("set")
        this.activestep = step
      },
	  handleChange(file, fileList) { //文件数量改变
	  	this.fileList = fileList;
	  },
      confirmUpload() {
        this.setprocess(2);
		this.generate = "图像识别中..."
		var param = new FormData();
		this.fileList.forEach(
			(val, index) => {
				param.append("file", val.raw);
			}
		);
		upload(param).then(responce => {
			if(responce.msg === 'success') {
				this.number = responce.number
				this.dialogOfUpload = false;
				let interval = setInterval(() => {
				  this.currentpercentage += 1
				  this.currentstatus = null
				  if (this.currentpercentage === 100) {
					clearInterval(interval)
				    this.currentstatus = 'success'
				    this.setprocess(3)
					this.type = "success"
					this.is_finish = true
					this.generate = "识别成功"
					this.state = true
					}
				}, this.traintime * 50 / 100)
			}
		});
      }
    }
  }
</script>

<style scoped>
  .menu {
    margin-top: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center
  }
</style>
