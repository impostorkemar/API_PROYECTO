from typing import Optional
from pydantic   import BaseModel

class User(BaseModel):
    id: Optional[str]
    name: str
    email:str    
    password: str

class Centro_costo(BaseModel):
    id_centro_costo: Optional[int]
    nombre_centro: str
    tienda: str    
    cuenta: str

class Candidato(BaseModel):
    cedula: Optional[str]
    nombre: str
    apellido: str    
    genero: str
    direccion_domicilio: str
    ciudad: str
    provincia: str
    estado_civil: str
    telefono_celular: str
    telefono_casa: str
    direccion_correo: str
    fecha_nacimiento: str
    edad: int
    nacionalidad: str
    status: str

class Experiencia_laboral(BaseModel):
    id_experiencia_laboral: Optional[int]    
    cedula: str 
    nombre_experiencia: str
    tiempo_experiencia: int
    estudios_universitarios: int

class Contrato(BaseModel):
    id_contrato: Optional[int]
    tipo_contrato: str
    fecha_inicio_contrato: str    
    salario: float
    observaciones: str

class Usuario(BaseModel):
    id_usuario: Optional[int]
    cedula: str
    nombre_usuario: str    
    password: str

class Cargo(BaseModel):
    id_cargo: int    
    nombre_cargo: str    

class Personal(BaseModel):
    id_personal: Optional[int]
    id_centro_costo: int
    cedula: str    
    status: str
    adendum_contrato: str
    id_contrato: int
    id_cargo: int

class Consulta(BaseModel):
    texto: str
    