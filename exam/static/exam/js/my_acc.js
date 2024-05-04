function updateProfile() { 
  var name = document.getElementById("inputName").value; 
  var surname = document.getElementById("inputSurname").value; 
  var profession = document.getElementById("inputProfession").value; 
  var organization = document.getElementById("inputOrganization").value; 
  
  var fullName = name + " " + surname; 

  document.getElementById("name").innerText = fullName; 
  document.getElementById("profession").innerText =  profession; 
  document.getElementById("organization").innerText =  organization; 
}

/* Выше это функция кнопик сохранить чтобы то что я ввожу и сохраняю в инпут отображалось под аватаркой
Снизу просто базовая функиця загрузки*/

document.getElementById('avatar-upload').addEventListener('change', function(event) {
    var file = event.target.files[0];
    var reader = new FileReader();
    
    reader.onload = function(e) {
      document.querySelector('.avatar-frame img').src = e.target.result;
    }
    
    reader.readAsDataURL(file);
  });

