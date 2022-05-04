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
          <el-descriptions size="medium" column="3"
            style="width: 700px;">
              <el-descriptions-item label="水印类型">
                  <el-tag type="info" size="small" :effect="tag_type">{{watermark_type}}</el-tag>
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
            <a v-bind:href="['http://127.0.0.1:8000/download/?id=' + this.hash]">
              <el-button type="warning"
                         @click=""
                         v-text="download"
                         size="small"
                         disabled="true">
              </el-button>
            </a>
          </div>
          <el-divider content-position="left"><h3 style="color: #606266;">
            <svg-icon icon-class="complete" style="margin-right: 10px;"/>材料提交</h3>
          </el-divider>
          <div>
            <p>提交相关材料以完成认证...</p>
            <el-upload
              class="upload-demo"
              action="https://jsonplaceholder.typicode.com/posts/"
              :on-change="handleChange"
              :file-list="fileList">
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
            </el-upload>
          </div>
      </el-col>
      <el-col :span="4" :offset="2">
        <el-steps :active="1" finish-status="success" direction="vertical" style="margin-top: 20px; margin-bottom: 20px; height: 420px;">
          <el-step title="算法推荐" icon="el-icon-edit"></el-step>
          <el-step title="密钥下载" icon="el-icon-download"></el-step>
          <el-step title="材料提交" icon="el-icon-upload"></el-step>
          <el-step title="认证完成" icon="el-icon-document-checked"></el-step>
        </el-steps>
      </el-col>
      </el-card>
    </el-row>
  </div>
</template>

<script>
export default{
   data() {
     return {
       hash: '',
       watermark_type: '黑盒',
       model_type: 'NLP',
       algorithm_name: 'lulu算法',
       tag_type: '',
       download: '下载密钥',
       detail: '这里是算法详情介绍...',
       filelist: []
     }
   },
   created(){
   	this.getDetail()
   },
   methods: {
    goBack() {
      this.$router.push({ path:'/certification/list/' })
     },
	  getDetail(){
      this.hash = this.$route.params.id
      if (this.watermark_type === '黑盒') this.tag_type = 'dark'
    },
    handleChange(file, fileList) {
      this.fileList = fileList.slice(-3);
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
