class custom_search{
  constructor(){
    this.test = "test";
    this.col = "col";
    this.table_id = "id";
  }

  search_by_req(){
    var t1 = document.getElementById('course_r'); //c_requirements
    this.deleteTableRows(t1);
    var checkboxes = ['req1','req2','req3','req4','req5','req6','req7','req8','req9','req10','req11','req12','req13'];
    var req_query = "";
    for (var y of checkboxes){
      if(document.getElementById(y).checked){
        req_query = req_query.concat(document.getElementById(y).value+",");
      }
    }
    req_query = req_query.substring(0,req_query.length-1);
    if (req_query !== ""){
      this.search1(req_query);
    }
  }

  search_by_ct(){
    var t3 = document.getElementById('req_r2'); //course title
    this.deleteTableRows(t3);
    var course_t_query = document.getElementById('coursetitle').value;
    if (course_t_query !== ""){
      this.search2(course_t_query);
    }
  }

  search_by_cn(){
    var t2 = document.getElementById('req_r1'); //course number
    this.deleteTableRows(t2);
    var course_n_query = document.getElementById('coursenumber').value;
    if (course_n_query !== ""){
      this.search3(course_n_query);
    }
  }

  gen_search(){ //pc.gen_search()
    this.search_by_ct()
    this.search_by_cn()
  }

  search_template(url,done_function){
    $.ajax({
      url: url,
      method: 'GET'
    }).fail(function(){console.log("failed")}).done(function(server_data){
      done_function(server_data);
    })
  }

  search1(req_query){
    //searching for courses that fulfill listed requirements
    var url = "/api/v1/sqlreq/" + req_query;
    this.search_template(url,this.req_query_done_function);
  }

  search2(course_t_query){
    //searching by <title> for requirements that a course(s) fulfills
    var url = "/api/v1/sqlcoursetitle/" + course_t_query;
    this.search_template(url,this.req_query_done_function2);
  }

  search3(course_n_query){
    var url = "/api/v1/sqlcoursenumber/" + course_n_query;
    this.search_template(url,this.req_query_done_function3);
  }

  deleteTableRows(table){ //clears the table rows, leaving the table columns
    var length = table.rows.length;
    for (let idx = 0; idx < length-1; idx++){
      table.deleteRow(1);
    }
   }
   req_query_done_function(server_data){
     var data = JSON.parse(server_data); //array
     for (var row of data){
       var tr = document.createElement('tr');
       for (var i = 0;i<2;i++){
         var td0 = document.createElement('td');
         td0.innerHTML = row[i];
         tr.appendChild(td0);
       }
       tr.className = "table-bordered";
       document.getElementById('course_r').append(tr);
     }
   }
   req_query_done_function2(server_data) {
     var data = JSON.parse(server_data); //array
     for (var row of data){
       var tr = document.createElement('tr');
       for (var i = 0;i<3;i++){
         var td0 = document.createElement('td');
         td0.innerHTML = row[i];
         tr.appendChild(td0);
       }
       tr.className = "table-bordered";
       document.getElementById('req_r2').append(tr);
     }
   }
   req_query_done_function3(server_data){
     var data = JSON.parse(server_data); //array
     for (var row of data){
       var tr = document.createElement('tr');
       for (var i = 0;i<3;i++){
         var td0 = document.createElement('td');
         td0.innerHTML = row[i];
         tr.appendChild(td0);
       }
       tr.className = "table-bordered";
       document.getElementById('req_r1').append(tr);
     }
   }
  onload(){
    var query1 = "select course.title,course.number,B.cout from (select course,count(requirement) as cout from course_requirement group by course order by cout DESC limit 5) as B join course on (B.course=course.id);";
    $.ajax({
      url: "/api/v1/sql/" + query1,
      method: 'GET'
    }).fail(function(){console.log("failed")}).done(function(server_data){
      var data = JSON.parse(server_data); //array
      for (var row of data){
        var tr = document.createElement('tr');
        for (var i = 0;i<3;i++){
          var td0 = document.createElement('td');
          td0.innerHTML = row[i];
          tr.appendChild(td0);
        }
        tr.className = "table-bordered";
        document.getElementById('top5').append(tr);

      }
    })
  }
}

var pc = new custom_search();
window.onload =  function(){
  pc.onload();
}

//populating the select options for the form
function append_select_options(id,lst){
  for(var i = 0; i < lst.length; i++) {
      var opt = document.createElement('option');
      opt.innerHTML = lst[i];
      opt.value = lst[i];
      console.log(id);
      if (document.getElementById(id) != null){
            document.getElementById(id).appendChild(opt);
	}
  }
  //document.getElementById(id).setAttribute('class','table table-striped table-hover table-bordered');
}

append_select_options('coursenumber',course_nums);
append_select_options('coursetitle',course_titles);
