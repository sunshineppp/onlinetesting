<template>
  <el-table ref="multipleTable" :data="files" tooltip-effect="dark" style="width: 100%">
    <el-table-column label="文件大小" show-overflow-tooltip prop="size">
    </el-table-column>
    <el-table-column label="上传日期">
      <template slot-scope="scope">{{ scope.row.create_time }}</template>
    </el-table-column>
    <el-table-column label="">
      <template slot-scope="scope">
        <el-button @click="open(scope.$index, scope.row)">按钮</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
 
<script>
export default {
  data() {
    return {
      files:[{
            create_time:"2020-07-12",
            size: 324156
        },{
            create_time:"2020-07-11",
            size: 348921
        }]
    }
  },
  methods: {
    open(index, row){
      console.log(index);
      console.log(row.create_time);
      // console.log(scope.row.create_time);
    }
  }
};
</script>
