let http = require("http");
let fs = require("fs");
const sqlite3 = require('sqlite3').verbose(); 

let db = new sqlite3.Database('weapons.db');

http.createServer(function(request,response){
	
	switch(request.url){
		case "/":
			fs.readFile("./ajax_weapons.html",function(err,content){
				if(!err){
					response.writeHead(200,{"Content-Type":"text/html;charset = utf-8"});
					response.end(content,"utf-8");
				}
				else{
					response.writeHead(500,{"Content-Type":"text/html;charset = utf-8"});
					response.end(err.message,"utf-8");
					console.log(err);
				}
			});
			break;
		case "/sql_table":
			response.writeHead(200,{"Content-Type":"text/html;charset = utf-8"});
		
			var jsonPost = '';
			var field; //Колонка таблицы
            var field_value; //Значение этой колонки
            var post;

        	request.on('data', function(data) {
            	jsonPost += data;
        	});

        	request.on('end', function() {
            	post = JSON.parse(jsonPost);  

            	if(post === ""){
            		SqlQueryField();
            	}
            	else{
            		field = Parsing_Field(post);
            		field_value = Parsing_Field_Value(post);

            		if(field != "NULL" && field_value != "NULL"){
            			SqlQueryField("SELECT * FROM Weapons WHERE " + field + "= ?",field_value);
            		}
            		else{
            			response.end(JSON.stringify(1));
            		}
            	}
            	
        	});

			break;
		default:
			response.writeHead(404,{"Content-Type":"text/html;charset = utf-8"});
			response.end("404, NOT FOUND: " + request.url);
	}

	function SqlQueryField(prepare_sql = "SELECT * FROM Weapons", field_value = []){
		db.all(prepare_sql,field_value,function(err,rows){
			if(err){
				response.write(err);
			}
			else{
			//	response.writeHead(200, {'Content-Type': 'application/json'});
				response.end(JSON.stringify(rows));
			}
		});
	}

	function Parsing_Field(post){
		var field;
         
        if(post.includes("ID")){
            field = "ID";
   		}
        else if(post.includes("Weapon")){
            field = "Weapon";
       	}
        else if(post.includes("Country")){
           	field = "Country";
       	}
        else if(post.includes("Type")){
           	field = "Type";
       	}
        else if(post.includes("Calibre")){
           	field = "Calibre";
       	}
       	else{
           	field = "NULL";
       	}
       	return field;
	}

	function Parsing_Field_Value(post){
		var field_value;
		var index = post.indexOf("=");

		if(Parsing_Field(post) === "NULL" || index === -1){
			field_value = "NULL";
		}
		else{
			field_value = post.slice(index + 1, post.length);
			field_value = field_value.replace(/\s/g,''); //удаляем пробелы
		}

		return field_value;
	}

}).listen(3000);