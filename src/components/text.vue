<!-- <template>
    <div>
        <button @click="search">点我</button>
        <ul>
            <li v-for="item in postList" :key="item.id">
                {{ item.id }} {{ item.analysis }}
            </li>
        </ul>
    </div>
    <div>
        题目问题：<input type="text">
        <button @click="add">新增题目</button>
    </div>
</template>
 
  <script>
   import axios from 'axios'

   //省略URL相同部分
   axios.defaults.baseURL = "http://localhost:5000"

        export default {
            data() {
                return {
                    postList:[]
                }
            },
            methods: {
                search(){
                    //传统方法
                    // axios({
                    //     method: "GET",
                    //     url: "http://localhost:5000/question"
                    // }).then(res => {
                    //     console.log(res); 
                    // })

                    //常用方法
                    axios.get("/question")
                    .then(res => {
                        console.log(res);
                        this.postList =  res.data;
                    }).catch(reason => {
                        console.log("异常触发");
                        console.log(reason);
                    })
                },
                add(){
                    axios.post("/question",{
                        analysis: "xxx"
                    }).then(res => {
                        console.log(res);
                    }).catch(reason => {
                        console.log("异常触发");
                        console.log(reason);
                    })
                    this.search();
                }
            }
        };
</script> -->
