var app = new Vue({
    el: '#app',
    data: {
        allInfo: []
    },

    created: function() {
        this.flush();
    },

    methods: {
        delOne: function(id){
            this.$http.get('./cgi-bin/info.py',{params: {req: 2, id: id}}).then(function(res){
                if(res.body.status == 1){
                    alert('删除成功');
                    this.flush(); 
                }
            });
        },
        toUpdateOne: function(id){
            $('#updateModal').modal()
            update.updateOne(id)
        },
        flush: function(){
            this.$http.get('./cgi-bin/info.py', {params: {req: 1}}).then(function(res){
                this.allInfo = res.body;
            });
        },
    },
})

var insert = new Vue({
    el: '#insert',
    data: {
        name: '',
        sex: null,
        age: null,
        email: ''
    },
    methods: {
        insertOne: function(){
            this.$http.get('./cgi-bin/info.py', {params: {
                req: 3,
                name: this.name,
                sex: this.sex,
                age: this.age,
                email: this.email
            }}).then(function(res){
                if(res.body.status == 1){
                    alert('添加成功!!');
                    app.flush();
                    this.name =  '';
                    this.sex =  null;
                    this.age =  null;
                    this.email =  '';
                    $('#insertModal').modal('hide');
                }
            })
        }
    }
})

var update = new Vue({
    el: "#update",
    data: {
        id: null,
        name: '',
        sex: null,
        age: null,
        email: ''
    },
    methods: {
        updateOne: function(id){
            this.id = id
            console.log(this.name)
            this.$http.get('./cgi-bin/info.py', {params: {
                req: 4,
                id: id
            }}).then(function(res){
                this.name = res.body.name,
                this.sex = res.body.sex,
                this.age = res.body.age,
                this.email = res.body.email
            })
        },
        updateCi: function(){
            this.$http.get('./cgi-bin/info.py', {params: {
                req: 5,
                id: this.id,
                name: this.name,
                sex: this.sex,
                age: this.age,
                email: this.email
            }}).then(function(res){
                if(res.body.status == 1){
                    alert('修改成功!!');
                    app.flush();
                    this.name =  '';
                    this.sex =  null;
                    this.age =  null;
                    this.email =  '';
                    $('#updateModal').modal('hide');
                }
            })
        }
    }
})