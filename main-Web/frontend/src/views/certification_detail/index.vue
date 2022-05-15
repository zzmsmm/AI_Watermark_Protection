<template>
  <div>
    <el-row>
      <el-button type="text" @click="goBack()"
            style="font-weight: bold; margin-left: 10px;">
            <i class="el-icon-back" style="font-weight: bold; font-size: 15px; margin-right: 5px;"></i>
              返回
      </el-button>
    </el-row>
    <el-row>
      <el-card style="margin-left: 2%;margin-right: 2%;">
      <el-col :span="18">
          <el-divider content-position="left">
            <h3 style="color: #606266;">
              <svg-icon icon-class="apply" style="margin-right: 10px;"/>
              申请信息
            </h3>
          </el-divider>
          <el-descriptions size="medium" :column="3"
            style="width: 700px;">
              <el-descriptions-item label="水印类型">
                  <el-tag type="info" size="small" :effect="watermark_type === '黑盒' ? 'dark' : ''">
                  {{watermark_type}}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="模型类型">{{model_type}}</el-descriptions-item>
              <el-descriptions-item label="算法推荐">{{algorithm_name}}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="Hash">{{hash}}</el-descriptions-item>
          </el-descriptions>
          <el-divider content-position="left"><h3 style="color: #606266;">
            <svg-icon icon-class="introduction" style="margin-right: 10px;"/>算法介绍</h3>
          </el-divider>
          <div>
            <p>{{detail}}</p>
            <a v-bind:href="['http://127.0.0.1:8000/download_key/?hash=' + this.hash]">
              <el-button type="warning"
                         @click="setprocess(2)"
                         v-text="download"
                         size="small">
              </el-button>
            </a>
          </div>
          <el-divider content-position="left"><h3 style="color: #606266;">
            <svg-icon icon-class="complete" style="margin-right: 10px;"/>材料提交</h3>
          </el-divider>
          <div>
            <p>提交相关材料以完成注册...</p>
            <el-upload
              class="upload-demo"
              action="http://127.0.0.1:8000/upload_test/"
              :on-change="handleChange"
              multiple
              :limit="1"
              :on-exceed="handleExceed"
              :before-remove="beforeRemove"
              :file-list="fileList">
              <el-button size="small" type="primary" @click="setprocess(3)">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">上传材料...</div>
            </el-upload>
          </div>
          <el-button size="medium" type="success"
          style="width:30%; margin-left:40%;"
          @click="finished_apply">注册</el-button>
      </el-col>
      <el-col :span="4" :offset="2">
        <el-steps :active="activestep" finish-status="success" direction="vertical" style="margin-top: 20px; margin-bottom: 20px; height: 420px;">
          <el-step title="算法推荐" icon="el-icon-edit"></el-step>
          <el-step title="密钥下载" icon="el-icon-download"></el-step>
          <el-step title="材料提交" icon="el-icon-upload"></el-step>
          <el-step title="注册完成" icon="el-icon-document-checked"></el-step>
        </el-steps>
      </el-col>
      </el-card>
    </el-row>
  </div>
</template>

<script>
import { unfinished_detail } from '@/api/certification'
export default{
   data() {
     return {
       hash: '',
       watermark_type: '',
       model_type: '',
       algorithm_name: '',
       download: '下载密钥',
       detail: '这里是算法详情介绍...',
       fileList: [],
       activestep: 1,
     }
   },
   created(){
   	this.getDetail()
   },
   methods: {
    goBack() {
      this.$router.push({ path:'/certification/list/' })
     },
    setprocess(step) {
      //console.log(step)
      this.activestep = step
    },
	  getDetail(){
      this.hash = this.$route.params.id
      unfinished_detail(this.hash).then(response => {
        const { data } = response
        this.watermark_type = data.watermark_type
        this.model_type = data.model_type
        this.algorithm_name = data.algorithm_name
      })
    },
    finished_apply() {
      console.log(this.fileList.length)
      //this.$router.push({ path:'/home' })
      this.activestep = 4
    },
    handleChange(file, fileList) {
      this.fileList = fileList.slice(-3)
    },
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${ file.name }？`);
    }
  }
}
</script>

<style>
    .el-divider {
        //background-color: #b6d7fb;
        //height: 2px;
        margin-top: 30px;
        margin-bottom: 30px;
      }
</style>
