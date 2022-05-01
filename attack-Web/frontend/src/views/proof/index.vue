<template>
  <el-container v-if="flag" style="height: 100vh;padding:1% 3% 0 3%">
    <el-aside style="padding: 20px 30px 0 0">
      <h3>选择验证电路</h3>
      <div class="menu">
        可用电路数量
        <el-input-number
          v-model="circuitNum"
          controls-position="right"
          :min="1"
          :max="5"
          size="mini"
        ></el-input-number>
      </div>
      <div class="menu">
        选择电路
        <el-select v-model="circuitvalue"
                   placeholder="选择一个验证电路"
                   size="mini"
                   @change="setprocess(1)">
          <el-option
            v-for="item in circuitoptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            :disabled="item.disabled">
          </el-option>
        </el-select>
      </div>
	  <div style="text-align: center;margin-top: 20px">
	    <div style="text-align: center;margin-top: 12px">
			<a v-bind:href="['http://127.0.0.1:8000/download/?id=' + this.circuitvalue]">
				<el-button type="warning"
							@click=""
							v-text="download"
							size="medium"
							:disabled="is_finish">
				</el-button>
			</a>
	    </div>
	  </div>
      <el-divider></el-divider>
      <h3>提交证明</h3>
      <div style="text-align: center;margin-top: 10px">
        <el-progress :percentage="currentpercentage" :status="currentstatus"></el-progress>
      </div>
      <div style="text-align: center;margin-top: 20px">
        <div style="text-align: center;margin-top: 12px">
        <el-button type="success"
				   @click="showDialog()"
                   v-text="generate"
                   size="medium"
				   :disabled="is_finish">                   
        </el-button>
        </div>
      </div>
    </el-aside>
    <el-container style="padding: 20px 50px">
      <el-header height="140px">
        <h3>流程</h3>
		<div>
		  <el-steps :active=activestep finish-status="success" align-center>
		    <el-step title="选择验证电路"></el-step>
		    <el-step title="提交证明"></el-step>
		    <el-step title="完成" icon="el-icon-finished"></el-step>
		  </el-steps>
		</div>
      </el-header>
      <el-main style="border: lightgray dashed 1px;border-radius: 10px;background-color: #f7f8fb"
               v-loading="this.state==='synchronizing...'" element-loading-text="blockchain synchronizing...">
		<div style="display: flex;justify-content: flex-start;align-content: flex-start;flex-wrap: wrap">
		  <Circuit v-for="(circuit,index) in circuitList" :key="index" :id="index" :state="state[index]" 
      :value="value[index]" :supplier="supplier[index]" :detail="detail[index]" @change="changevalue"></Circuit>
        </div>
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
      </el-main>
    </el-container>
  </el-container>
	<el-container v-else-if="!flag" style="height: 100vh;padding:1% 3% 0 3%">
		<el-aside style="padding: 20px 30px 0 0">
		<h2>您无权查看此页面!!</h2>
		</el-aside>
	</el-container>
</template>

<script>
import {upload, permission} from '@/api/user'
  import Circuit from "./components/Circuit";
  export default {
    name: "centralizationfl",
	inject:['reload'],
    components: {
      Circuit
    },
    data() {
      return {
		flag: false,
		dialogOfUpload: false,
		fileList: [],
        activestep: 0,
        supplier:["企业A","银行B","学校C","景区D",],
        detail:["绩点不低于3.7...","收入不低于5000...","--","--","--",],
        circuitNum: 4,
        circuitList: [],
        circuitoptions: [
			{
				value: '1', label: '验证电路1'
			},
			{
				value: '2', label: '验证电路2'
			},
			{
				value: '3', label: '验证电路3'
			},
			{
				value: '4', label: '验证电路4'
			}
        ],
        circuitvalue: '',
        traintime: 100,
        download: '下载电路',
		generate: '点击上传',
        state: ['待选用', '待选用', '待选用', '待选用', '待选用'],
        currentpercentage: 0,
        currentstatus: null,
        updatetime: '', //
		value: [false, false, false, false, false],
		is_finish: false
      }
    },
    created() {
      this.initCircuit()
	  this.getPermission()
    },
    watch: {
      circuitNum: function () {
        this.initCircuit()
      },
	  circuitvalue: function () {
		for(var i = 0;i < this.circuitNum;i++){
			if(i == this.circuitvalue - 1) this.value[i] = true
			else this.value[i] = false
		}
	  }
    },
    methods: {
			getPermission() {
				permission().then(response => {
					if(response.msg == '1') {
						this.flag = true;
					}
					else this.flag = false;
				});
			},
			showDialog() {
			this.dialogOfUpload = true
			},
      initCircuit() {
        this.circuitList = new Array(this.circuitNum)
		    for(var i = 5;i < this.circuitNum;i++){
			    this.state[i] = '待选用';
			    this.value[i] = false;
				this.supplier[i]="--";
				this.detail[i]="--";
			}
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
		var param = new FormData();
		this.fileList.forEach(
			(val, index) => {
				param.append("file", val.raw);
			}
		);
		upload(param).then(responce => {
			if(responce.msg === 'success') {
				this.dialogOfUpload = false;
				let interval = setInterval(() => {
				  this.currentpercentage += 1
				  this.currentstatus = null
				  if (this.currentpercentage === 100) {
					clearInterval(interval)
				    this.currentstatus = 'success'
				    this.setprocess(3)
					this.is_finish = true
					this.generate = "上传成功"
					}	
				}, this.traintime * 100 / 100)
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
