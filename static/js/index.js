function validate(){
	var fInput=document.getElementById("profilePic");
	var email=document.getElementById("email");
	var userId=document.getElementById("userId");
	var password=document.getElementById("password");
	var flag=0;
	if(fInput.value.length!=0){
		/* file validation */
		var validExt= /(\.jpg|\.jpeg|\.png|\.gif)$/i;
		if (!validExt.exec(fInput.value)) {
			document.getElementById("filecheck").innerHTML='<font color="red">Only JPEG, JPG, PNG and GIF formats are supported!</font>';
            fInput.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("filecheck").innerHTML='<font color="green">Looks good!</font>';
			flag=1;
            fInput.style.borderColor="green";
		} 
    }
	if(email.value.length!=0){
		/* email validation */
		var res=email.value.split('@');
		var ext = /(\.com|\.in|\.ac.in|\.net)$/i;
		if (res[0].length<2 || res[1].length<4 || !ext.exec(res[1]) || res[1]==undefined || res[0]==undefined){
			document.getElementById("emailcheck").innerHTML='<font color="red">Please enter a valid email!</font>';
			flag=0;
            email.style.borderColor="red";
		}
		else{
			document.getElementById("emailcheck").innerHTML='<font color="green">Looks good!</font>';
			flag=1;
            email.style.borderColor="green";
		} 
    }

	if(userId.value.length!=0){
		/* userId validation */
		var res=userId.value
		if (res.length<5 || res.length>20) {
			document.getElementById("idcheck").innerHTML='<font color="red">Length of User Id should be in between 5-20 characters!</font>';
            userId.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("idcheck").innerHTML='<font color="green">Looks good!</font>';
            userId.style.borderColor="green";
			flag=1;
		} 
    }

	if(password.value.length!=0){
		/* password validation */
		var res=password.value
		if (res.length<6 || res.length>15) {
			document.getElementById("passcheck").innerHTML='<font color="red">length of Password should be in between 6-15 characters!</font>';
            password.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("passcheck").innerHTML='<font color="green">Looks good!</font>';
            password.style.borderColor="green";
			flag=1;
		}
	 
    }

    if(flag==1){
        return true;
    }
    else{
        return false;
    }	
}

function validate_login(){
	var userId=document.getElementById("userId");
	var password=document.getElementById("password");
	var flag=0;

	if(userId.value.length!=0){
		/* userId validation */
		var res=userId.value
		if (res.length<5 || res.length>20) {
			document.getElementById("idcheck").innerHTML='<font color="red">&nbsp;&nbsp;&nbsp;&nbsp;Length of User Id should be in between 5-20 characters!</font>';
            userId.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("idcheck").innerHTML='<font color="green">&nbsp;&nbsp;&nbsp;&nbsp;Looks good!</font>';
			flag=1;
            userId.style.borderColor="green";
		} 
    }

	if(password.value.length!=0){
		/* password validation */
		var res=password.value
		if (res.length<6 || res.length>15) {
			document.getElementById("passcheck").innerHTML='<font color="red">&nbsp;&nbsp;&nbsp;&nbsp;Length of Password should be in between 6-15 characters!</font>';
            password.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("passcheck").innerHTML='<font color="green">&nbsp;&nbsp;&nbsp;&nbsp;Looks good!</font>';
			flag=1; 
            password.style.borderColor="green";
		}
	 
    }

    if(flag==1){
        return true;
    }
    else{
        return false;
    }	
}

function remove_msg(){
	if(document.getElementById("alert alert-success")!=null){
		document.getElementById("alert alert-success").style.display='none';
	}
	if(document.getElementById("alert alert-danger")!=null){
		document.getElementById("alert alert-danger").style.display='none';
	}
}

function getUsersData(){
	fetch('/users')
	.then(
		(res) => {
			return res.json();
		}
	)
	.then(
		(data)=>{
			if(data.users.length > 0){
				let users='<div class="user-data-div"><table><tr><th>User ID</th><th>Profile</th><th>Username</th><th>Email</th><th>Action</th></tr>';
				data.users.map(
					(user)=>{
						users=users.concat("<tr>");
						users=users.concat("<td>"+ user.userID +"</td>");
						users=users.concat('<td><img src="'+ user.profilePic +'" class="profile"></td>');
						users=users.concat("<td>"+ user.username +"</td>");
						users=users.concat("<td>"+ user.email +"</td>");
						if(user.isActive == 1){
							users=users.concat('<td><input type="submit" class="btn btn-danger" value="Deactivate" onClick="deactivate('+ user.userID +')"></td>');	
						}
						else{
							users=users.concat('<td><input type="submit" class="btn btn-primary" value="Activate" onClick="activate('+ user.userID +')"></td>');
						}
						users=users.concat("</tr>");
					}
				);
				users=users.concat("</table></div>");
				document.getElementById("user_data").innerHTML=users;
				document.getElementById("getUsersDataBtn").style.visibility='hidden';
			}
			else{
				document.getElementById("user_data").innerHTML='<h1><font color="white">No data available.</font></h1>';
			}

		}
	);
}

function activate(id){
	fetch('/activate/'+id)
	.then((res)=>{
		return res.json()
	})
	.then(
		(response)=>{
			if(response.status==200){
				getUsersData();
			}
		}
	);
}
function deactivate(id){
	fetch('/deactivate/'+id)
	.then((res)=>{
		return res.json()
	})
	.then(
		(response)=>{
			if(response.status==200){
				getUsersData();
			}
		}
	);
}

function set_settings_param(){
	let code=document.getElementById("settings_mode").value;
	let data;
	if(code!=99){
		if(code==0){
			data="<center><table>";
			data+='<tr><td><b>New User Name</b></td><td><input type="text" id="uname" name="uname" placeholder="User Name"></td></tr><tr><td><b>(re-Type)New User Name</b></td><td><input type="text" id="reuname" name="reuname" placeholder="Retype User Name"></td></tr><tr><td><input type="submit" value="Change" onClick="changeUname()" class="btn btn-primary"></td><td><input type="reset" value="Cancel" class="btn btn-danger"></td></tr></table><div id"unamecheck"></div></center>';
		}
		else if(code==1){
			data="<center><table>";
			data+='<tr><td><b>New Password</b></td><td><input type="password" name="pass" id="pass" placeholder="Password"></td></tr><tr><td><b>(re-Type)New Password</b></td><td><input type="password" id="repass" name="repass" placeholder="Retype password"></td></tr><tr><td><input type="submit" value="Change" onClick="changePass()" class="btn btn-primary"></td><td><input type="reset" value="Cancel" class="btn btn-danger"></td></tr></table><div id="passcheck"></div></center>';	
		}
		else if(code==2){
			data="<center><table>";
			data+='<tr><td><b>New Email</b></td><td><input type="email" name="email" id="email" placeholder="Email"></td></tr><tr><td><b>(re-Type)New Email</b></td><td><input type="email" id="reemail" name="reemail" placeholder="Retype Email"></td></tr><tr><td><input type="submit" value="Change" onClick="changeEmail()" class="btn btn-primary"></td><td><input type="reset" value="Cancel" class="btn btn-danger"></td></tr></table><div id="emailcheck"></div></center>';
		}
		else if(code==3){
			data="<center>";
			 data+='<form method="post" enctype="multipart/form-data" onSubmit="return validateAndUpload()" action="changeProfilePicture"><table><tr><td><b>New Profile Picture</b></td><td><input type="file" id="profpic" name="profpic" onChange="validateUpload()" name="profpic"></td></tr><tr><td><input type="submit" value="Change" class="btn btn-primary"></td><td><input type="reset" value="Cancel" class="btn btn-danger"></td></tr></table></form><div id="filecheck"></div></center>';
		}
		else{
			data="Invalid selection code!";
		}
	}
	else{
		data="";
	}
	document.getElementById("settings").innerHTML=data;
}

function changeUname(){
	let nuname=document.getElementById("uname");
	let renuname=document.getElementById("reuname");
	if(nuname.value==renuname.value){
		if (nuname.length<5 || renuname.length>20) {
			document.getElementById("unamecheck").innerHTML='<font color="red">length of User name should be in between 5-20 characters!</font>';
			nuname.style.borderColor="red";
			renuname.style.borderColor="red";
		}
		else{
			let formdata = new FormData();		
			formdata.append("mode", "0");
			formdata.append("value", nuname.value);

			let requestOptions = {
  				method: 'POST',
  				body: formdata,
  				redirect: 'follow'
			};	

		fetch("/changeCredentials", requestOptions)
		.then(response => response.json())
		.then((result) => {
			if(result.status==200){
				  window.location.href='http://127.0.0.1:5000/';
			}
			else{
				alert("Server error! Try again later.");
			}
		})
  		.catch(error => console.log('error', error));
		
		
		}
		
	}
	else{
		document.getElementById("unamecheck").innerHTML='<font color="red">User Name and retyped User Name not matching!</font>';
		nuname.style.borderColor="red";
		renuname.style.borderColor="red";

	}

}

function changePass(){
	var npass=document.getElementById("pass");
	var renpass=document.getElementById("repass");
	if(renpass.value==npass.value){
		if (npass.length<6 || npass.length>15) {
			document.getElementById("passcheck").innerHTML='<font color="red">length of Password should be in between 6-15 characters!</font>';
			npass.style.borderColor="red";
			renpass.style.borderColor="red";
		}
		else{
			let formdata = new FormData();		
			formdata.append("mode", "1");
			formdata.append("value", npass.value);

			let requestOptions = {
  				method: 'POST',
  				body: formdata,
  				redirect: 'follow'
			};	

		fetch("/changeCredentials", requestOptions)
		.then(response => response.json())
		.then((result) => {
			if(result.status==200){
				  window.location.href='http://127.0.0.1:5000/';
			}
			else{
				alert("Server error! Try again later.");
			}
		})
  		.catch(error => console.log('error', error));
		
		}
	}
	else{
		document.getElementById("passcheck").innerHTML='<font color="red">Password and retyped password not matching!</font>';
		npass.style.borderColor="red";
		renpass.style.borderColor="red";

	}

}


function changeEmail(){
	var nemail=document.getElementById("email");
	var reemail=document.getElementById("reemail");
	if(reemail.value==nemail.value){
		let formdata = new FormData();		
			formdata.append("mode", "2");
			formdata.append("value", nemail.value);

			let requestOptions = {
  				method: 'POST',
  				body: formdata,
  				redirect: 'follow'
			};	

		fetch("/changeCredentials", requestOptions)
  		.then(response => response.json())
  		.then((result) => {
			  if(result.status==200){
					window.location.href='http://127.0.0.1:5000/';
			  }
			  else{
				  alert("Server error! Try again later.");
			  }
		  })
  		.catch(error => console.log('error', error));
		
		
		}
	else{
		document.getElementById("emailcheck").innerHTML='<font color="red">Email and retyped email not matching!</font>';
		npass.style.borderColor="red";
		renpass.style.borderColor="red";

	}

}

function validateUpload(){
	var fInput = document.getElementById("profpic")
	var flag = 0
	if(fInput.value.length!=0){
		/* file validation */
		var validExt= /(\.jpg|\.jpeg|\.png|\.gif)$/i;
		if (!validExt.exec(fInput.value)) {
			document.getElementById("filecheck").innerHTML='<font color="red">Only JPEG, JPG, PNG and GIF formats are supported!</font>';
			fInput.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("filecheck").innerHTML='<font color="green">Looks good!</font>';
			flag=1;
			fInput.style.borderColor="green";
		} 
	}
	if(flag==0){
		return false;
	}
	else{
		return true;
	}

}

function set_task_param(){
	let code=document.getElementById("task_mode").value;
	let data;
	if(code!=99){
		if(code==1){
			data="<center>";
			data+='<form method="post" enctype="multipart/form-data" onSubmit="return validateAndUploadInfer()" action="inference"><table><tr><td><b>Image : </b></td><td><input type="file" id="inferPic" onChange="validateUploadInfer()" name="inferPic"></td></tr><tr><td><input type="submit" value="Infer" class="btn btn-primary"></td><td><input type="reset" value="Cancel" class="btn btn-danger"></td></tr></table></form><div id="filecheck"></div></center>';	
		}
		else if(code==2){
			data="";
			data+='<div class="d-flex align-items-center">';
  			data+='<strong>Fetching data...</strong>'
  			data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
			data+='</div>'
			getModelStats();
		}
		else if(code==3){
			data="";
			data+='<div class="d-flex align-items-center">';
  			data+='<strong>Fetching data...</strong>'
  			data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
			data+='</div>'
			getDataset();
		}
		else{
			data="Invalid selection code!";
		}
	}
	else{
		data="";
	}
	document.getElementById("task").innerHTML=data;
}


function getDataset(){
	fetch('/getDataset')
	.then((res)=>{
		return res.json()
	})
	.then(
		(response)=>{
			if(response.status==200){
				let data="";
				data+="<b>Dataset fetched successfully!</b><br>";
				data+='<table class="user-data-div">';
				data+='<tr><th>Class Name</th><th>Data</th></tr>';
				response.images.map((dataset)=>{
					data+='<tr>';
					data+='<td>'+ dataset.name +'</td>';
					data+='<td><img src="'+ dataset.image +'" class="dataset-image"></td>';
					data+='</tr>';
				});
				response.videos.map((dataset)=>{
					data+='<tr>';
					data+='<td>'+ dataset.name +'</td>';
					data+='<td><video class="dataset-video" controls><source src="'+ dataset.video +'" type="video/mp4"> Your Browser does not support video media! </video></td>';
					data+='</tr>';
				});
				data+="</table>";
				document.getElementById("task").innerHTML=data;
			}
		}
	);
}

function getModelStats(){
	fetch('/getModelStats')
	.then((res)=>{
		return res.json()
	})
	.then(
		(response)=>{
			if(response.status==200){
				let data="";
				data+="<b>Model statistics fetched successfully!</b><br>";
				data+='<table class="user-data-div">';
				data+='<tr><th>Parameter</th><th>Value</th></tr>';
				response.params.map((param)=>{
					data+='<tr>';
					data+='<td>'+ param.name +'</td>';
					data+='<td>'+ param.value +'</td>';
					data+='</tr>';
				});
				data+="</table>";
				document.getElementById("task").innerHTML=data;
			}
		}
	);
}

function validateUploadInfer(){
	var fInput = document.getElementById("inferPic")
	var flag = 0
	if(fInput.value.length!=0){
		/* file validation */
		var validExt= /(\.jpg|\.jpeg|\.png|\.gif)$/i;
		if (!validExt.exec(fInput.value)) {
			document.getElementById("filecheck").innerHTML='<font color="red">Only JPEG, JPG, PNG and GIF formats are supported!</font>';
			fInput.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("filecheck").innerHTML='<font color="green">Looks good!</font>';
			flag=1;
			fInput.style.borderColor="green";
		} 
	}
	if(flag==0){
		return false;
	}
	else{
		let formData=new FormData();
		formData.append('file',fInput.files[0]);
		let requestOptions = {
			method: 'POST',
			body: formData,
			redirect: 'follow'
	  };	
		let data="";
		data+='<div class="d-flex align-items-center">';
		data+='<strong>Making inference...</strong>'
		data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
		data+='</div>'
		document.getElementById("task").innerHTML=data;
	fetch("/inference", requestOptions)
	.then(response => response.json())
	.then((result) => {
		if(result.status==200){
			data='Response time = '+result.response_time +' Seconds.<br>';
			data+='<img src="'+ result.image +'" class="result_img">'
			data+='&nbsp;&nbsp;&nbsp;&nbsp;The supplied image belongs to <u><b>'+result.prediction + '</b></u> class!<br>';
			document.getElementById("task").innerHTML=data;
		}
		else{
			alert("Server error! Try again later.");
		}
	})
	.catch(error => console.log('error', error));

	}

}