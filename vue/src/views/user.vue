<template>
    <div>

    <section>
        <div class="color"></div>
        <div class="color"></div>
        <div class="color"></div>
        <div class="box">
            <div class="square" style="--i:0;" id="data" @click="todata">data</div>
            <div class="square" style="--i:1;" id="study" @click="tostudy">study</div>
            <div class="container">
                <div class="form" id="sign">
                    <form id="_form" @submit.prevent="trans">
                        <div>
                            <textarea name="word" v-model="word" cols="30" rows="5" placeholder="请输入文本"></textarea>
                        </div>
                        <div>
                            <input type="checkbox" name="hold" v-model="hold" id="hold">
                            <label for="hold">将此单词添加至我的学习</label>
                        </div>
                        <div>
                            <input type="submit" value="翻译" id="sub" @click.prevent="trans">
                        </div>
                    </form>
                    <div id="result">
                        <p id="i1"></p>
                        <p id="i2"></p>
                        <p id="i3"></p>
                        <p id="i4"></p>
                        <p id="i5"></p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    </div>
</template>
<script>
export default{
    data(){
        return {
            username:this.$route.params.username,
            word:'',
            hold:''
        }
    },
    methods:{
        tostudy(){
            this.$router.push(`/study/${this.username}`);
        },
        todata(){
            this.$router.push(`/data/${this.username}`);
        },
        trans(){
            console.log(this.hold)
            fetch('http://localhost:81/api/v1.0', {
                method: ['POST'],
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    word: this.word,
                    hold: this.hold,
                    username: this.username
                })
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    document.getElementById('i1').innerText = data['english']
                    document.getElementById('i2').innerHTML = data['phonetic']
                    document.getElementById('i3').innerHTML = data['chinese']
                    document.getElementById('i4').innerHTML = data['sentence1']
                    document.getElementById('i5').innerHTML = data['sentence2']
                })
                .catch((error) => {
                    console.error('Error', error)
                })


        }
    }

}
</script>
<style scoped>
@import '@/assets/login.css';
#in {
                width: 320px;
                height: 100px;
                border-radius: 10px;
                border: 0;
                padding: 10px;
                outline: 10px rgb(27, 139, 225);
            }

#sub {
                height: 30px;
                width: 70px;
                border-radius: 10px;
                border-color: #f1f4f9;
                outline: 10px rgb(27, 139, 225);
                margin-left: 10px;
            }

</style>