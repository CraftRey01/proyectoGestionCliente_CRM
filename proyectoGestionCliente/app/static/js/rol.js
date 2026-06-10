
// Cargar todos los roles disponibles al cargar la página
  async function cargarRoles() {
    const selectRol = document.getElementById('rol');
    try {
      const response = await fetch('/api/roles');
      
      if (response.ok) {
        const data = await response.json();
        const roles = data.roles || [];
        
        selectRol.innerHTML = '<option value="">Selecciona un rol...</option>';
        
        if (roles.length > 0) {
          roles.forEach(rol => {
            const option = document.createElement('option');
            option.value = rol;
            option.textContent = rol.charAt(0).toUpperCase() + rol.slice(1);
            selectRol.appendChild(option);
          });
          selectRol.disabled = false;
        } else {
          selectRol.innerHTML = '<option value="">No hay roles disponibles</option>';
          selectRol.disabled = true;
        }
      } else {
        selectRol.innerHTML = '<option value="">Error al cargar roles</option>';
        selectRol.disabled = true;
      }
    } catch (error) {
      console.error('Error:', error);
      selectRol.innerHTML = '<option value="">Error al cargar roles</option>';
      selectRol.disabled = true;
    }
  }

  // Cargar roles cuando la página carga
  document.addEventListener('DOMContentLoaded', cargarRoles);

  // Deshabilitar el botón de envío si faltan campos
  const inputUsuario = document.getElementById('nombre_usuario');
  const inputContrasena = document.getElementById('contrasena');
  const selectRol = document.getElementById('rol');
  const btnEnviar = document.querySelector('.btn-login');

  function actualizarEstadoBoton() {
    const todosCompletos = inputUsuario.value.trim() && inputContrasena.value && selectRol.value;
    btnEnviar.disabled = !todosCompletos;
  }

  inputUsuario.addEventListener('change', actualizarEstadoBoton);
  inputUsuario.addEventListener('input', actualizarEstadoBoton);
  inputContrasena.addEventListener('change', actualizarEstadoBoton);
  inputContrasena.addEventListener('input', actualizarEstadoBoton);
  selectRol.addEventListener('change', actualizarEstadoBoton);
  
  // Estado inicial
  actualizarEstadoBoton();