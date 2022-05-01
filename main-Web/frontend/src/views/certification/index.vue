<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="80px">
      <el-form-item label="模型名称">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item label="模型算法">
        <el-select v-model="form.region" placeholder="请选择活动区域">
          <el-option label="alg1" value="shanghai"></el-option>
          <el-option label="alg2" value="beijing"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="模型有效期">
        <el-col :span="11">
          <el-date-picker type="date" placeholder="选择日期" v-model="form.date1" style="width: 100%;"></el-date-picker>
        </el-col>
        <el-col class="line" :span="2">-</el-col>
        <el-col :span="11">
          <el-time-picker placeholder="选择时间" v-model="form.date2" style="width: 100%;"></el-time-picker>
        </el-col>
      </el-form-item>
      <el-form-item label="模型">
        <el-switch v-model="form.delivery"></el-switch>
      </el-form-item>
      <el-form-item label="模型特性">
        <el-checkbox-group v-model="form.type">
          <el-checkbox label="模型1" name="type"></el-checkbox>
          <el-checkbox label="模型2" name="type"></el-checkbox>
          <el-checkbox label="模型3" name="type"></el-checkbox>
          <el-checkbox label="模型4" name="type"></el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item label="模型!">
        <el-radio-group v-model="form.resource">
          <el-radio label="alg1"></el-radio>
          <el-radio label="alg2"></el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="上传模型">
        <el-upload
          class="upload-demo"
          action="https://jsonplaceholder.typicode.com/posts/"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :before-remove="beforeRemove"
          multiple
          :limit="3"
          :on-exceed="handleExceed"
          :file-list="fileList">
          <el-button size="small" type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
        </el-upload>
      </el-form-item>
      <el-form-item label="模型备注">
        <el-input type="textarea" v-model="form.desc"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">立即申请</el-button>
        <el-button>取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        name: '',
        region: '',
        date1: '',
        date2: '',
        alg: false,
        type: [],
        resource: '',
        desc: ''
      }
    }
  },
  methods: {
    onSubmit() {
      console.log('submit!')
    },
    handleRemove(file, fileList) {
      console.log(file, fileList)
    },
    handlePreview(file) {
      console.log(file)
    },
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`)
    }
  }
}
</script>

<style>
</style>