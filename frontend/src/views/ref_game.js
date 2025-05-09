<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
		<style>
		/* 父子网页界面设计 */
		   .kid{
		   	width: 100px;
		   	height: 100px;
		   	background-color: #aaffff;
		   	border: 1px solid black;
		   	margin: 10px;
		   	float: left;
		   }
		   .par{
		   	width: 1000px;
		   	padding: 10px;
		   	border: 1px solid black;
		   	float: left;
		   }
		</style>
		<script>
		     var f=0;
			 var id2=0;
			 var find = [0,0,0,0,0,0,0,0,0];
			 var marked=0;
			window.onload = function(){
				//规则：五个背景图，每张图出现两次，随机分配到16个div中
				var ele = document.getElementById("parent");
				
				var imgs = [1,2,3,4,5,6,7,8]; 				
				
				var is = [0,0,0,0,0,0,0,0,0];
				
				for(var i = 0; i < 16; i++){
					var index = getImgIndex(is);
					console.info(index);
					ele.innerHTML += "<div id='k"+i+"' class='kid' "
						+"οnclick='oclick(this.id,"+index+");'></div>";				
				}
			}
			function getImgIndex(is){
				var index = parseInt(Math.random()*8)+1;
				if(is[index] < 2){
					is[index]++;
				} else {
					index = getImgIndex(is);
				}
				return index;
			}
			function oclick(id,index)
			{   
				if(find[index]<2)
				{
			    if(f==0){
			    find[index]++;
				look(id,index);
				f=index;
				id2=id;
				}
				else
				{
					if(f==index&&id!=id2)
					{   
						find[index]++;
						look(id,index);
						f=0;
						id2=0;
						marked++;
					}
					else
					{   
						find[f]=0;
						look(id,index);
						look(id2,f);
						clearStyle(id);
						clearStyle(id2);
						f=0;
						id2=0;
					}
				}
				}
				if(marked==8)
				{
					alert("恭喜完成");
				}
			}
			function look(id,index){
				var ele = document.getElementById(id);
				ele.style="background-image: url("+index+".gif);";
			}
			function clearStyle(id){
				setTimeout(function(){
						var ele = document.getElementById(id);
						ele.style="";
					}, 200);
			}
			function re(){
				window.location.reload();
			}
		</script>
	</head>
	<body>
		<div id="parent" class="par"></div>
			<input type="button" name="b1" id="b1" value="再van♂一次" onclick="re();"/>
	</body>
</html>

